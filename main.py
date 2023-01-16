import os
from flask import Flask, render_template, redirect, url_for, request, send_from_directory, session, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mimetypes
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'TheBigSecretForASmallCompany'
app.config['UPLOAD_FOLDER'] = 'uploads'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "file_keeper.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')
	
class RegistrationForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
@login_required
def index():
	files_data = []
	for file in os.listdir(app.config['UPLOAD_FOLDER']):
		file_data = {}
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
		file_data['name'] = file
		file_data['mimetype'], file_data['encoding'] = mimetypes.guess_type(file_path)
		file_data['upload_time'] = datetime.fromtimestamp(os.path.getctime(file_path))
		file_data['size'] = os.path.getsize(file_path)
		files_data.append(file_data)
	return render_template('index.html', user=current_user.username, files=files_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
		form = LoginForm()
		if form.validate_on_submit():
				user = User.query.filter_by(username=form.username.data).first()
				if user and argon2.verify(form.password.data, user.password):
						login_user(user, remember=form.remember.data)
						return redirect(url_for('index'))
				else:
						return '<h2>Invalid username or password! <a href="/login">Try again!</a></h2>'
		return render_template('login.html', form=form)
	
@app.route('/register', methods=['GET', 'POST'])
def register():
		form = RegistrationForm()
		if form.validate_on_submit():
				passed_username = form.username.data
				if User.query.filter_by(username=passed_username).first():
						return '<h2>This user already exists! <a href="/register">Try again!</a></h2>'
				new_user = User(username=passed_username, password=argon2.hash(form.password.data))
				db.session.add(new_user)
				db.session.commit()
				return '<h2>The new user has been registered. <a href="/login">Log in!</a></h2>'
		return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
		logout_user()
		return redirect(url_for('index'))

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_old():
# 	file = request.files['file']
# 	if file:
# 		filename = file.filename
# 		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 		return '<h2>The file has been uploaded! <a href="/">Go back!</a></h2>'
# 	else:
# 		return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	if file:
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		files_data = []
		for file in os.listdir(app.config['UPLOAD_FOLDER']):
			file_data = {}
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
			file_data['name'] = file
			file_data['mimetype'], file_data['encoding'] = mimetypes.guess_type(file_path)
			file_data['upload_time'] = datetime.fromtimestamp(os.path.getctime(file_path))
			file_data['size'] = os.path.getsize(file_path)
			files_data.append(file_data)
		return jsonify(files_data)
	else:
		return 'No file selected', 400

@app.route('/download/<path:filename>')
def download_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/remove/<path:filename>', methods=['GET', 'POST'])
def remove_file(filename):
	file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	os.remove(file_path)
	return redirect(url_for('index'))

@app.route('/sort_files')
def sort_files():
	if 'sort_by' not in session:
		session['sort_by'] = 'name'
		session['sort_order'] = 'asc'
	sort_by = request.args.get('sort_by')
	sort_order = request.args.get('sort_order')
	if sort_by == session['sort_by']:
		sort_order = 'asc' if session['sort_order'] == 'desc' else 'desc'
	session['sort_by'] = sort_by
	session['sort_order'] = sort_order
	files_data = []
	for file in os.listdir(app.config['UPLOAD_FOLDER']):
		file_data = {}
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
		file_data['name'] = file
		file_data['mimetype'], file_data['encoding'] = mimetypes.guess_type(file_path)
		file_data['upload_time'] = datetime.fromtimestamp(os.path.getctime(file_path))
		file_data['size'] = os.path.getsize(file_path)
		files_data.append(file_data)
	if sort_by == 'name':
		sorted_files_data = sorted(files_data, key=lambda file: file['name'], reverse=(sort_order=='desc'))
	elif sort_by == 'size':
		sorted_files_data = sorted(files_data, key=lambda file: file['size'], reverse=(sort_order=='desc'))
	elif sort_by == 'upload_time':
		sorted_files_data = sorted(files_data, key=lambda file: file['upload_time'], reverse=(sort_order=='desc'))
	else:
		sorted_files_data = files_data
	return render_template('index.html', files=sorted_files_data)

app.run(host='0.0.0.0', port=81)