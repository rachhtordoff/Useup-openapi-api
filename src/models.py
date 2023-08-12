from src import db
from sqlalchemy.dialects.postgresql import JSONB


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    categories = db.Column(JSONB)
    expiry_date = db.Column(db.db.String(64))
    date_added = db.Column(db.db.String(64))
    brand = db.Column(db.String(64))
    image_url = db.Column(db.String(400))
    barcode = db.Column(db.String(400))

    def __repr__(self):
        return f'<Product {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'categories': self.categories,
            'expiry_date': self.expiry_date,
            'date_added': self.date_added,
            'brand': self.brand,
            'image_url': self.image_url,
            'barcode': self.barcode
        }