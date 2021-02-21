import boto3
import requests
import time
from datetime import datetime
from pytz import timezone
from replit import db
from utils import get_sha1
# The primary file name we're saving stuff as
file_name = 'TDTrackerMattZ.json'
# Source url that we will be polling from
url = 'https://mattz-cdn.geostyx.com/file/mattz-public/TDTrackerMattZ.json'
s3 = boto3.resource('s3',
                    endpoint_url='https://s3.us-west-002.backblazeb2.com')
bucket = s3.Bucket('mattz-history')

# DB keys so it's not hard coded strings everywhere
class KEY: 
    run_count = 'run_count'
    grab_file_hash = 'grab_file_hash'


# init db stuff if it's not there
if db.get(KEY.run_count) is None:
    db[KEY.run_count] = 0
if db.get(KEY.grab_file_hash) is None:
    db[KEY.grab_file_hash] = 'x'

db[KEY.run_count] = db[KEY.run_count] + 1
print('Starting main loop ({0})'.format(db[KEY.run_count]))

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

                # SAVE NEW VERSIONS TO B2 STORAGE
                sha1str = get_sha1(file_name)
                if sha1str != db[KEY.grab_file_hash]:  # It's new! Save it to B2!
                    print("SHA1: {0}".format(sha1str))
                    db[KEY.grab_file_hash] = sha1str
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
