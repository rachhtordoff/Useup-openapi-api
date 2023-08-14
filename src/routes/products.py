from flask import Blueprint, jsonify, request
from src.models import Product
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime, timedelta
from src import db

products = Blueprint('products', __name__)
'''
Status for products:

pantry/fridge
waste
consumed
shopping
'''


@products.route('/products-shopping/<id>', methods=['GET'])
@jwt_required()
def get_products_shopping(id):
    print(id)
    ten_days_ago = datetime.now() - timedelta(days=10)

    products = Product.query.filter_by(user_id=int(id)).all()
    newlist=[]
    for product in products:
        if product.status == 'shopping':
            newlist.append(product.to_dict())
    return jsonify(newlist)



@products.route('/products/<id>', methods=['GET'])
@jwt_required()
def get_products(id):
    print(id)
    ten_days_ago = datetime.now() - timedelta(days=10)

    products = Product.query.filter_by(user_id=int(id)).all()
    newlist=[]
    for product in products:
        if product.status != 'shopping'  and product.status != 'waste':
            if product.expiry_date != '' and product.expiry_date != None:
                product_expiry_date = datetime.strptime(product.expiry_date, '%d/%m/%Y')
                if ten_days_ago <= product_expiry_date < datetime.now():
                    print('dont add expired')
                else:
                    newlist.append(product.to_dict())
            else:
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
        if product.status != 'shopping'  and product.status != 'waste':

            if product.expiry_date != '' and product.expiry_date != None:
                product_expiry_date = datetime.strptime(product.expiry_date, '%d/%m/%Y').date()

                if today < product_expiry_date <= three_days_from_now:
                    expiring_products.append(product.to_dict())

    return jsonify(expiring_products)


@products.route('/remove-product/<int:product_id>', methods=['GET'])
def remove_product(product_id):
    product = Product.query.get(product_id)
    
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": f"Product {product.id} deleted"}), 200

@products.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # Getting the request data
    data = request.json

    # Update fields based on the provided data
    if 'name' in data:
        product.name = data['name']
    if 'user_id' in data:
        product.user_id = data['user_id']
    if 'categories' in data:
        product.categories = data['categories']
    if 'expiry_date' in data:
        product.expiry_date = data['expiry_date']
    if 'brand' in data:
        product.brand = data['brand']
    if 'image_url' in data:
        product.image_url = data['image_url']
    if 'barcode' in data:
        product.barcode = data['barcode']
    if 'price' in data:
        product.price = data['price']
    if 'status' in data:
        product.status = data['status']
    if 'waste_level' in data:
        product.status = data['waste_level']

    db.session.commit()

    return jsonify({"message": f"Product {product.id} updated successfully"}), 200

@products.route('/copy_product-fridge/<int:product_id>', methods=['GET'])
def copy_product_fridge(product_id):
    product = Product.query.get(product_id)
    
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # Create a new product with the same data but status set to 'shopping'
    new_product = Product(
        name=product.name,
        user_id=product.user_id,
        categories=product.categories,
        expiry_date='',
        brand=product.brand,
        image_url=product.image_url,
        barcode=product.barcode,
        price=product.price,
        status='pantry/fridge'
    )

    db.session.add(new_product)
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": f"Product {new_product.id} created with status shopping"}), 200



@products.route('/copy_product-shopping/<int:product_id>', methods=['GET'])
def copy_product_shopping(product_id):
    product = Product.query.get(product_id)
    
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # Create a new product with the same data but status set to 'shopping'
    new_product = Product(
        name=product.name,
        user_id=product.user_id,
        categories=product.categories,
        expiry_date='',
        brand=product.brand,
        image_url=product.image_url,
        barcode=product.barcode,
        price=product.price,
        status='shopping'
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": f"Product {new_product.id} created with status shopping"}), 200


@products.route('/expired-products/<id>', methods=['GET'])
@jwt_required()
def get_recently_expired_products(id):
    print(id)
    ten_days_ago = datetime.now() - timedelta(days=10)

    # Convert all product expiry_dates to datetime objects and compare
    expired_products = []
    products = Product.query.filter_by(user_id=int(id)).all()
    for product in products:
        if product.status != 'shopping'  and product.status != 'waste':
            if product.expiry_date != '' and product.expiry_date != None:
                product_expiry_date = datetime.strptime(product.expiry_date, '%d/%m/%Y')
                if ten_days_ago <= product_expiry_date < datetime.now():
                    expired_products.append(product.to_dict())

    return jsonify(expired_products)

@products.route('/recipe-products/<id>', methods=['GET'])
@jwt_required()
def recipe_products(id):
    print(id)
    today = datetime.now().date()
    ten_days_ago = datetime.now() - timedelta(days=10)
    three_days_from_now = today + timedelta(days=3)

    expiring_products_str = ""
    other_products_str = ""
    products = Product.query.filter_by(user_id=int(id)).all()

    for product in products:
        if product.expiry_date != '' and product.expiry_date != None:

            product_expiry_date = datetime.strptime(product.expiry_date, '%d/%m/%Y').date()

            if today < product_expiry_date <= three_days_from_now:

                if expiring_products_str:
                    expiring_products_str += ", "
                expiring_products_str += product.to_dict()['name']

            elif product_expiry_date < today:
                print('ignore')
            else:
                if other_products_str:
                    other_products_str += ", "
                other_products_str += product.to_dict()['name']

    response = {
        "expiring_products": expiring_products_str,
        "other_products": other_products_str
    }
    return jsonify(response)


@products.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict())
