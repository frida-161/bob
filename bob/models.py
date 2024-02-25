from bob import db
from geoalchemy2.elements import WKTElement
from geoalchemy2 import Geometry


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    comment = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    # Add a geometry field to store the spatial data (point)
    geom = db.Column(Geometry('POINT'))

    def __init__(self, latitude, longitude, comment, photo):
        self.latitude = latitude
        self.longitude = longitude
        self.comment = comment
        self.photo = photo
        # Generate point data from latitude and longitude
        self.geom = self.generate_point()

    def generate_point(self):
        # Construct a point geometry from latitude and longitude
        point_wkt = f'POINT({self.longitude} {self.latitude})'
        return WKTElement(point_wkt, srid=4326)
