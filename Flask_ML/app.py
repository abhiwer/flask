
from flask import Flask, Response, render_template
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import warnings
from datetime import datetime
import json
import urllib
import requests
import flask
import urllib.request
import re
from flask import render_template, request, send_file, jsonify, Response
import zipfile
import os
from PIL import Image
from blob_storage_upload_code import AzureBlobFileUploader
from blob_storage_download_code import AzureBlobFileDownloader
from custom_vision_prediction_code import customvision
# Comiited by Abhinav & Aniket
app = flask.Flask(__name__, static_folder='static')

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

IMG_FOLDER = os.path.join('static', 'img')
UL_FOLDER = os.path.join('static', 'upload')
DL_FOLDER = os.path.join('static', 'download')
app.config['UPLOAD_FOLDER'] = UL_FOLDER
app.config['DOWNLOAD_FOLDER'] = DL_FOLDER
numImages = 18


warnings.filterwarnings('ignore')




@app.route('/video')
def video():
    return Response(process(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/download_blob')
def download_blob():
    azure_blob_file_downloader = AzureBlobFileDownloader()
    azure_blob_file_downloader.download_all_blobs_in_container()
    return jsonify({'html': 'Images Received'})


@app.route('/run_model')
def runModel():
    print('processing now!')
    # Image_Dect()
    customvision()
    return jsonify({'html': 'Process Completed'})


@app.route('/display_result')
def display_result():
    images = os.listdir('static/predicted')
    images = [file for file in images]
    data = []
    for image in images:
        temp = {}
        temp['file_name'] = image
        data.append(temp)

    return jsonify(data)


@app.route('/download')
def download_file():
    zipf = zipfile.ZipFile('predicted.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('static/predicted/'):
        for file in files:
            zipf.write('static/predicted/'+file)
    zipf.close()
    return send_file('predicted.zip',
                     mimetype='zip',
                     attachment_filename='predicted.zip',
                     as_attachment=True)


# upload to blob storage
@app.route("/model/", methods=['POST'])
def uplaodfile():
    uploaded_file = request.files['file']
    

    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename))
        image = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        print('upload begins here')
        
        azure_blob_file_uploader = AzureBlobFileUploader()
        azure_blob_file_uploader.upload_all_images_in_folder()

    return render_template(
        "model.html",
        img=image
    )



# uplaod file to upload folder & return saved file to display.
# @app.route("/model/", methods=['POST'])
# def uplaodfile():
#     uploaded_file = request.files['file']
#     print('lets upload ')
#     print(uploaded_file)

#     if uploaded_file.filename != '':
#         uploaded_file.save(os.path.join(
#             app.config['UPLOAD_FOLDER'], uploaded_file.filename))
#         image = os.path.join(
#             app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#     return render_template(
#         "model.html",
#         img=image
#     )


@app.route("/model/")
def model():
    return render_template("model.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6001)
