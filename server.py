import os
import datetime
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from google.cloud import storage


UPLOAD_FOLDER = '/home/akovacs/akproject/grocery-list/uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
PROJECT_ID = '315041698645'
BUCKET_NAME = 'grocerylistyum'

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
            # Save local copy of the file
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # Upload to google cloud
            uploaded_url = upload_file(file.read(), file.filename, file.content_type)
            print(uploaded_url)
            return redirect(url_for('index',
                filename=filename))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    filename = _safe_filename(filename)

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url

