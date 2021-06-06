
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_cors import CORS
import base64

from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Dani060990@localhost:3307/dlmotor'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql11416217:AGfCIW1zeC@sql11.freemysqlhosting.net/sql11416217'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql11416217:AGfCIW1zeC@sql11.freemysqlhosting.net/sql11416217'
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

# MODEL userType
class UsersType(db.Model):
    userstype_id = db.Column(db.Integer, primary_key=True)
    userstype_name = db.Column(db.String(45))
    def __init__(self, userstype_name):
        self.userstype_name = userstype_name
        

# MODEL users
class Users(db.Model):
    users_id = db.Column(db.Integer, primary_key=True)
    users_name = db.Column(db.String(50))
    users_surname = db.Column(db.String(50))
    users_password = db.Column(db.String(25))
    users_email = db.Column(db.String(50))
    users_type = db.Column(db.Integer)

    def __init__(self, users_name, users_surname, users_password, users_email, users_type):
        self.users_name = users_name
        self.users_surname = users_surname
        self.users_password = users_password
        self.users_email = users_email
        self.users_type = users_type


db.create_all()

class CompanySchema(ma.Schema):
    class Meta:
        fields = ('company_id', 'company_name', 'company_description', 'company_contact', 'company_logo')
company_schema = CompanySchema()
companys_schema = CompanySchema(many=True)

class UserTypesSchema(ma.Schema):
    class Meta:
        fields = ('userstype_id', 'userstype_name')
userType_schema = UserTypesSchema()
userTypes_schema = UserTypesSchema(many=True)

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('users_id', 'users_name', 'users_surname', 'users_password', 'users_email', 'users_type_id')
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


## ROUTES
## company
@app.route('/company/<_id>', methods=['GET'])
def get_company(_id):
    company = Company.query.get(_id)
    
    result = {
        "company_name": company.company_name,
        "company_description": company.company_description,
        "company_contact": company.company_contact,
        "company_logo":  base64.b64encode(company.company_logo).decode("utf-8")   
    }

    db.session.commit()
    response = jsonify(result)

    return response

## Garage
@app.route('/garage/<_id>', methods=['GET'])
def get_garage(_id):
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
    return response


## RacingTeam
@app.route('/racingTeam/<_id>', methods=['GET'])
def get_racingTeam(_id):
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
    return response

## categoriesRacing
@app.route('/categoriesRacing', methods=['GET'])
def get_categoriesracing():
    categoriesracing = Categoriesracing.query.all()
    
    result = []
    for category in categoriesracing:
        result.append({
            "categoriesracing_name": category.categoriesracing_name,
            "categoriesracing_image": base64.b64encode(category.categoriesracing_image).decode("utf-8"),
            "categoriesracing_video": category.categoriesracing_video  
        })

    db.session.commit()
    response = jsonify(result)

    return response


## user_types
@app.route('/user_types/<_id>', methods=['GET'])
def get_userTypes_id(_id):
    userTypes = UsersType.query.get(_id)
    return userType_schema.jsonify(userTypes)


## USER- INFO by id
@app.route('/userInfo/<_id>', methods=['GET'])
def get_userinfoByid(_id):    
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
    return response

## USER- INFO login
@app.route('/userInfo/<email>/<password>', methods=['GET'])
def get_userinfo(email, password):    
    user_email = email
    user_password = password
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
                "response": "Declined"
            }
    else:
        result = {
            "response": "Declined"
        }

    db.session.commit()
    response = jsonify(result)
    return response

## CREATE USER
@app.route('/users', methods=['POST'])
def create_user():
    users_name = request.json['users_name']
    users_surname = request.json['users_surname']
    users_password = request.json['users_password']
    users_email = request.json['users_email']
    users_type = request.json['users_type']

    
    new_user = Users( users_name, users_surname, users_password, users_email, users_type )
    db.session.add(new_user)
    db.session.commit()

    user = Users.query.get(new_user.users_id)
    typeU = UsersType.query.get(new_user.users_type)
    print(typeU.userstype_id)
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
    return  jsonify(result)


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

