import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime as dt
import base64
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dlmotorroot:dlmotorroot@db4free.net/dlmotor'
# #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Dani060990@localhost:3307/dlmotor'
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
    def __init__(self, users_name, users_surname, users_password, users_email, users_type):
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
#user_types
@app.route('/user_types/<_id>', methods=['GET'])
def get_userTypes_id(_id):
    userTypes = UsersType.query.get(_id)
    return userType_schema.jsonify(userTypes)
# USER- INFO by id
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
# USER- INFO login
@app.route('/userInfo/<email>/<password>', methods=['GET'])
def get_userinfo(email, password):    
    user_email = email
    user_password = password
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
    return response

# USER- create
@app.route('/users', methods=['POST'])
def create_user():
    users_name = request.json['users_name']
    users_surname = request.json['users_surname']
    users_password = request.json['users_password']
    users_email = request.json['users_email']
    users_type = request.json['users_type']

    exist = Users.query.filter(Users.users_email == users_email).all()
    if (exist):
        result = {
            "response": "There is an account with this email!"
        }
    else:
        new_user = Users( users_name, users_surname, users_password, users_email, users_type )
        db.session.add(new_user)
        db.session.commit()

        user = Users.query.get(new_user.users_id)
        typeU = UsersType.query.get(new_user.users_type)
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
    return  jsonify(result)

