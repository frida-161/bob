from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_from_directory
from bob.models import Location
from bob import db, app

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/')
def index():
    locations = Location.query.all()
    return render_template('index.html', locations=locations)


@views_blueprint.route('/add_location', methods=['POST'])
def add_location():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    comment = request.form['comment']
    photo = request.files['photo']

    new_location = Location(latitude=latitude, longitude=longitude, comment=comment, photo=photo.filename)
    db.session.add(new_location)
    db.session.commit()

    photo.save(str(Path(app.config['UPLOAD_DIR']) / photo.filename))

    return redirect(url_for('views.index'))


@views_blueprint.route('/upload_location')
def upload_location():
    return render_template('upload_location.html')


@views_blueprint.route('/display_map')
def display_map():
    locations = Location.query.all()
    return render_template('display_map.html', locations=locations)


@views_blueprint.route('/api/locations')
def get_locations():
    locations = Location.query.all()
    location_data = [
        {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "comment": location.comment,
            "photo": url_for("views.get_images", filename=location.photo)
        } for location in locations]
    return jsonify(location_data)


@views_blueprint.route('/images/<string:filename>')
def get_images(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)
