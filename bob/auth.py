"""Authentication end points."""
from datetime import datetime, timedelta

from flask import abort, flash, redirect, render_template, request, url_for, Blueprint, current_app
from flask_login import current_user, login_required, login_user, logout_user

from bob import db, login_manager
from bob.models import User, Invite

auth_blueprint = Blueprint('auth', __name__)

@login_manager.request_loader
def load_user_from_header(request):
    auth = request.authorization
    if not auth:
        # no basic auth provided, continue with normal auth
        return None

    user = User.query.filter_by(name=auth.username).first()
    if not user or not user.check_password(auth.password):
        # wrong basic auth provided deny access
        abort(401)

    # basic auth works
    return user


@login_manager.user_loader
def load_user(user_id):
    """Load a user by id."""
    return User.query.filter_by(id=user_id).first()


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Log in the user."""
    if current_user.is_authenticated:
        return redirect(url_for("views.display_map"))
    if request.method == "POST":
        user = User.query.filter_by(name=request.form.get("username")).first()
        if user is None or not user.check_password(request.form.get("password")):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))

        login_user(user)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("views.display_map")
        return redirect(next_page)
    else:
        return render_template("login.html")


@auth_blueprint.route("/logout")
def logout():
    """Log out the user."""
    logout_user()

    return redirect(url_for("views.display_map"))


@auth_blueprint.route("/register/<string:invite_id>", methods=["GET", "POST"])
def register(invite_id):
    if current_user.is_authenticated:
        return redirect(url_for("views.display_map"))
    invite = Invite.query.get(invite_id)
    if not invite:
        return abort(404) # Unavailable
    if not invite.is_valid():
        return abort(410) # GONE TODO: make a nice page
    if request.method == "GET":
        return render_template("register.html", invite=invite)

    username = request.form["username"]
    password = request.form["password"]

    if not (username and password):
        return abort(400)
    user = User(name=username, invited_by_id= invite.user_id)
    user.set_password(password)
    invite.remaining_invites -= 1
    db.session.add(user)
    db.session.add(invite)
    db.session.commit()
    current_app.logger.info(f"create user {username} with id {user.id}")
    return redirect(url_for("auth.login"))

@login_required
@auth_blueprint.route("/invite")
def invite():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    # create an Invite for one user
    invite = Invite(
        user_id = current_user.id,
        remaining_invites = 1,
        exp_date = datetime.now() + timedelta(minutes=15)
    )
    db.session.add(invite)
    db.session.commit()

    return render_template("invite.html", invite=invite)

