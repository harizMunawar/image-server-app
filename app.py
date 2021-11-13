import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask('robi', static_folder='storage')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'LMAO'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return "I'm Alive"

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if request.args.get('folder'):
                if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('folder'))):
                    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('folder')))
                path = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('folder'), filename)
            else:
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return redirect(url_for('download', filename=filename, folder=request.args.get('folder')))
    else:
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
                <input type=file name=file>
                <input type=submit value=Upload>
            </form>
        '''

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    if request.args.get('folder'):
	    return send_from_directory(f'{app.config["UPLOAD_FOLDER"]}/{request.args.get("folder")}', filename)
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)
 