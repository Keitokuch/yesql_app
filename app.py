from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/hello')
def hello():
    name = request.args.get('name','')
    return 'Hello ' + name + '!'

@app.route('/test')
def test():
    return render_template('search_result.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
