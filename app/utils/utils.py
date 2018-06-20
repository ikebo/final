import datetime
import hashlib
import os
import uuid

from flask import url_for

from app import app
from app.utils.subject import Subject


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def get_fileRoute(filename):
    file = str(uuid.uuid4()) + '.' + filename.rsplit('.',1)[1].lower()
    folder = os.path.join(app.config['UPLOAD_FOLDER'],get_current_date())
    if not os.path.exists(folder):
        os.mkdir(folder)
    return os.path.join(folder,file)


def generate_subject(name,scores):
    ss = []
    for s in scores:
        ss.append(s[0])
    count = len(ss)
    maxScore = max(ss)
    minScore = min(ss)
    avgScore = round(sum(ss)/count,2)
    subject = Subject(name,count,maxScore,minScore,avgScore)
    return subject


def generate_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode(encoding='utf-8'))
    return md5.hexdigest()
