from os.path import basename

import cv2
import flask
from werkzeug.utils import secure_filename

from flask import Flask, request, jsonify
import os
import time
import uuid
import json
import py7zr
from pyunpack import Archive
import os
import random
import zipfile
from math import floor
import threading
import queue
import gc
import re
import openpyxl
from copy import deepcopy
import shutil
from functools import wraps
from werkzeug.exceptions import BadRequest
from moduletest import seggregator_new, converting_to_image_new, save_image_of_pdf_new
from PIL import Image
from reportlab.pdfgen import canvas

app = Flask(__name__)

def allowed_file_class(filename):
    # return '.' in filename and filename.rsplit('.', 1)[1].lower() in APP.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf','zip','jpg','png','tiff']
@app.route('/classifier', methods=['POST'])
def upload_pdf_moduletest():
    print('donme')
    all_pdf_output = {}
    random_id = str(uuid.uuid4())
    os.mkdir("listen" + '/' + random_id)
    fan = os.path.join("listen", random_id)
    MAIN_DIR = fan
    # for f in os.listdir(MAIN_DIR):
    #     print(os.path.join(APP.config['UPLOAD_FOLDER'], f))
    #     # os.remove(os.path.join(APP.config['UPLOAD_FOLDER'],f))
    #     try:
    #         shutil.rmtree(os.path.join(APP.config['UPLOAD_FOLDER'], f))
    #         print("% s removed successfully" % os.path.join(APP.config['UPLOAD_FOLDER'], f))
    #     except OSError as error:
    #         print(error)
    #         print("File path can not be removed")
    #     print("donme")
    BASE_IMGS_FOLDER = "imgsfolders"
    print('BASE_IMGS_FOLDER', BASE_IMGS_FOLDER)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file[]' not in request.files:
            return BadRequest("No File")
        # files = request.files['file[]']
        files = flask.request.files.getlist("file[]")
        print(files)
        print('file', files)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # print(files.filename,"gotit")
        hospital_id = request.form.get('hospital_id')
        print((hospital_id,"got hospital_id"))
        for file in files:
            if file.filename == '':
                # flash('No selected file')
                return BadRequest("No File")
            if not allowed_file_class(file.filename):
                return BadRequest("File Not Allowed")

            if file and allowed_file_class(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(MAIN_DIR, filename))

        token = 1
        while token:
            if 1:

                root_path = "./extract"
                hospital_identified = 'none'

                i = 0
                if ".zip" in filename.lower():
                    for filename in os.listdir(MAIN_DIR):
                        with zipfile.ZipFile(os.path.join(MAIN_DIR, filename), 'r') as zip_ref:
                            zip_ref.extractall(MAIN_DIR)
                            for root, dirs, files in os.walk(MAIN_DIR):
                                print(root, "root")
                                print(dirs, "dirs")
                                # for claim_key in dirs:
                                #     claim_key_actual = str(claim_key)
                                #     print(claim_key_actual,"here not deleted claimkey")
                                print(files, "files")
                                for file in files:
                                    print("gotin")

                                    src_file_path = os.path.join(root, file)
                                    dest_file_path = os.path.join(MAIN_DIR, file)

                                    try:
                                        if os.path.exists(dest_file_path):
                                            os.remove(dest_file_path)

                                        # Using shutil.move() for more robustness
                                        shutil.move(src_file_path, dest_file_path)

                                        print(file, "check")

                                    except PermissionError as e:
                                        print(f"Permission error: {e}. Retrying...")
                                        time.sleep(2)  # wait for 2 seconds before ret

                        os.remove(os.path.join(MAIN_DIR, filename))
                elif ".pdf" in filename.lower():
                    pass
                elif ".jpg" in filename.lower() or ".png" in filename.lower() or ".tiff" in filename.lower():
                    pass
                print(os.listdir(MAIN_DIR), "pdf_catch")
                items = os.listdir(MAIN_DIR)
                directories = [item for item in items if os.path.isdir(os.path.join(MAIN_DIR, item))]

                if directories:
                    print(f"The following directories exist in '{MAIN_DIR}':")
                    for directory in directories:
                        print(directory)
                        directory_path = os.path.join(MAIN_DIR, directory)
                        print(directory_path, "okayfinally")
                        shutil.rmtree(directory_path)

                else:
                    print(f"No directories found in '{MAIN_DIR}'.")

                for filename in os.listdir(MAIN_DIR):
                    # if (".pdf") not in filename.lower():
                    #     os.remove(os.path.join(MAIN_DIR, filename))
                    print(filename)
                    eachfilepath = os.path.join(MAIN_DIR, filename)
                    random_id = str(uuid.uuid4())
                    os.mkdir(BASE_IMGS_FOLDER + '/' + random_id)
                    folder = BASE_IMGS_FOLDER + '/' + random_id
                    save_path = folder

                    main1_file = filename
                    print(main1_file)
                    print(main1_file)
                    # new_directory = "" + str(main1_file) + ""
                    # parent_dire = r"Extracted_Images"
                    # main_path = os.path.join(parent_dire, new_directory)
                    # exists_check = os.path.isdir("Extracted_Images/" + str(main1_file) + "")
                    # print(exists_check)
                    # if exists_check == True:
                    #     print("Main file Alreaddy Exists")
                    # else:
                    #
                    #     os.mkdir(main_path)
                    #     print("filecreated")
                    # print(claim_key_actual,"here not deleted claimkey")


                    if (".pdf") in filename.lower():
                        converting_to_image_new(eachfilepath, save_path, folder)
                        output = seggregator_new(save_path, random_id, MAIN_DIR, filename,
                                             main1_file,
                                             hospital_id)

                        all_pdf_output[filename] = output
                        # os.remove(MAIN_DIR)
                        print("done")
                    elif((".jpg") in filename.lower() or (".png") in filename.lower() or (".jpeg") in filename.lower()
                    or (".JPEG") in filename.lower()):
                        image = cv2.imread(os.path.join(MAIN_DIR,filename))
                        if image is None:
                            print(f"Could not read the image: {os.path.join(MAIN_DIR,filename)}")
                            return

                        output_path = os.path.join(save_path,
                                                   random_id + "1"  + '.jpg')
                        cv2.imwrite(output_path, image)
                        print(image,"check")
                        print("enterdatatttttt")
                        length_of_files_present = 0
                        # change_resolution(
                        #     os.path.join(save_path, random_id + "1"  + '.jpg'),
                        #     os.path.join(save_path, random_id + "1"  + '.jpg'),
                        #     2300, 2700)

                        output = seggregator_new(save_path, random_id, MAIN_DIR, filename,
                                             main1_file,
                                             hospital_id
                                            )

                        all_pdf_output[filename] = output
                    elif ((".tiff") in filename.lower() or (".tif") in filename.lower()):
                        image = os.path.join(MAIN_DIR, filename)
                        if image is None:
                            print(f"Could not read the image: {os.path.join(MAIN_DIR, filename)}")
                            return

                        output_path = os.path.join(save_path,
                                                   random_id + "1" + '.jpg')
                        try:
                            img = Image.open(image)

                            # Save as JPG
                            img.save(output_path, "JPEG")

                            print(f"Conversion successful. Saved as {output_path}")
                        except Exception as e:
                            print(f"Error converting the file: {e}")
                        print(image, "check")
                        print("enterdatatttttt")
                        length_of_files_present = 0
                        # change_resolution(
                        #     os.path.join(save_path, random_id + "1" + '.jpg'),
                        #     os.path.join(save_path, random_id + "1" + '.jpg'),
                        #     2300, 2700)

                        output = seggregator_new(save_path, random_id, MAIN_DIR, filename,
                                             main1_file,
                                             hospital_id)

                        all_pdf_output[filename] = output

                print(all_pdf_output, "asdfghjkl")
                for f in os.listdir(MAIN_DIR):
                    print(os.path.join(MAIN_DIR, f))
                    # os.remove(os.path.join(APP.config['UPLOAD_FOLDER'],f))
                    try:
                        shutil.rmtree(MAIN_DIR)
                        print("% s removed successfully" % MAIN_DIR)
                    except OSError as error:
                        print(error)
                        print("File path can not be removed")
                    print("donme")
                token = 0
            return jsonify(all_pdf_output)


if __name__ == '__main__':
    app.run(debug=True , use_reloader=False)