#garage
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
#racingTeam
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
#categoriesRacing
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
# 
        
        
# # MODEL categories
# class Categories(db.Model):
#     categories_id = db.Column(db.Integer, primary_key=True)
#     categories_name = db.Column(db.String(50))
#     categories_image = db.Column(db.BLOB)
#     categories_description = db.Column(db.Text)
#     def __init__(self, categories_name, categories_image, categories_description):
#         self.categories_name = categories_name
#         self.categories_image = categories_image
#         self.categories_description = categories_description
# # MODEL vehicles
# class Vehicles(db.Model):
#     vehicles_id = db.Column(db.Integer, primary_key=True)
#     vehicles_name = db.Column(db.String(50))
#     vehicles_banner = db.Column(db.BLOB)
#     vehicles_image_category = db.Column(db.BLOB)
#     vehicles_category =  db.Column(db.Integer)
#     vehicles_slogan = db.Column(db.String(100))
#     vehicles_description = db.Column(db.Text)
#     vehicles_warranty = db.Column(db.String(50))
#     def __init__(self, vehicles_name, vehicles_banner, vehicles_image_category, vehicles_category, vehicles_slogan, vehicles_description, vehicles_warranty):
#         self.vehicles_name = vehicles_name
#         self.vehicles_banner = vehicles_banner
#         self.vehicles_image_category = vehicles_image_category
#         self.vehicles_category = vehicles_category
#         self.vehicles_slogan = vehicles_slogan
#         self.vehicles_description = vehicles_description
#         self.vehicles_warranty = vehicles_warranty
# # MODEL images vehicles
# class Imagesvehicles(db.Model):
#     imagesvehicles_id = db.Column(db.Integer, primary_key=True)
#     imagesvehicles_image =  db.Column(db.BLOB)
#     imagesvehicles_vehicleid = db.Column(db.Integer)
#     def __init__(self, imagesvehicles_id, imagesvehicles_image, imagesvehicles_vehicleid):
#         self.imagesvehicles_id = imagesvehicles_id
#         self.imagesvehicles_image = imagesvehicles_image
#         self.imagesvehicles_vehicleid = imagesvehicles_vehicleid
# # MODEL Versions vehicles
# class Versionsvehicles(db.Model):
#     versionsvehicles_id = db.Column(db.Integer, primary_key=True)
#     versionsvehicles_name =  db.Column(db.String(50))
#     versionsvehicles_image =  db.Column(db.BLOB)
#     versionsvehicles_baseprice = db.Column(db.FLOAT)
#     versionsvehicles_vehicleid = db.Column(db.Integer)
#     def __init__(self, versionsvehicles_id, versionsvehicles_name, versionsvehicles_image, versionsvehicles_baseprice, versionsvehicles_vehicleid):
#         self.versionsvehicles_id = versionsvehicles_id
#         self.versionsvehicles_name = versionsvehicles_name
#         self.versionsvehicles_image = versionsvehicles_image
#         self.versionsvehicles_baseprice = versionsvehicles_baseprice
#         self.versionsvehicles_vehicleid = versionsvehicles_vehicleid
# # MODEL complement versions vehicles
# class Complementsversions(db.Model):
#     complementsversions_id = db.Column(db.Integer, primary_key=True)
#     complementsversions_name =  db.Column(db.String(100))
#     complementsversions_versionsid = db.Column(db.Integer)
#     def __init__(self, complementsversions_id, complementsversions_name, complementsversions_versionsid):
#         self.complementsversions_id = complementsversions_id
#         self.complementsversions_name = complementsversions_name
#         self.complementsversions_versionsid = complementsversions_versionsid
# # MODEL colors vehicles
# class Colorsvehicles(db.Model):
#     colorsvehicles_id = db.Column(db.Integer, primary_key=True)
#     colorsvehicles_name =  db.Column(db.String(50))
#     colorsvehicles_color =  db.Column(db.BLOB)
#     colorsvehicles_imgcolor = db.Column(db.BLOB)
#     colorsvehicles_price = db.Column(db.Integer)
#     colorsvehicles_vehicleid = db.Column(db.Integer)
#     def __init__(self, colorsvehicles_id, colorsvehicles_name, colorsvehicles_color, colorsvehicles_imgcolor, colorsvehicles_price, colorsvehicles_vehicleid):
#         self.colorsvehicles_id = colorsvehicles_id
#         self.colorsvehicles_name = colorsvehicles_name
#         self.colorsvehicles_color = colorsvehicles_color
#         self.colorsvehicles_imgcolor = colorsvehicles_imgcolor
#         self.colorsvehicles_price = colorsvehicles_price
#         self.colorsvehicles_vehicleid = colorsvehicles_vehicleid
# # MODEL Interiors vehicles
# class Interiorsvehicles(db.Model):
#     interiorsvehicles_id = db.Column(db.Integer, primary_key=True)
#     interiorsvehicles_name =  db.Column(db.String(50))
#     interiorsvehicles_image =  db.Column(db.BLOB)
#     interiorsvehicles_baseprice = db.Column(db.FLOAT)
#     interiorsvehicles_vehicleid = db.Column(db.Integer)
#     def __init__(self, interiorsvehicles_id, interiorsvehicles_name, interiorsvehicles_image, interiorsvehicles_baseprice, interiorsvehicles_vehicleid):
#         self.interiorsvehicles_id = interiorsvehicles_id
#         self.interiorsvehicles_name = interiorsvehicles_name
#         self.interiorsvehicles_image = interiorsvehicles_image
#         self.interiorsvehicles_baseprice = interiorsvehicles_baseprice
#         self.interiorsvehicles_vehicleid = interiorsvehicles_vehicleid
# # MODEL complement interiors vehicles
# class Complementsinteriors(db.Model):
#     complementsinteriors_id = db.Column(db.Integer, primary_key=True)
#     complementsinteriors_name =  db.Column(db.String(100))
#     complementsinteriors_interiorid = db.Column(db.Integer)
#     def __init__(self, complementsinteriors_id, complementsinteriors_name, complementsinteriors_interiorid):
#         self.complementsinteriors_id = complementsinteriors_id
#         self.complementsinteriors_name = complementsinteriors_name
#         self.complementsinteriors_interiorid = complementsinteriors_interiorid
# # MODEL rims vehicles
# class Rimsvehicles(db.Model):
#     rimsvehicles_id = db.Column(db.Integer, primary_key=True)
#     rimsvehicles_model =  db.Column(db.String(50))
#     rimsvehicles_size =  db.Column(db.String(50))
#     rimsvehicles_material =  db.Column(db.String(50))
#     rimsvehicles_image =  db.Column(db.BLOB)
#     rimsvehicles_baseprice = db.Column(db.FLOAT)
#     rimsvehicles_vehicleid = db.Column(db.Integer)
#     def __init__(self, rimsvehicles_id, rimsvehicles_model, rimsvehicles_size, rimsvehicles_material, rimsvehicles_image, rimsvehicles_baseprice, rimsvehicles_vehicleid):
#         self.rimsvehicles_id = rimsvehicles_id
#         self.rimsvehicles_model = rimsvehicles_model
#         self.rimsvehicles_size = rimsvehicles_size
#         self.rimsvehicles_material = rimsvehicles_material
#         self.rimsvehicles_image = rimsvehicles_image
#         self.rimsvehicles_baseprice = rimsvehicles_baseprice
#         self.rimsvehicles_vehicleid = rimsvehicles_vehicleid
# # MODEL quote
# class Quotes(db.Model):
#     quotes_id = db.Column(db.Integer, primary_key=True)
#     quotes_date = db.Column(db.DATETIME)
#     quotes_customer = db.Column(db.String(100))
#     quotes_email = db.Column(db.String(50))
#     quotes_vehicleid = db.Column(db.Integer)
#     quotes_modelvehicle = db.Column(db.String(50))
#     quotes_version = db.Column(db.Integer)
#     quotes_versionprice = db.Column(db.FLOAT)
#     quotes_color = db.Column(db.Integer)
#     quotes_colorprice = db.Column(db.FLOAT)
#     quotes_interior = db.Column(db.Integer)
#     quotes_interiorprice = db.Column(db.FLOAT)
#     quotes_rims = db.Column(db.Integer)
#     quotes_rimsprice = db.Column(db.FLOAT)
#     quotes_discount = db.Column(db.String(100))
#     quotes_discountprice = db.Column(db.FLOAT)
#     quotes_total = db.Column(db.FLOAT)
#     quotes_status = db.Column(db.Integer)
#     def __init__(self, quotes_date, quotes_customer, quotes_email, quotes_vehicleid, quotes_modelvehicle, quotes_version, quotes_versionprice, quotes_color, quotes_colorprice, quotes_interior, quotes_interiorprice, quotes_rims, quotes_rimsprice, quotes_discount, quotes_discountprice, quotes_total, quotes_status):
#         self.quotes_date = quotes_date
#         self.quotes_customer = quotes_customer
#         self.quotes_email = quotes_email
#         self.quotes_vehicleid = quotes_vehicleid
#         self.quotes_modelvehicle = quotes_modelvehicle
#         self.quotes_version = quotes_version
#         self.quotes_versionprice = quotes_versionprice
#         self.quotes_color = quotes_color
#         self.quotes_colorprice = quotes_colorprice
#         self.quotes_interior = quotes_interior
#         self.quotes_interiorprice = quotes_interiorprice
#         self.quotes_rims = quotes_rims
#         self.quotes_rimsprice = quotes_rimsprice
#         self.quotes_discount = quotes_discount
#         self.quotes_discountprice = quotes_discountprice
#         self.quotes_total = quotes_total
#         self.quotes_status = quotes_status
# # MODEL quote
# class Quotesstatus(db.Model):
#     quotesstatus_id = db.Column(db.Integer, primary_key=True)
#     quotesstatus_name = db.Column(db.String(25))
#     def __init__(self, quotesstatus_id, quotesstatus_name):
#         self.quotesstatus_id = quotesstatus_id
#         self.quotesstatus_name = quotesstatus_name
# db.create_all()
# 
# class UsersSchema(ma.Schema):
#     class Meta:
#         fields = ('users_id', 'users_name', 'users_surname', 'users_password', 'users_email', 'users_type_id')
# user_schema = UsersSchema()
# users_schema = UsersSchema(many=True)
# class ComplementsversionsSchema(ma.Schema):
#     class Meta:
#         fields = ('complementsversions_id', 'complementsversions_name', 'complementsversions_versionsid')
# complementVersion_schema = ComplementsversionsSchema()
# complementsVersion_schema = ComplementsversionsSchema(many=True)
# class QuotesstatusSchema(ma.Schema):
#     class Meta:
#         fields = ('quotesstatus_id', 'quotesstatus_name')
# quoteStatus_schema = QuotesstatusSchema()
# quotesStatus_schema = QuotesstatusSchema(many=True)
