from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def root():
    return render_template('home.html')


@app.route('/test')
def test():
    return render_template('search_result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
