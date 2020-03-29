import os
from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
from spectrum import mp3_to_img

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    for the_file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    for the_file in os.listdir('static/images'):
        file_path = os.path.join('static/images', the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('main.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    mp3_to_img(filename)
    spectrum_image = url_for('static', filename='images/' + filename[:-4] + '.png')
    return render_template('result.html', filename=filename, spectrum_image=spectrum_image)


if __name__ == '__main__':
  app.run(debug=True)
