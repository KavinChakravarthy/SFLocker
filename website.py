from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create a Flask Instance

app = Flask(__name__)
#Add Databse
# Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db'

# Secret Key!
app.config['SECRET_KEY'] = "secret key"
# Initialize The Database 
db = SQLAlchemy(app)

# Create a Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a Form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
 


# Create a Form class
class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.dadta = ''
        flash(" User added successfully! ")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users=our_users)
    

# create a route (decorator)
@app.route('/')
# def index():
    # return "<h1>Hello World!</h1>"
def index():
    pizza = ["cheesy corn","hot chilli", "peppy paneer"]
    first_name="Kavin"
    stuff="this is my <strong>bold</strong> "
    return render_template("index.html", first_name=first_name, stuff = stuff, pizza=pizza)

# localhost:5000/user/Kavin
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

#Ctreate Custom Error Pages

# 1)  Invalid URL 404
@app.errorhandler(404)
def  page_not_found(e):
    return render_template("404.html"), 404

# 2)  Internal Server Error 500 change
@app.errorhandler(500)
def  page_not_found(e):
    return render_template("500.html"), 500

# Create a name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully")

    return render_template("name.html", name = name, form = form)
    

if __name__ == "__main__":

    app.run(debug=True)