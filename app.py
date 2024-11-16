from flask import Flask, render_template, redirect, url_for, request
from forms import UserProfileForm, PostForm
from database import Database
from models import db, User, Post

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fdfhghgfhfd'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = Database(app)

with app.app_context():
    database.create_all_tables()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserProfileForm()
    if form.validate_on_submit():
        username = form.username.data
        image = form.profile_picture.data

        check_user = database.get_user_by_username(username)

        if check_user:
            return redirect(url_for('profile', username=check_user.username))

        new_user = database.create_user(username, image)

        if new_user:
            return redirect(url_for('profile', username=new_user.username))

    return render_template('form.html', form=form)

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    user = database.get_user_by_username(username)
    if not user:
        return redirect(url_for('home'))

    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        text = post_form.text.data
        image = post_form.image.data
        new_post = database.create_post(title, text, image, user.id)
        
        if new_post:
            return redirect(url_for('profile', username=user.username))

    page = request.args.get('page', 1, type=int)
    per_page = 10

    posts_paginated = database.get_posts_by_user(user.id, page=page, per_page=per_page)

    return render_template('profile.html', user=user, posts=posts_paginated.items, pagination=posts_paginated, post_form=post_form)

@app.route('/success/<username>')
def success(username):
    user = database.get_user_by_username(username)
    if user:
        return f'User {user.username} has been registered with profile picture at {user.profile_picture}'
    return 'User not found!'

if __name__ == '__main__':
    app.run(debug=True)

