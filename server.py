import sys, os
sys.path.append(os.getcwd())

from flask import Flask, render_template, redirect, session, request
from models.fact_model import FactModel
from models.base_model import DBSingleton

app = Flask(__name__)

@app.before_first_request
def initialize_tables():
	connect_db()
	if not FactModel.table_exists():
		FactModel.create_table()
	disconnect_db()

@app.before_request
def connect_db():
	DBSingleton.getInstance().connect()

@app.teardown_request
def disconnect_db(err=None):
	DBSingleton.getInstance().close()

@app.route('/facts/<int:id>', methods=['DELETE'])
def delete_fact(id):
	pass

@app.route('/facts/<int:id>', methods=['POST'])
def add_fact(id):
	pass

@app.route('/facts/<int:id>', methods=['PUT'])
def update_fact(id):
	pass

@app.route('/facts/<int:id>',methods=['GET'])
def get_fact(id):
	query = FactModel.select().where(FactModel.id == id)

	if query.count() != 1:
		return "error", "400 Bad Request"

	else:
		fact_record = query.get()

		return "My fact is {}".fomart(fact_record.fact)

@app.route('/facts', methods=['GET'])
def view_all_facts():
	query = FactModel.select().dicts()

	return render_template('example_template.html', query=query)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
