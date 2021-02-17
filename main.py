import boto3
import requests
import time
from datetime import datetime
import hashlib
from replit import db

# The primary file name we're saving stuff as
file_name = 'TDTrackerMattZ.json'
# Source url that we will be polling from
url = 'https://f000.backblazeb2.com/file/mattz-public/TDTrackerMattZ.json'
s3 = boto3.resource('s3',
                    endpoint_url='https://s3.us-west-002.backblazeb2.com')
bucket = s3.Bucket('mattz-history')

# MAIN LOOP TO UPDATE FILE
while True:
    # DOWNLOAD THE FILE
    r = requests.get(url)
    with open(file_name, 'wb') as outfile:
        outfile.write(r.content)
    dt = datetime.utcnow()
    date_time_path = dt.strftime('%Y/%m/%d/%H/%Y-%m-%dT%H-%M-%S')
    # 2021/02/17/02/2021-02-17T02-01-09

    # GET THE HASH
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha1 = hashlib.sha1()
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    sha1str = sha1.hexdigest() # This seems to give the string
    if sha1str != db['grab_file_hash']:  # It's new! Save it to B2!
        print("SHA1: {0}".format(sha1str))
        db['grab_file_hash'] = sha1str
        # Upload new version to b2
        with open(file_name, 'rb') as file:
            destination_path = 'TDTrackerMattZ/{0}_{1}'.format(
                date_time_path, file_name)
            bucket.put_object(Key=destination_path, Body=file)

    time.sleep(12)  # check every 12 seconds
