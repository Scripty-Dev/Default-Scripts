from flask import Blueprint, jsonify

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/test')
def test():
    return jsonify({
        'message': 'API is working!'
    }) 