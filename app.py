from flask import Flask, request, render_template, redirect, url_for
from database import mysql as db
import utils.config as config
from utils.errors import *
import logging
import logging.handlers
import os
import service.user_service as Users
import service.session_service as Sessions
import service.article_service as Articles


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    search_method = request.args.get('type')
    if keyword:
        if search_method == 'advanced':
            results = Articles.full_search(keyword)
        elif search_method == 'intelligent':
            results = Articles.lemma_search(keyword)
        else:
            results = Articles.title_search(keyword)
    else:
        results = Articles.list()
    #  return render_template('home.html', data=results)
    return render_template('journal.html', data=results)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        passwd = request.form['passwd']
        try:
            user = Users.login_user(username, passwd)
            response = redirect(url_for('journal_page'))
            session = Sessions.new(user)
            response.set_cookie('session', session.key)
            return response
        except LoginError as err:
            return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        passwd = request.form['passwd']
        try:
            user = Users.signup_user(username, passwd)
        except UserExistsError:
            return redirect(url_for('login'))
        if not user:
            raise ValueError("Unsuccessful New User Create")
        response = redirect(url_for('login'))
        return response
    else:
        return render_template('signup')


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
logger.info('\n\n====== Application started ======\n')

#  import inspect
#  frame_info = inspect.stack()[1]
#  logger.info('by ' + frame_info.filename)



if __name__ == '__main__':
    # Run app
    app.run(host='0.0.0.0')
