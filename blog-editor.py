"""
My blog editor flask application.
"""
from flask import Flask, render_template, request, redirect, url_for
import requests
from requests.auth import HTTPBasicAuth
import base64
import os

app = Flask(__name__)
HOST = os.getenv('HOST')
HEADERS = {'X-Api-Key': os.getenv('API_KEY')}

@app.route('/')
def index():
    """Gets the webpage with all articles"""
    r = requests.get(HOST + '/api/articles', headers=HEADERS)
    if r.status_code != requests.codes.ok:
        return r.text, r.status_code

    articles = r.json()
    return render_template('index.html', articles=articles)

@app.route('/new')
def new():
    """New article form"""
    return render_template('editor.html')

@app.route('/edit/<int:article_id>')
def edit(article_id):
    """Edit existing article form"""
    r = requests.get(HOST + '/api/articles', headers=HEADERS)
    if r.status_code != requests.codes.ok:
        return r.text, r.status_code

    return render_template('editor.html', article=r.json()[article_id])

@app.route('/save', methods=['POST'])
def save():
    """Save new or existing article"""
    form_data = request.form.to_dict()
    if (form_data['release-at'] == 'Never'):
        form_data['release-at'] = None

    r = requests.post(HOST + '/api/articles', headers=HEADERS, json=form_data)
    if r.status_code != requests.codes.created:
        return r.text, r.status_code

    return redirect(url_for('index'), code=278)

@app.route('/delete/<int:article_id>', methods=['DELETE'])
def delete(article_id):
    """Delete an existing article"""
    r = requests.delete(HOST + '/' + str(article_id), headers=HEADERS)
    if r.status_code != requests.codes.no_content:
        return r.text, r.status_code
    return redirect(url_for('index'), code=278)

if __name__ == '__main__':
    app.run(host='0.0.0.0')