from flask import Flask, request, render_template
import logging

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def root():
    return render_template('home.html')


@app.route('/test')
def test():
    return render_template('demo.html')


@app.route('/update.html')
def update_page():
    return render_template('update.html')


@app.route('/update')
def update():
    name = request.args.get('update_name')


@app.route('/recommend.html')
def recommend():
    return render_template('recommend.html')


@app.route('/journal.html')
def toJournal():
    return render_template('journal.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG,  # lowest level to show in console
        filename="logs/logs.txt"
    )

