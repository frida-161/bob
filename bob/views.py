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


@views_blueprint.route('/', methods=['GET','POST'])
def display_map():
    if request.method == 'GET':
        return render_template('display_map.html')
    print("hi")
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    photo = request.files['photo']

    print(":)")

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

    print("pong")

    return redirect(url_for('views.get_location',id=new_location.id))


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
