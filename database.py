import os
from werkzeug.utils import secure_filename
from models import db, User, Post

class Database:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        db.init_app(app)
        if not os.path.exists(os.path.join('static', app.config['UPLOAD_FOLDER'])):
            os.makedirs(os.path.join('static', app.config['UPLOAD_FOLDER']))

    def create_user(self, username, image):
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join('uploads', filename)
            image.save(os.path.join('static', image_path))

            new_user = User(username=username, profile_picture=image_path)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        return None

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create_post(self, title, text, image, user_id):
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join('uploads', filename)
            image.save(os.path.join('static', image_path))

            new_post = Post(title=title, text=text, image=image_path, user_id=user_id)
            db.session.add(new_post)
            db.session.commit()
            return new_post
        return None

    def get_posts_by_user(self, user_id, page=1, per_page=10):
        return Post.query.filter_by(user_id=user_id)\
            .paginate(page=page, per_page=per_page, error_out=False)

    def create_all_tables(self):
        with db.session.begin():
            db.create_all()

