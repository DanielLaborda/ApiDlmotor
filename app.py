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

    def __init__(self,  users_name, users_surname, users_password, users_email, users_type):
        self.users_name = users_name
        self.users_surname = users_surname
        self.users_password = users_password
        self.users_email = users_email
        self.users_type = users_type

# MODEL GARAGE
class Garage(db.Model):
    garage_id = db.Column(db.Integer, primary_key=True)
    garage_name = db.Column(db.String(45))
    garage_description = db.Column(db.Text)
    garage_contact = db.Column(db.String(11))
    garage_positionX = db.Column(db.FLOAT)
    garage_positionY = db.Column(db.FLOAT)
    garage_image = db.Column(db.BLOB)
  
    def __init__(self,  garage_name, garage_description, garage_contact, garage_positionX, garage_positionY, garage_image):
        self.garage_name = garage_name
        self.garage_description = garage_description
        self.garage_contact = garage_contact
        self.garage_positionX = garage_positionX
        self.garage_positionY = garage_positionY
        self.garage_image = garage_image

# MODEL RacingTeam
class Racingteam(db.Model):
    racingteam_id = db.Column(db.Integer, primary_key=True)
    racingteam_name = db.Column(db.String(50))
    racingteam_slogan = db.Column(db.String(100))
    racingteam_description = db.Column(db.Text)
    racingteam_description2 = db.Column(db.Text)
    racingteam_video = db.Column(db.String(100))
    
    def __init__(self,  racingteam_name, racingteam_slogan, racingteam_description, racingteam_description2, racingteam_video):
        self.racingteam_name = racingteam_name
        self.racingteam_slogan = racingteam_slogan
        self.racingteam_description = racingteam_description
        self.racingteam_description2 = racingteam_description2
        self.racingteam_video = racingteam_video

# MODEL ImagesBannerRacing
class Imagesbannerracing(db.Model):
    ImagesBannerRacing_id = db.Column(db.Integer, primary_key=True)
    ImagesBannerRacing_image = db.Column(db.BLOB)
    ImagesBannerRacing_racingteam = db.Column(db.Integer)

    def __init__(self,  ImagesBannerRacing_id, ImagesBannerRacing_image, ImagesBannerRacing_racingteam):
        self.ImagesBannerRacing_id = ImagesBannerRacing_id
        self.ImagesBannerRacing_image = ImagesBannerRacing_image
        self.ImagesBannerRacing_racingteam = ImagesBannerRacing_racingteam

# MODEL Categoriesracing
class Categoriesracing(db.Model):
    categoriesracing_id = db.Column(db.Integer, primary_key=True)
    categoriesracing_name = db.Column(db.String(50))
    categoriesracing_image = db.Column(db.BLOB)
    categoriesracing_video = db.Column(db.String(100))

    def __init__(self,  categoriesracing_id, categoriesracing_name, categoriesracing_image, categoriesracing_video):
        self.categoriesracing_id = categoriesracing_id
        self.categoriesracing_name = categoriesracing_name
        self.categoriesracing_image = categoriesracing_image
        self.categoriesracing_video = categoriesracing_video

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
        db.session.add(new_user)
        db.session.commit()

        user = Users.query.filter(Users.users_email == users_email).first()
        typeU = UsersType.query.get(new_user.users_type)
        db.session.commit()
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
        

    response = jsonify(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return  response

#garage
@app.route('/garage/', methods=['GET'])
def get_garage():
    _id = request.args['id']  
    garage = Garage.query.get(_id)
    result = {
        "garage_name": garage.garage_name,
        "garage_description": garage.garage_description,
        "garage_contact": garage.garage_contact,
        "garage_position": [garage.garage_positionX, garage.garage_positionY],
        "garage_image":  base64.b64encode(garage.garage_image).decode("utf-8")   
    }
  
    db.session.commit()
    response = jsonify(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

#racingTeam
@app.route('/racingTeam/', methods=['GET'])
def get_racingTeam():
    _id = request.args['id']  
    racingTeam = Racingteam.query.get(_id)
    imagesBanner = Imagesbannerracing.query.filter(Imagesbannerracing.ImagesBannerRacing_racingteam == _id).all()
    
    resultImages = []
    for image in imagesBanner:
        resultImages.append(base64.b64encode(image.ImagesBannerRacing_image).decode("utf-8") )
    
    result = {
        "racingTeam_name": racingTeam.racingteam_name,
        "racingTeam_slogan": racingTeam.racingteam_slogan,
        "racingTeam_description": racingTeam.racingteam_description,
        "racingTeam_description2": racingTeam.racingteam_description2,
        "racingTeam_video": racingTeam.racingteam_video,
        "racingTeam_imagesBanner":  resultImages  
    }
    
    db.session.commit()
    response = jsonify(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response   