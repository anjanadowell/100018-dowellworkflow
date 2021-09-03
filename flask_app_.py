
# A very simple Flask Hello World app for you to get started with...

from flask import Flask , render_template

app = Flask(__name__, template_folder="/home/dowellproject/mysite/static")

@app.route('/eSignature')
def signs():
    return render_template('sign.html')
