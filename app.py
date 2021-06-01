import re
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# from flask_cors import CORS
import base64

app = Flask(__name__)

# cors = CORS(app, allow_headers='Content-Type', CORS_SEND_WILDCARD=True)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Dani060990@localhost:3307/dlmotor'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql11416217:AGfCIW1zeC@sql11.freemysqlhosting.net/sql11416217'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# MODEL COMPANY
class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(45))
    company_logo = db.Column(db.BLOB)
    company_description = db.Column(db.Text)
    company_contact = db.Column(db.String(11))
    
    def __init__(self,  company_name, company_logo, company_description, company_contact):
        self.company_name = company_name
        self.company_logo = company_logo
        self.company_description = company_description
        self.company_contact = company_contact
        

# # MODEL userType
# class UsersType(db.Model):
#     usertype_id = db.Column(db.Integer, primary_key=True)
#     usertype_name = db.Column(db.String(45))
#     def __init__(self, usertype_name):
#         self.usertype_name = usertype_name
        

# # MODEL users
# class Users(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(50))
#     user_password = db.Column(db.String(50))
#     user_email = db.Column(db.String(50))
#     user_type_id = db.Column(db.Integer, db.ForeignKey('users_type.usertype_id'))

#     def __init__(self, user_name, user_password, user_email, user_type_id):
#         self.user_name = user_name
#         self.user_password = user_password
#         self.user_email = user_email
#         self.user_type_id = user_type_id


db.create_all()

class Companychema(ma.Schema):
    class Meta:
        fields = ('company_id', 'company_name', 'company_description', 'company_contact', 'company_logo')
company_schema = Companychema()
companys_schema = Companychema(many=True)


# class UserTypesSchema(ma.Schema):
#     class Meta:
#         fields = ('usertype_id', 'usertype_name')
# userType_schema = UserTypesSchema()
# userTypes_schema = UserTypesSchema(many=True)

# class UsersSchema(ma.Schema):
#     class Meta:
#         fields = ('user_id', 'user_name', 'user_password', 'user_email', 'user_type_id')
# user_schema = UsersSchema()
# users_schema = UsersSchema(many=True)


## ROUTES
## company
@app.route('/company/<_id>', methods=['GET'])
def get_companies(_id):
    company = Company.query.get(_id)
    
    result = {
        "company_name": company.company_name,
        "company_description": company.company_description,
        "company_contact": company.company_contact,
        "company_logo":  base64.b64encode(company.company_logo).decode("utf-8")   
    }

    # print(result)
    db.session.commit()
    response = jsonify(result)

    return response


## Users types
# @app.route('/user_types', methods=['POST'])
# def create_userTypes():
#     usertype_name = request.json['usertype_name']

#     new_userType = UsersType( usertype_name )
#     db.session.add(new_userType)
#     db.session.commit()

#     userType = UsersType.query.get(new_userType.usertype_id)
#     result = userType_schema.dump(userType)
#     return  jsonify(result)

# @app.route('/user_types', methods=['GET'])
# def get_userTypes():
#     all_userTypes = UsersType.query.all()
#     result = userTypes_schema.dump(all_userTypes)
#     return jsonify(result)

# @app.route('/user_types/<_id>', methods=['GET'])
# def get_userTypes_id(_id):
#     userTypes = UsersType.query.get(_id)
#     return userType_schema.jsonify(userTypes)

# @app.route('/user_types/<_id>', methods=['PUT'])
# def update_userTypes(_id):
#     userTypes = UsersType.query.get(_id)
#     name = request.json['name']

#     userTypes.name = name
#     db.session.commit()

#     return userType_schema.jsonify(userTypes)

# @app.route('/user_types/<_id>', methods=['DELETE'])
# def delete_userTypes(_id):
#     userTypes = UsersType.query.get(_id)
    
#     db.session.delete(userTypes)
#     db.session.commit()

#     return userType_schema.jsonify(userTypes)


# ## Users types
# @app.route('/users', methods=['GET'])
# def get_users():
#     all_users = Users.query.all()
#     result = users_schema.dump(all_users)
#     return jsonify(result)


# @app.route('/users/<_id>', methods=['GET'])
# def get_users_id(_id):
#     user = Users.query.get(_id)
#     typeU = UsersType.query.get(user.user_type_id)

#     result = {
#         "user_id": user.user_id,
#         "user_name": user.user_name,
#         "user_password": user.user_password,
#         "user_email": user.user_email,
#         "userType":[
#             {
#                 "usertype_id": typeU.usertype_id, 
#                 "usertype_name": typeU.usertype_name
#             }
#         ]
        
#     }
#     response = jsonify(result)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route('/users', methods=['POST'])
# def create_user():
#     user_name = request.json['user_name']
#     user_password = request.json['user_password']
#     user_email = request.json['user_email']
#     user_type_id = request.json['user_type_id']
    

#     new_user = Users( user_name, user_password, user_email, user_type_id )
#     db.session.add(new_user)
#     db.session.commit()

#     user = Users.query.get(new_user.user_id)
#     result = user_schema.dump(user)
#     return  jsonify(result)

# @app.route('/users/<_id>', methods=['PUT'])
# def update_user(_id):
#     user = Users.query.get(_id)
#     user_name = request.json['user_name']
#     user_password = request.json['user_password']
#     user_email = request.json['user_email']
#     user_type_id = request.json['user_type_id']

#     user.user_name = user_name
#     user.user_password = user_password
#     user.user_email = user_email
#     user.user_type_id = user_type_id
#     db.session.commit()

#     return user_schema.jsonify(user)

# @app.route('/users/<_id>', methods=['DELETE'])
# def delete_user(_id):
#     user = Users.query.get(_id)
    
#     db.session.delete(user)
#     db.session.commit()

#     return user_schema.jsonify(user)

# # Session
# @app.route('/sessions', methods=['GET'])
# def session():
#     email = request.json['email']
#     password = request.json['password']
#     user = Users.query.filter_by(user_email = email).first()

#     if(user):
#         if (user.user_password == password):
#             response = get_users_id(user.user_id)
#             response.headers.add('Access-Control-Allow-Origin', '*')
#             return response
#         else:
#             return "password no correcta"
#     else:
#         return "no existe"

    
    


if __name__ == '__main__':
    app.run(debug=True)

