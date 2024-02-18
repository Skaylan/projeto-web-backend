from flask import jsonify, request, Blueprint
from app.models.tables.category import Category
from app.controllers.utils.functions import print_error_details
from app.models.schemas.category_schema import CategorySchema
from app.extensions import db

category_route = Blueprint('gategory_route', __name__)


@category_route.route('/api/v1/add_category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        try:
            body = dict(request.get_json())
            name = body['name'] 

            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            db.session.close()      
            
            return jsonify({
                'status': 'ok',
                'message': 'Categoria adicionada com sucesso!'
            }), 201       

        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500                              
    

@category_route.route('/api/v1/get_categories', methods=["GET"])
def get_categories():
    try:
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        payload = category_schema.dump(categories)
        
        return jsonify({
            'categories': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500                                


@category_route.route('/api/v1/edit_category', methods=['PUT'])
def edit_category():
    if request.method == 'PUT':
        try:
            body = dict(request.get_json())
            category_id = body.get('category_id')
            new_name = body.get('new_name')

            if not category_id or not new_name:
                return jsonify({
                    'status': 'error',
                    'message': 'ID da categoria ou novo nome não foram fornecidos'
                }), 400

            category = Category.query.filter_by(id=category_id).first()

            if not category:
                return jsonify({
                    'status': 'error',
                    'message': 'Categoria não foi encontrada'
                }), 404

            category.name = new_name
            db.session.add(category)
            db.session.commit() 
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Categoria modificada com sucesso'
            }), 200

        except Exception as error:
            print_error_details(error)
            return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500

        

@category_route.route('/api/v1/delete_category', methods=['DELETE'])
def delete_category():
    if request.method == 'DELETE':
        try:
            body = request.get_json()
            id = body.get('id')

            category = Category.query.filter_by(id=id).first()

            if category == None:
                return jsonify({
                    'status': 'error',
                    'message': 'Categoria não encotrada'
                }),404
            
            db.session.delete(category)
            db.session.commit()
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Categoria deletada com sucesso!'
            }),200

        except Exception as error:
            print_error_details(error)
            return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
        

@category_route.route('/api/v1/get_one_category', methods=['GET'])
def get_one_category():
    if request.method == 'GET':
        try:
            name = request.args.get('name')

            one_category = Category.query.filter_by(name=name).first()

            if one_category == None:
                return jsonify({
                    'status': 'error',
                    'message': 'Categoria não encontrada!'
                }),404
            
            category_schema = CategorySchema()
            payload = category_schema.dump(one_category)

            return jsonify({
                'status': 'ok',
                'category': payload
            }),200
        
        except Exception as error:
            print_error_details(error)
            return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500