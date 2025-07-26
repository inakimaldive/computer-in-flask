from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import feedparser # Import feedparser

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/about')
def about():
    return 'About'

@app.route('/time')
def get_time():
    from datetime import datetime
    return f"<div>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>"

@app.route('/time-page')
def time_page():
    return render_template('time.html')

@app.route('/create-post')
def create_post():
    return render_template('create_post.html')

@app.route('/blog')
def blog():
    posts = []
    contents_dir = 'contents'
    if os.path.exists(contents_dir):
        for filename in os.listdir(contents_dir):
            if filename.endswith('.md'):
                with open(os.path.join(contents_dir, filename), 'r') as f:
                    content = f.read()
                    title = content.split('\n')[0].replace('# ', '')
                    body = '\n'.join(content.split('\n')[1:])
                    posts.append({'title': title, 'content': body})
    return render_template('blog.html', posts=posts)

@app.route('/rss')
def rss_feed():
    # Using BBC News RSS feed as an example
    rss_url = "https://feeds.bbci.co.uk/news/rss.xml"
    feed = feedparser.parse(rss_url)
    
    feed_items = []
    for entry in feed.entries:
        feed_items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
        })
    
    return render_template('rss.html', feed_items=feed_items)

@app.route('/submit-post', methods=['POST'])
def submit_post():
    title = request.form['title']
    content = request.form['content']

    github_token = os.environ.get('GITHUB_TOKEN')
    repo_owner = "inakimaldive"
    repo_name = "computer-in-flask"
    workflow_id = "create-post.yml"

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_id}/dispatches"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}"
    }

    data = {
        "ref": "main",
        "inputs": {
            "title": title,
            "content": content
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        return render_template('create_post.html', message="Post created successfully! Your post is being processed.")
    else:
        return render_template('create_post.html', message=f"Failed to create post: {response.status_code} - {response.text}"), 500
