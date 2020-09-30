from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


#Create an instances of our web application and set path of our SQLite uri.
app = Flask(__name__, template_folder="templates")
app.secret_key = "SecretKey20202020202020"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data_test.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#postgres
#app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql+psycopg2://postgres:password@localhost/quotes'

#Creating a table
#Create an instance of SQLAlchemy
db = SQLAlchemy(app)

class eData(db.Model):
	__tablename__ = 'records'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(200), unique=False)
	email = db.Column(db.String(250), unique=False)
	timestamp = db.Column(
		db.DateTime, default=datetime.now(), onupdate=datetime.now()
  )

@app.errorhandler(404)
def page_not_found(e):
	return '<h1>404 PAGE NOT FOUND!<br><a href="/">Click here go to Home</a></h1>'
	#return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
	return '<h1>500 Internal Server Error!</h1>'
	#return render_template('500.html')

@app.route('/')
def index():
	result = eData.query.all()
	return render_template('index.html',result=result)
#	return '<h1>Hello World!</h1>'

@app.route('/table')
def table():
	results = eData.query.all()
	return render_template('table.html',results=results)

@app.route('/data')
def data():
	 return render_template('add.html')

#add new record
@app.route('/add', methods =['POST'])
def add():
	username = request.form['username']
	email = request.form['email']
#
	add_data = eData(username=username,email=email)
	db.session.add(add_data)
	db.session.commit()

	return redirect(url_for('index'))
	#return '<h1>ADD TEST</h1><br><h1>Username: {}<br>Email: {}</h1>'.format(username,email)

#edit a record
@app.route('/edit/<id>', methods = ['GET', 'POST'])
def edit(id):
	edit_data = eData.query.get(id)
	return render_template("edit.html",result = edit_data)


#update a record
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        update_data = eData.query.get(request.form.get('id'))
        update_data.username = request.form['username']
        update_data.email = request.form['email']

        db.session.commit()
        flash("Data Updated Successfully")
	
        return redirect('/')
        #return redirect(url_for('Index'))

#delete a record
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    del_data = eData.query.get(id)
    db.session.delete(del_data)
    db.session.commit()
    flash("Data Deleted Successfully")

    return redirect('/')

#search page
@app.route('/search', methods=['GET', 'POST'])
def search():
	return render_template('search.html')


#search result
@app.route('/results', methods =['POST'])
def search_results():
	search = request.form['search']
	search_text = search
	qry1 = eData.query.filter(eData.username.like('%'+ search_text +'%')).all()
	qry2 = eData.query.filter(eData.email.like('%'+ search_text +'%')).all()
	qry3 = eData.query.filter(eData.id.like('%'+ search_text +'%')).all()
	result = qry1 or qry2 or qry3
	return render_template('search.html', result=result)





