from flask import Flask, request, render_template, redirect, url_for
from database import mysql as db
import logging

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def root():
    return render_template('home.html')


@app.route('/test')
def test_page():
    return render_template('demo.html')


@app.route('/update')
def update():
    jid = request.args.get('id')
    jname = request.args.get('name')
    if jid and jname:
        db.update_jname_by_id(jid, jname)
        return redirect('journal.html')

    return render_template('update.html')

@app.route('/delete')
def delete():
    jid = request.args.get('id')
    db.delete_journal_by_id(jid)
    return redirect('/journal.html')


@app.route('/recommend.html')
def recommend():
    return render_template('recommend.html')


@app.route('/journal.html')
def journal_page():
    journals = db.get_jid_name()
    return render_template('journal.html', data=journals)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG,  # lowest level to show in console
        filename="logs/logs.txt"
    )

