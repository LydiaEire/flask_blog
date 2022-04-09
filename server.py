import datetime

import requests as requests
from flask import Flask, render_template, request

from post import Post

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

posts = requests.get('https://api.npoint.io/9ec6fac4764e429e0f8b').json()
post_objects = []
for post in posts:
    post_obj = Post(post['id'], post['title'], post['subtitle'], post['body'])
    post_objects.append(post_obj)


@app.route('/')
def home():
    current_year = datetime.datetime.now().year
    return render_template('index.html', all_posts=post_objects, years=current_year)


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)


@app.route('/about')
def about_me():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact_me():
    if request.method == 'POST':
        data = request.form
        print(data['name'])
        print(data['email'])
        print(data['phone'])
        print(data['message'])
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)
