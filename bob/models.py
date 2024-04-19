import uuid
from geoalchemy2.elements import WKTElement
from geoalchemy2 import Geometry
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.dialects.postgresql import UUID
import datetime

from bob import db

# Association table for the many-to-many relationship between Location and Tag
location_tag = db.Table('location_tag',
    db.Column('location_id', db.Integer, db.ForeignKey('locations.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # Use server default
    timestamp = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    removed_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    comment = db.Column(db.String)

    tags = db.relationship('Tag', secondary='location_tag', back_populates='locations')
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('locations_added', lazy='dynamic'))
    removed_by = db.relationship('User', foreign_keys=[removed_id], backref=db.backref('locations_removed', lazy='dynamic'))
    loc_type = db.relationship('Type', back_populates='locations')

    # Add a geometry field to store the spatial data (point)
    geom = db.Column(Geometry('POINT'))

    def __init__(self, latitude, longitude, photo):
        # all we need to initialize a new location
        self.latitude = latitude
        self.longitude = longitude
        self.photo = photo
        # Generate point data from latitude and longitude
        self.geom = self.generate_point()

    def generate_point(self):
        # Construct a point geometry from latitude and longitude
        point_wkt = f'POINT({self.longitude} {self.latitude})'
        return WKTElement(point_wkt, srid=4326)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    locations = db.relationship('Location', secondary='location_tag', back_populates='tags')

class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    descr = db.Column(db.String)  # Assuming 'descr' stands for 'description'
    locations = db.relationship("Location", back_populates="loc_type")

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    timestamp = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP'))
    role = db.Column(db.String)
    # The invite that this user got invited with
    invite_id = db.Column(UUID, db.ForeignKey('invites.id'))
    # The invites that this user has issued
    invites = db.relationship('Invite', backref='issued_by', lazy=True, foreign_keys=[invite_id])

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Invite(db.Model):
    __tablename__ = 'invites'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # The id of the user that issued this  invite
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP'))
    revoked = db.Column(db.Boolean, default=False)
    exp_date = db.Column(db.DateTime)
    user_limit = db.Column(db.Integer)
    # The users that were invited by this invite
    users = db.relationship('User', backref='invited_by', lazy=True, foreign_keys=[user_id])

    def is_valid(self):
        """ Return False if the invite is not valid anymore. """
        return (
            datetime.datetime.now() < self.exp_date and
            self.user_limit < len(self.users) and
            not self.revoked
        )
