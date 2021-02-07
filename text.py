import datetime
import os
import urllib.request
import zipfile
import redis
import json


def fetch_and_store_bhavcopy():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    conn = redis.Redis(host='localhost', port=6379, db=0)

    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(1)

    if yesterday.weekday() in [5, 6]:
        # Weekends holidays
        print("Returning because yesterday is a weekend")
        return

    year = str(yesterday.year)[2:]
    month = yesterday.month
    if month < 10:
        month = "0%s" % month
    day = yesterday.day
    if day < 10:
        day = "0%s" % day

    url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ050221_CSV.ZIP"

    # Fetch file
    downloaded_zip_files_location = os.path.join(BASE_DIR, "bhavcopy_zip")
    if not os.path.isdir(downloaded_zip_files_location):
        os.mkdir(downloaded_zip_files_location)
    file_name = "EQ%s%s%s_CSV.ZIP" % (day, month, year)
    file_url = os.path.join(downloaded_zip_files_location, file_name)
    try:
        urllib.request.urlretrieve(url, file_url)
    except Exception as e:
        # File doesnt exist either due to wrong url or holiday
        print(e)
        print("Returning because yesterday is either a holiday or wrong url")
        return

    # Extract file from zip
    csv_files_location = os.path.join(BASE_DIR, "bhavcopy_csv")
    if not os.path.isdir(csv_files_location):
        os.mkdir(csv_files_location)

    zip_ref = zipfile.ZipFile(file_url, 'r')
    zip_ref.extractall(csv_files_location)
    zip_ref.close()

    # Read csv file and store
    csv_file_url = os.path.join(
        csv_files_location, "EQ%s%s%s.CSV" % (day, month, year))
    csv_file = open(csv_file_url)
    csv_file_text = csv_file.read()
    csv_file.close()

    csv_file_lines = csv_file_text.split("\n")[1:]
    data = {}
    for row_text in csv_file_lines:
        if not row_text:
            break
        row = row_text.split(",")

        code = row[0]
        name = row[1]
        _open = row[4]
        high = row[5]
        low = row[6]
        close = row[7]
        data[code] = {
            'code': code,
            'name': name,
            'open': _open,
            'high': high,
            'low': low,
            'close': close
        }
    key = "equity-bhavcopy-%s%s%s" % (day, month, year)
    conn.set(key, json.dumps(data))


fetch_and_store_bhavcopy()
