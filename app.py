import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime as dt
import base64

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dlmotorroot:dlmotorroot@db4free.net/dlmotor'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Dani060990@localhost:3307/dlmotor'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# MODEL COMPANY
class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(45))
    company_logo = db.Column(db.BLOB)
    company_description = db.Column(db.Text)
    company_contact = db.Column(db.String(11))
    
    def __init__(self, company_id, company_name, company_logo, company_description, company_contact):
        self.company_id = company_id
        self.company_name = company_name
        self.company_logo = company_logo
        self.company_description = company_description
        self.company_contact = company_contact

# MODEL USERTYPE
class UsersType(db.Model):
    userstype_id = db.Column(db.Integer, primary_key=True)
    userstype_name = db.Column(db.String(45))
    def __init__(self, userstype_name):
        self.userstype_name = userstype_name

# MODEL USERS
class Users(db.Model):
    users_id = db.Column(db.Integer, primary_key=True)
    users_name = db.Column(db.String(50))
    users_surname = db.Column(db.String(50))
    users_password = db.Column(db.String(25))
    users_email = db.Column(db.String(50))
    users_type = db.Column(db.Integer)

    def __init__(self, users_id, users_name, users_surname, users_password, users_email, users_type):
        self.users_id = users_id
        self.users_name = users_name
        self.users_surname = users_surname
        self.users_password = users_password
        self.users_email = users_email
        self.users_type = users_type

#SCHEMA
class UserTypesSchema(ma.Schema):
    class Meta:
        fields = ('userstype_id', 'userstype_name')
userType_schema = UserTypesSchema()
userTypes_schema = UserTypesSchema(many=True)

#ROUTES

#home
@app.route('/', methods=['GET'])
def home():
    return f'Its working'

#company
@app.route('/company/', methods=['GET'])
def get_company():
    _id = request.args['id']
  
    company = Company.query.get(_id)
    
    result = {
        "company_name": company.company_name,
        "company_description": company.company_description,
        "company_contact": company.company_contact,
        "company_logo":  base64.b64encode(company.company_logo).decode("utf-8")   
    }
    db.session.commit()
    response = jsonify(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

#user_types
@app.route('/user_types/', methods=['GET'])
def get_userTypes_id():
    _id = request.args['id']
    userTypes = UsersType.query.get(_id)
    response = userType_schema.jsonify(userTypes)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# USER- INFO by id
@app.route('/userInfoById/', methods=['GET'])
def get_userinfoByid():
    _id = request.args['id']    
    user = Users.query.get(_id)

    typeU = UsersType.query.get(user.users_type)
    result = {
        "user_id": user.users_id,
        "user_name": user.users_name,
        "user_surname": user.users_surname,
        "user_password": user.users_password,
        "user_email": user.users_email,
        "userType":[
            {
                "usertype_id": typeU.userstype_id, 
                "usertype_name": typeU.userstype_name
            }
        ],
        "response": "Accepted"        
    }

    db.session.commit()
    response = jsonify(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# USER- INFO login
@app.route('/userInfo/', methods=['GET'])
def get_userinfo():    
    user_email = request.args['email'] 
    user_password =  request.args['password'] 
    exist = Users.query.filter(Users.users_email == user_email).all()
    if (exist):
        user = Users.query.filter(Users.users_email == user_email).one()
        if(user):
            if (user_password == user.users_password):
                typeU = UsersType.query.get(user.users_type)
                result = {
                    "user_id": user.users_id,
                    "user_name": user.users_name,
                    "user_surname": user.users_surname,
                    "user_password": user.users_password,
                    "user_email": user.users_email,
                    "userType":[
                        {
                            "usertype_id": typeU.userstype_id, 
                            "usertype_name": typeU.userstype_name
                        }
                    ],
                    "response": "Accepted"        
                }
            else:
                result = {
                    "response": "Wrong email or password"
                }
        else:
            result = {
                "response": "Wrong email or password"
            }
    else:
        result = {
            "response": "Account not Found"
        }

    db.session.commit()
    response = jsonify(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# USER- create
@app.route('/createUsers/', methods=['POST'])
def create_user():
    users_name = request.json['users_name']
    users_surname = request.json['users_surname']
    users_password = request.json['users_password']
    users_email = request.json['users_email']
    users_type = request.json['users_type']

    result ={
        "users_name": users_name, 
        "users_surname": users_surname,
        "users_password": users_password,
        "users_email": users_email,
        "users_type": users_type,
    }
    exist = Users.query.filter(Users.users_email == users_email).all()
    if (exist):
        result = {
            "response": "There is an account with this email!"
        }
    else:
        new_user = Users( users_name, users_surname, users_password, users_email, users_type )
        # db.session.add(new_user)
        db.session.commit()

        result = {
            "new_user": new_user,
            "response": "creado"
        }

    # if (exist):
    #     result = {
    #         
    #     }
    # else:
    #     new_user = Users( users_name, users_surname, users_password, users_email, users_type )
    #     db.session.add(new_user)
    #     db.session.commit()

    #     user = Users.query.get(new_user.users_id)
    #     typeU = UsersType.query.get(new_user.users_type)
    #     result = {
    #         "user_id": user.users_id,
    #         "user_name": user.users_name,
    #         "user_surname": user.users_surname,
    #         "user_password": user.users_password,
    #         "user_email": user.users_email,
    #         "userType":[
    #             {
    #                 "usertype_id": typeU.userstype_id, 
    #                 "usertype_name": typeU.userstype_name
    #             }
    #         ],
    #         "response": "Accepted"        
    #     }
         
    # db.session.commit()
    response = jsonify(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return  response
