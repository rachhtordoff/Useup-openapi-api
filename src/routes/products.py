from flask import Blueprint, jsonify
from src.models import Product
from flask_jwt_extended import create_access_token, jwt_required

products = Blueprint('products', __name__)

@products.route('/products/<id>', methods=['GET'])
@jwt_required(id)
def get_products():
    products = Product.query.filter_by(user_id=id).first()
    return jsonify([product.to_dict() for product in products])

@products.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict())
