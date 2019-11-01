from flask import Flask, request, render_template, redirect, url_for
from database import mysql as db
import utils.config as config
import logging
import logging.handlers
import os

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def root():
    return render_template('home.html')


@app.route('/test')
def test_page():
    return render_template('demo.html')


@app.route('/update.html')
def update_page():
    jid = request.args.get('id')
    jname = db.get_jname_by_id(jid)
    return render_template('update.html', old_name=jname['journal_name'])


@app.route('/update')
def update():
    jid = request.args.get('id')
    jname = request.args.get('name')
    if jid and jname:
        db.update_jname_by_id(jid, jname)
        return redirect('journal.html')
    else:
        redirect('/update.html')


@app.route('/delete')
def delete():
    jid = request.args.get('id')
    db.delete_journal_by_id(jid)
    return redirect('/journal.html')


@app.route('/insert')
def insert():
    jname = request.args.get('jname')
    db.insert_journal_name(jname)
    return redirect('journal.html')


@app.route('/recommend.html')
def recommend():
    return render_template('recommend.html')


@app.route('/journal.html')
def journal_page():
    keyword = request.args.get('keyword')
    if keyword:
        journals = db.search_journal_by_name(keyword)
    else:
        journals = db.get_jid_name()
    return render_template('journal.html', data=journals)


if __name__ == '__main__':
    # Set up logging
    os.makedirs(config.LOG_DIR, exist_ok=True)
    logger = logging.getLogger("app")
    logger.setLevel(config.LOG_LEVEL)
    formatter = logging.Formatter(**config.LOG_FORMAT)
    file_handler = logging.handlers.RotatingFileHandler(config.LOG_FILE,
                                                        maxBytes=config.LOG_SIZE,
                                                        backupCount=config.LOG_CNT)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.info("\n\n-------------------- start -----------------------\n")

    # Run app
    app.run(host='0.0.0.0')
