from os import path
from flask import Flask, render_template, request, send_from_directory, redirect
from waitress import serve

from utilities import *

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('home.html', users = userCount(), images = imageCount(), version = VERSION)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        token = request.form['token']
        file = request.files["file"]
        extension = file.filename.split(".")[-1]

        if checkToken(token) is False:
            return 'Invalid token.', 401
        
        else:
            if 'file' not in request.files:
                return 'Bad request, no file has been found.', 400

            if file and allowed_file(file.filename):
                filename = generateFilename() + '.' + extension
                addUpload(token, filename)
                file.save(path.join(app.config["UPLOAD_FOLDER"], filename))
                print(f'[UPLOAD] {getUsername(token)} ( {token} ) has uploaded {filename}.')
                return f"{URL}/uploads/{filename}", 200

@app.route(f'/uploads/<file_name>')
def uploaded(file_name):
    return send_from_directory(UPLOAD_FOLDER, file_name)

@app.route('/deleteall/<token>')
def delete(token):
    if checkToken(token):
        if checkAdmin(token):
            deleteAll()
            return redirect('/')
        else:
            return 'Invalid administrator permissions.', 401

    else:
        return 'Invalid administrator permissions.', 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

serve(app, host="0.0.0.0", port=3000)