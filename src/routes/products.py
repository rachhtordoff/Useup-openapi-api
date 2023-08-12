from flask import Blueprint, jsonify
from src.models import Product
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime, timedelta

products = Blueprint('products', __name__)

@products.route('/products/<id>', methods=['GET'])
@jwt_required()
def get_products(id):
    print(id)
    products = Product.query.filter_by(user_id=int(id)).all()
    newlist=[]
    for product in products:
        newlist.append(product.to_dict())
    return jsonify(newlist)


@products.route('/expiring-products/<id>', methods=['GET'])
@jwt_required()
def get_expiring_products(id):
    today = datetime.now().date()
    three_days_from_now = today + timedelta(days=3)

    # Convert all product expiry_dates to datetime objects and compare
    expiring_products = []
    products = Product.query.filter_by(user_id=int(id)).all()
    for product in products:
        product_expiry_date = datetime.strptime(product.expiry_date, '%d/%m/%Y').date()

        if today < product_expiry_date <= three_days_from_now:
            expiring_products.append(product.to_dict())
    return jsonify(expiring_products)

@products.route('/expired-products/<id>', methods=['GET'])
@jwt_required()
def get_recently_expired_products(id):
    print(id)
    ten_days_ago = datetime.now() - timedelta(days=10)

    # Convert all product expiry_dates to datetime objects and compare
    expired_products = []
    products = Product.query.filter_by(user_id=int(id)).all()
    for product in products:
        product_expiry_date = datetime.strptime(product.expiry_date, '%d/%m/%Y')
        if ten_days_ago <= product_expiry_date < datetime.now():
            expired_products.append(product.to_dict())

    return jsonify(expired_products)


@products.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict())
