
from datetime import date
import io
import zipfile
import requests
import os
import json
import time

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    sched = BackgroundScheduler(daemon=True)
    # sched.add_job(fetchCSV, 'cron', minute='*')
    sched.add_job(fetchCSV, 'cron', hour='12', minute='30',
                  day_of_week='mon-fri')  # UTC to IST
    sched.start()


def fetchCSV():
    from . import models
    # conn = redis.Redis(host='localhost', port=6379, db=0)

    today = date.today().strftime("%d%m%Y")
    url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ" + \
        today[0:4] + today[6:] + "_CSV.ZIP"
    # url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ090221_CSV.ZIP"
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    print('Fetched')
    # csv_file_url = 'EQ090221.CSV'
    csv_file_url = "EQ" + today[0:4] + today[6:] + ".CSV"
    csv_file = open(csv_file_url)
    csv_file_text = csv_file.read()
    csv_file.close()

    csv_file_lines = csv_file_text.split("\n")[1:]
    models.Stock.objects.all().delete()
    for row_text in csv_file_lines:
        if not row_text:
            break
        row = row_text.split(",")
        stock = models.Stock(
            code=row[0], name=row[1].strip(), open=row[4], high=row[5], low=row[6], close=row[7])
        stock.save()
    os.remove("EQ" + today[0:4] + today[6:] + ".CSV")

    return
