from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
import feedparser # Import feedparser
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

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

@app.route('/create-post')
def create_post():
    return render_template('create_post.html')

def get_posts():
    posts = []
    contents_dir = 'contents'
    if os.path.exists(contents_dir):
        for filename in os.listdir(contents_dir):
            if filename.endswith('.md'):
                with open(os.path.join(contents_dir, filename), 'r') as f:
                    content = f.read()
                    title = content.split('\n')[0].replace('# ', '')
                    body_preview = '\n'.join(content.split('\n')[1:])[:100] + '...'
                    posts.append({'title': title, 'content': body_preview, 'filename': filename})
    return posts

def get_post(filename):
    contents_dir = 'contents'
    filepath = os.path.join(contents_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            title = content.split('\n')[0].replace('# ', '')
            body = '\n'.join(content.split('\n')[1:])
            return {'title': title, 'content': body}
    return None

@app.route('/blog')
def blog():
    posts = get_posts()
    return render_template('blog.html', posts=posts)

@app.route('/post/<filename>')
def post(filename):
    post_data = get_post(filename)
    if post_data:
        return render_template('post.html', title=post_data['title'], content=post_data['content'])
    else:
        return "Post not found", 404

@app.route('/rss')
def rss_feed():
    # Using BBC News RSS feed as an example
    rss_url = "https://feeds.bbci.co.uk/news/rss.xml"
    try:
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
    except Exception as e:
        return f"Error fetching RSS feed: {e}", 500

@app.route('/submit-post', methods=['POST'])
def submit_post():
    title = request.form['title']
    content = request.form['content']

    github_token = os.environ.get('GITHUB_TOKEN')
    GITHUB_REPO_OWNER = os.environ.get('GITHUB_REPO_OWNER', 'inakimaldive')
    GITHUB_REPO_NAME = os.environ.get('GITHUB_REPO_NAME', 'computer-in-flask')
    workflow_id = os.environ.get('WORKFLOW_ID', 'create-post.yml')

    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/actions/workflows/{workflow_id}/dispatches"

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
    elif response.status_code == 401:
        return render_template('create_post.html', message="Error: Unauthorized. Please check your GitHub token."), 401
    elif response.status_code == 404:
        return render_template('create_post.html', message="Error: Repository or workflow not found."), 404
    else:
        return render_template('create_post.html', message=f"Failed to create post: {response.status_code} - {response.text}"), 500

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

def get_gemini_model():
    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_api_key:
        return None
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    model = get_gemini_model()
    if not model:
        return jsonify({'reply': 'Error: Gemini API key not found.'}), 500
    
    message = request.json['message']
    response = model.generate_content(message)
    
    return jsonify({'reply': response.text})

@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    model = get_gemini_model()
    if not model:
        return jsonify({'error': 'Gemini API key not found.'}), 500

    try:
        prompt = "Generate a random blog post title and content. The title should be short and catchy. The content should be a few paragraphs long."
        response = model.generate_content(prompt)
        
        # Assuming the response is in the format "Title: [title]\n\n[content]"
        parts = response.text.split('\n\n', 1)
        title = parts[0].replace('Title: ', '')
        content = parts[1]

        return jsonify({'title': title, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
