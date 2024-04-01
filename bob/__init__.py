import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://username:password@localhost/databasename')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_DIR'] = os.environ.get(
    'UPLOAD_DIR', '/images'
)

app.add_url_rule(
    f'{app.config["UPLOAD_DIR"]}/<path:filename>',
    endpoint='images', view_func=app.send_static_file)


# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import views (assuming views are defined in a separate file using Blueprints)
from .views import views_blueprint

# Register Blueprints
app.register_blueprint(views_blueprint)

# Create database tables
with app.app_context():
    db.create_all()
    if not Path(app.config['UPLOAD_DIR']).exists():
        (Path(app.config['UPLOAD_DIR'])).mkdir(parents=True)

# Set up login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401