"""
My blog editor flask application.
"""
from flask import Flask, render_template, request, redirect, url_for
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
API_ROUTE = 'http://localhost/api/article'

@app.route('/')
def index():
    """Gets the webpage with all articles"""
    r = requests.get(API_ROUTE, auth=_auth())
    if r.status_code != requests.codes.ok:
        return r.text, r.status_code

    articles = sorted(r.json(), key=lambda article: (article['release_at'] or '9', article['updated_at']), reverse=True)
    return render_template('index.html', articles=articles)

@app.route('/new')
def new():
    """New article form"""
    return render_template('editor.html')

@app.route('/edit/<int:id>')
def edit(id):
    """Edit existing article form"""
    r = requests.get(API_ROUTE + '/' + str(id), auth=_auth())
    if r.status_code != requests.codes.ok:
        return r.text, r.status_code

    return render_template('editor.html', article=r.json())

@app.route('/save', methods=['POST'])
def save():
    """Save new or existing article"""
    form_data = request.form.to_dict()
    if (form_data['release-at'] == 'Never'):
        form_data['release-at'] = None

    if not 'id' in form_data:
        r = requests.post(API_ROUTE, auth=_auth(), json=form_data)
        if r.status_code != requests.codes.created:
            return r.text, r.status_code
    else:
        r = requests.put(API_ROUTE + '/' + str(request.form['id']), auth=_auth(), json=form_data)
        if r.status_code != requests.codes.ok:
            return r.text, r.status_code

    return redirect(url_for('index'), code=278)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    """Delete an existing article"""
    r = requests.delete(API_ROUTE + '/' + str(id), auth=_auth())
    if r.status_code != requests.codes.no_content:
        return r.text, r.status_code
    return redirect(url_for('index'), code=278)

def _auth():
    """Retrieve username and password from hidden file and construct auth object"""
    with open('api-credentials.txt', 'r') as f:
        lines = f.read().splitlines()
        return HTTPBasicAuth(lines[0], lines[1])
