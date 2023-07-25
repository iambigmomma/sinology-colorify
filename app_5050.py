# import the necessary packages
import os
import sys
import requests
import ssl
from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask import send_file
import boto3
from botocore.client import Config


from app_utils import download
from app_utils import generate_random_filename
from app_utils import clean_me
from app_utils import clean_all
from app_utils import create_directory
from app_utils import get_model_bin
from app_utils import convertToJPG

from os import path
import torch

import fastai
from deoldify.visualize import *
from pathlib import Path
import traceback


torch.backends.cudnn.benchmark=True


os.environ['CUDA_VISIBLE_DEVICES']='0'

app = Flask(__name__)

def upload_image(upload_file_path, bucket, destination):
    client.upload_file(upload_file_path, bucket, destination)

# define a predict function as an endpoint
@app.route("/process", methods=["POST"])
def process_image():

    input_path = generate_random_filename(upload_directory,"jpeg")
    output_path = os.path.join(results_img_directory, os.path.basename(input_path))

    try:
        url = request.json["source_url"]
        render_factor = int(request.json["render_factor"])

        download(url, input_path)

        try:
            image_colorizer.plot_transformed_image(path=input_path, figsize=(20,20),
                render_factor=render_factor, display_render_factor=True, compare=False)
        except:
            convertToJPG(input_path)
            image_colorizer.plot_transformed_image(path=input_path, figsize=(20,20),
            render_factor=render_factor, display_render_factor=True, compare=False)

        callback = send_file(output_path, mimetype='image/jpeg')
        
        return callback, 200

    except:
        traceback.print_exc()
        return {'message': 'input error'}, 400

    finally:
        pass
        clean_all([
            input_path,
            output_path
            ])


if __name__ == '__main__':
    global upload_directory
    global results_img_directory
    global image_colorizer

    upload_directory = '/data/upload/'
    create_directory(upload_directory)

    results_img_directory = '/data/result_images/'
    create_directory(results_img_directory)

    model_directory = '/data/models/'
    create_directory(model_directory)
    
    artistic_model_url = 'https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth'
    get_model_bin(artistic_model_url, os.path.join(model_directory, 'ColorizeArtistic_gen.pth'))


    image_colorizer = get_image_colorizer(artistic=True)
    image_colorizer.results_dir = Path(results_img_directory)
    session = boto3.session.Session()
    client = session.client('s3',
                        region_name='fra1',
                        endpoint_url='https://fra1.digitaloceanspaces.com',
                        aws_access_key_id='DO0072ARKH2U8T7T2EFY',
                        aws_secret_access_key='t6Oxyd6CQrbRI+pA8a9Z1uElt3PIqKPG+DCQuP08b7A')
    
    port = 5050
    host = '0.0.0.0'

    app.run(host=host, port=port, threaded=False)

