


from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


import colorgram
import numpy as np


import shrinker as shr

# UI/CSS
from flask_bootstrap import Bootstrap

import os
DIR = os.path.dirname(os.path.abspath(__file__))
print('DIR:',DIR)

UPLOAD_FOLDER = os.path.join(DIR,'static','imgs')
print('UPLOAD_FOLDER: ',UPLOAD_FOLDER)


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
# rgb_to_hex((255, 255, 195))




@app.route("/", methods=['GET', 'POST'])
def home():

    if request.method == "POST":

        for old_file in os.listdir(UPLOAD_FOLDER):
            # print(old_file)
            os.remove( os.path.join(UPLOAD_FOLDER,old_file))

        if 'file' not in request.files:
            flash('No file part')
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            print('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            print('Image successfully uploaded and displayed below')
            print(filename)

            # Extract 6 colors from an image.
            fullfilename = os.path.join(UPLOAD_FOLDER,filename)

            small_file = shr.downres(fullfilename)
            print(small_file)
            
            temp = colorgram.extract(small_file, 10)
            print(*temp)

            colors = []
            for c in temp:
                # print(c)
                # print(rgb_to_hex(c.rgb))

                rgb = str([c.rgb[0],c.rgb[1],c.rgb[2]])
                mean = round(((c.rgb[0]+c.rgb[1]+c.rgb[2])/3.0)/255,2)
                # sat = round(np.std([c.rgb[0],c.rgb[1],c.rgb[2]]),2)

                sat = round((max([c.rgb[0],c.rgb[1],c.rgb[2]]) - min([c.rgb[0],c.rgb[1],c.rgb[2]]))/255,2)

                txtcolor = '#f8f9fa'
                # print((c.rgb[0] + c.rgb[1] + c.rgb[2])/3.0)
                if mean > 0.5:
                    txtcolor = '#212529'

                colors.append({ 
                    'hex' : '#'+ str(rgb_to_hex(c.rgb)) , 
                    'rgb': rgb,
                    'mean': mean,
                    'sat': sat,
                    'txtcolor': txtcolor,
                    'percent':'{:.2f}'.format(c.proportion*100) 
                    })

            print(*colors,sep='\n')

            colors_by_percent = colors[:5]
            dark = sorted(colors, key=lambda x : x['mean'], reverse=False)[:5]
            light = sorted(colors, key=lambda x : x['mean'], reverse=True)[:5]

            high_sat = sorted(colors, key=lambda x : x['sat'], reverse=True)[:5]
            low_sat = sorted(colors, key=lambda x : x['sat'], reverse=False)[:5]

            return render_template(
                'index.html', 
                filename=filename, 
                colors_by_percent = colors_by_percent,
                dark = dark,
                light = light,
                high_sat = high_sat,
                low_sat = low_sat
                )
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            print('Allowed image types are - png, jpg, jpeg, gif')
            # return redirect(request.url)
            return render_template('index.html')

    return render_template('index.html')


if __name__ == '__main__':
    app.static_folder = 'static'
    app.debug = True
    app.run()


