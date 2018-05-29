from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, select, Table, MetaData
from json import dumps
from flask import jsonify
import json
import os

db = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
app = Flask(__name__)
api = Api(app)
meta = MetaData(db, reflect=True)

departments = meta.tables['departments']
dept_emp = meta.tables['dept_emp']
dept_manager = meta.tables['dept_manager']
employees = meta.tables['employees']
salaries = meta.tables['salaries']
titles = meta.tables['titles']


class Employees(Resource):
	def get(self):
		con = db.connect()
		select_statement = select([employees])
		res = con.execute(select_statement)
		result = [dict(zip(tuple (res.keys()) ,i)) for i in res.cursor]
		return jsonify(result)
	
	def post(self):
		con = db.connect()
		for key,value in request.json.items():
			print (key,value)
		try:
			emp_no_recv = request.json['emp_no']
			birth_date_recv = request.json['birth_date']
			first_name_recv = request.json['first_name']
			last_name_recv = request.json['last_name']
			gender_recv = request.json['gender']
			hire_date_recv = request.json['hire_date']
		except:
			return {"error":"probably misssing some field"}
		
		ins = employees.insert().values(
				emp_no = emp_no_recv,
				birth_date = birth_date_recv,
				first_name = first_name_recv,
				last_name = last_name_recv,
				gender = gender_recv,
				hire_date = hire_date_recv)
		con.execute(ins)
		
	
class Employees_Id(Resource):
	def get(self,emp_no):
		con = db.connect()
		select_statement = select([employees]).where(employees.c.emp_no == emp_no)
		res = con.execute(select_statement)
		result = [dict(zip(tuple (res.keys()) ,i)) for i in res.cursor]
		return jsonify(result)

class Status(Resource):
	def get(self):
		res = {}
		res['status'] = 'OK'
		res['hostname'] = os.getenv('HOSTNAME')
		return res

class Home(Resource):
	def get(self):
		return {'HOME':'OK'}

api.add_resource(Employees, '/employees')
api.add_resource(Employees_Id, '/employees/<emp_no>')
api.add_resource(Status, '/status')
api.add_resource(Home, '/')



if __name__ == '__main__':
	app.run(debug=True)



