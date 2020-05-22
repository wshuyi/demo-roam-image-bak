#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re
from pathlib import Path
import datetime
import requests
import shutil
import json

def str_formatted_current_time():
    current_time = datetime.datetime.now()
    date_format = '%Y-%m-%d-%H-%M-%S-%f'
    timestr = current_time.strftime(date_format)
    return timestr

def download_firebase_img(remote_img, image_storage_dir, firebase_local_records):
    if remote_img not in firebase_local_records: #not downloaded
        current_time_str = str_formatted_current_time()
        download_image_filename = image_storage_dir/f"{current_time_str}.png"
        r = requests.get(remote_img, stream=True)
        with open(download_image_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        firebase_local_records[remote_img] = str(download_image_filename)
    else:
        print("Already downloaded!")


if len(sys.argv) < 3:
    print("usage: python roam_image_backup.py [your-roam-json-file] [image-storage-dir]")
    exit()

myjson = Path(sys.argv[1]).expanduser().resolve()
image_storage_dir = Path(sys.argv[2]).expanduser().resolve()

if not image_storage_dir.exists():
    image_storage_dir.mkdir()

firebase_download_record_json = image_storage_dir/"firebase_local_records.json"

with open(myjson) as f:
    data = f.read()

# get all remote images link

def get_image_links(data):
    return list(re.findall(r'\!\[.*?\]\((.*?)\)', data))

image_links  = get_image_links(data)


# get google fire base storage images

googlefirebaseimages = []
for image_link in image_links:
    if image_link.find("firebasestorage")>0:
        googlefirebaseimages.append(image_link)



# download firebase storage images to local

if firebase_download_record_json.exists():
    with open(firebase_download_record_json) as f:
        firebase_local_records = json.load(f)
else:
    firebase_local_records = {}

for remote_img in googlefirebaseimages:
    download_firebase_img(remote_img, image_storage_dir, firebase_local_records)

with open(firebase_download_record_json, 'w') as f:
    json.dump(firebase_local_records, f)

