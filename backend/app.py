from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
CORS = CORS(app) # This will enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(120),unique = False, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def json(self):
        return {"id": self.id, "email": self.email, "username": self.username, "password": self.password}

db.create_all()

# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'test success'})

# Create a User
@app.route('/api/flask/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(email = data['email'], username=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id': new_user.id,
            'email': new_user.email,
            'username': new_user.username,
            'password': new_user.password
        }
        )

    except Exception as e:
        return make_response(jsonify({'error': 'Something went wrong', 'Error': str(e)}), 500)

    
# Get all users
@app.route('/api/flask/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [{'id': user.id,'email': user.email, 'username': user.username, 'password': user.password} for user in users]
        return jsonify(users_data), 200

    except Exception as e:
        return make_response(jsonify({'error': 'Something went wrong', 'Error': str(e)}), 500)

#Get user by id
@app.route('/api/flask/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first() # This will return the first user with the id passed
        if user is None:
            return make_response(jsonify({'error': 'User not found'}), 404)
        return jsonify({'id': user.id,'email': user.email, 'username': user.username, 'password': user.password}), 200

    except Exception as e:
        return make_response(jsonify({'error': 'Something went wrong', 'Error': str(e)}), 500)


# Update user by id
@app.route('/api/flask/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first() # This will return the first user with the id passed
        if user is None:
            return make_response(jsonify({'error': 'User not found'}), 404)

        data = request.get_json()
        user.email = data['email']
        user.username = data['username']
        user.password = data['password']
        db.session.commit()

        return jsonify({'id': user.id,'email': user.email, 'username': user.username, 'password': user.password}), 200

    except Exception as e:
        return make_response(jsonify({'error': 'Something went wrong', 'Error': str(e)}), 500)

# Delete user by id
@app.route('/api/flask/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first() # This will return the first user with the id passed
        if user is None:
            return make_response(jsonify({'error': 'User not found'}), 404)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        return make_response(jsonify({'error': 'Something went wrong', 'Error': str(e)}), 500)