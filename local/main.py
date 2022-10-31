from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def upload_image():
    return render_template('index.html')

#def hello():
#    return 'Hello, World!'

if __name__ == '__main__':
    import os
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
