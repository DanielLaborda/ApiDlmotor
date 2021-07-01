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
    
    def __init__(self,  company_name, company_logo, company_description, company_contact):
        self.company_name = company_name
        self.company_logo = company_logo
        self.company_description = company_description
        self.company_contact = company_contact

#ROUTES

#home
@app.route('/', methods=['GET'])
def home():
    return f'Its working'

#company
@app.route('/company/', methods=['GET'])
def get_company():
    _id = request.args['id']
    # company = Company.query.get(_id)
    # result = {
    #     "company_name": company.company_name
    # }
    # db.session.commit()
    # company = Company.query.get(_id)
  
    # result = {
    #     "company_name": company.company_name,
    #     "company_description": company.company_description,
    #     "company_contact": company.company_contact,
    #     "company_logo":  base64.b64encode(company.company_logo).decode("utf-8")   
    # }
    # db.session.commit()
    # response = jsonify(result)
    return f'response' + db
