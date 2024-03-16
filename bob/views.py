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
        comment=comment, photo=ufilename)

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


@views_blueprint.route('/api/locations')
def get_locations():
    def get_url(location):
        if location.photo:
            return url_for("views.get_images", filename=location.photo)
        return None

    locations = Location.query.all()
    location_data = [
        {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "comment": location.comment,
            "photo": get_url(location)
        } for location in locations]
    return jsonify(location_data)


@views_blueprint.route('/images/<string:filename>')
def get_images(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)
