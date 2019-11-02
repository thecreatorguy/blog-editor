from flask import Flask, render_template, request, redirect, url_for
import requests as api
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
API_ROUTE = 'http://localhost/api/article'

@app.route('/')
def index():
    articles = api.get(API_ROUTE, auth=_auth()).json()
    articles.sort(key=lambda article: (article['release_at'] or '9', article['updated_at']), reverse=True)
    return render_template('index.html', articles=articles)

@app.route('/new')
def new():
    return render_template('editor.html')

@app.route('/edit/<int:id>')
def edit(id):
    article = api.get(API_ROUTE + '/' + str(id), auth=_auth()).json()
    return render_template('editor.html', article=article)

@app.route('/save', methods=['POST'])
def save():
    if not request.form['id']:
        api.post(API_ROUTE, auth=_auth(), json=request.form)
    else:
        api.put(API_ROUTE + '/' + str(request.form['id']), auth=_auth(), json=request.form)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    api.delete(API_ROUTE + '/' + str(id), auth=_auth())
    return redirect(url_for('index'), code=278)

def _auth():
    with open('api-auth.txt', 'r') as f:
        return HTTPBasicAuth(f.readline(), f.readline())
