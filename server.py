import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/akovacs/akproject/grocery-list/uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return """
    <html>
<body>
<h1>Camera Test</h1>
<form method=post enctype=multipart/form-data>
  <input type="file" name="file" accept="image/*;capture=camera">
  <input type=submit value=Upload>
</form>
</body>
</html>
"""
    else:
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('index',
                filename=filename))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

