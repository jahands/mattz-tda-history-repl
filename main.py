import boto3
import requests
import time
from datetime import datetime
from pytz import timezone
import hashlib
from replit import db
# The primary file name we're saving stuff as
file_name = 'TDTrackerMattZ.json'
# Source url that we will be polling from
url = 'https://mattz-cdn.geostyx.com/file/mattz-public/TDTrackerMattZ.json'
s3 = boto3.resource('s3',
                    endpoint_url='https://s3.us-west-002.backblazeb2.com')
bucket = s3.Bucket('mattz-history')
if db.get('run_count') is None:
  db['run_count'] = 0
db['run_count'] = db['run_count'] + 1
print('Starting main loop ({0})'.format(db['run_count']))
# MAIN LOOP TO UPDATE FILE
while True:
    # Skip weekends
    dt = datetime.utcnow()
    isWeekend = (datetime.now(timezone('US/Eastern')).isoweekday() >= 6)
    if not isWeekend:
        # DOWNLOAD THE FILE
        try:
            r = requests.get(url)
            if r.ok:
                with open(file_name, 'wb') as outfile:
                    outfile.write(r.content)
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

                # SAVE NEW VERSIONS TO B2 STORAGE
                sha1str = sha1.hexdigest()  # This seems to give the string
                if sha1str != db['grab_file_hash']:  # It's new! Save it to B2!
                    print("SHA1: {0}".format(sha1str))
                    db['grab_file_hash'] = sha1str
                    # Upload new version to b2
                    destination_path = 'TDTrackerMattZ/{0}_{1}'.format(
                        date_time_path, file_name)
                    try:
                        bucket.upload_file(Filename=file_name,
                                           Key=destination_path)
                    except:
                        print(
                            'FAILED TO UPLOAD, OH WELL BETTER LUCK NEXT TIME!')
        except:
            print('general error')
        time.sleep(12)  # check every 12 seconds
