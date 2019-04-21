#!/usr/bin/env python3

from flask import Flask, render_template, url_for, redirect, request, flash
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'img/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/products") 
def product():
    return render_template("products.html")

@app.route("/login")
def login():
    return render_template("login.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


import infer
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    gc.collect()
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
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            res = infer.infer("img/"+filename)
            gc.collect()
            return render_template("prediction.html", cat=str(res[0]), prob=res[2].tolist())
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

import gc
gc.collect()


if __name__ == "__main__":
    app.run(debug=True, port = 8099)