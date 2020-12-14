from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from vs_url_for import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GDIOGJFOIAJDG33F3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bird:password@localhost/birdies_db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
geolocator = Nominatim()


class users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))
	kind = db.Column(db.String(20))
        

class orders(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	zip = db.Column(db.String(255))
	des = db.Column(db.String(255))
	order_date = db.Column(db.DateTime, nullable=False)
	user_id = db.Column(db.Integer)
	lat = db.Column(db.String(255))
	lng = db.Column(db.String(255))
	price = db.Column(db.Integer)

class addOrderForm(FlaskForm):
	des = StringField('Please enter description of your items here', validators = [InputRequired(), Length(min=1, max=255)])
	zip = StringField('Please enter your Postcode', validators = [InputRequired(), Length(min=5, max=8)])
	price = StringField('Please enter the price of your items', validators = [InputRequired()])

@login_manager.user_loader
def load_user(user_id):
	return users.query.get(int(user_id))


class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')
	


class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email')])

	username = StringField('username', validators = [InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)]) 


class OrderForm(FlaskForm):
	zip = StringField('zip', validators=[InputRequired()])

	des = StringField('items', validators=[InputRequired()])
        
	price = StringField('Price', validators=[InputRequired()])

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = users.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember)
				if user.kind == 'volunteer':
						return redirect(vs_url_for('dashboard'))
				else:
						return redirect(vs_url_for('landing', id=current_user.id))

		return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()
	
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method ='sha256')
		new_user = users(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return '<h1> a new user has been created </h1>' 

	return render_template('signup.html',form=form)
@app.route('/signup2', methods=['GET', 'POST'])
def signup2():
	form = RegisterForm()
	
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user = volunteers(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return '<h1> a new user has been created </h1>'
	return render_template('signup2.html',form=form)



@app.route('/dashboard')
@login_required

def dashboard():
	form = orders.query.all()

	return render_template('dashboard.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/landing/<id>', methods=['GET', 'POST'])
@login_required
def landing(id):

	form = orders.query.filter_by(user_id = id).all()
	return render_template('landing.html', form=form)


@app.route('/add_order', methods=['GET', 'POST'])
@login_required
def add_order():
    form = addOrderForm()
    if form.validate_on_submit():
        location = geolocator.geocode(form.zip.data)
        new_order = orders(des= form.des.data, zip = form.zip.data,price = form.price.data, user_id = current_user.id, lat = location.latitude, lng = location.longitude)
        db.session.add(new_order)
        db.session.commit()
        flash('You have succesfully submitted your order')
        return redirect(vs_url_for('landing', id=current_user.id))
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('orderform.html', form=form)


@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/active')
def active():
	return render_template('active.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)
