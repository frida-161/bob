from pathlib import Path
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
    abort
)
from bob.models import Location
from bob import db, app
import uuid
import magic
import flask_login

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/add_location', methods=['POST'])
def add_location():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    comment = request.form['comment']
    photo = request.files['photo']

    ufilename = None
    if photo.filename:
        if(magic.from_buffer(photo.stream.read(1024), mime=True).startswith("image")):
            ufilename = str(uuid.uuid4())
            photo.stream.seek(0)
            photo.save(str(Path(app.config['UPLOAD_DIR']) / ufilename))
        else:
            return abort(415)
    new_location = Location(
        latitude=latitude, longitude=longitude,
        photo=ufilename)

    db.session.add(new_location)
    db.session.commit()


    return redirect(url_for('views.display_map'))


@views_blueprint.route('/upload_location')
def upload_location():
    return render_template('upload_location.html')


@views_blueprint.route('/display_map')
@views_blueprint.route('/')
def display_map():
    locations = Location.query.all()
    return render_template('display_map.html', locations=locations)


@views_blueprint.route('/location/<int:id>')
def get_location(id):
    location = Location.query.get(id)
    if not location:
        return abort(404)
    return render_template('location_detail.html', location=location)


@views_blueprint.route('/api/locations')
def get_locations():

    locations = Location.query.all()
    location_data = [
        {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "comment": location.comment,
            "link": url_for("views.get_location", id = location.id)
        } for location in locations]
    return jsonify(location_data)


@views_blueprint.route('/images/<string:filename>')
def get_images(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)

@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@views_blueprint.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id
