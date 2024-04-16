import os
import logging
from pathlib import Path
from flask import Flask, url_for
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

# Setup logging with gunicorn
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


app.add_url_rule(
    f'{app.config["UPLOAD_DIR"]}/<path:filename>',
    endpoint='images', view_func=app.send_static_file)


# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Set up login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Import views (assuming views are defined in a separate file using Blueprints)
from .views import views_blueprint
from .auth import auth_blueprint

# Register Blueprints
app.register_blueprint(views_blueprint)
app.register_blueprint(auth_blueprint)

# Create database tables
from .models import Invite, User
with app.app_context():
    db.create_all()
    if not Path(app.config['UPLOAD_DIR']).exists():
        (Path(app.config['UPLOAD_DIR'])).mkdir(parents=True)
    # Check if we need to create an invite
    if not (User.query.all() and Invite.query.all()):
        invite = Invite(user_limit=1)
        db.session.add(invite)
        db.session.commit()
        app.logger.info(f'Created invite with the id {invite.id}')



