from werkzeug.urls import url_parse
from app import app, db
from flask import render_template,flash,redirect,request, url_for
from app.forms import LoginForm,RegistrationForm, EditprofileForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from datetime import datetime


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditprofileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title="Edit Profile",
                           form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'Om'}
    posts =[
    {'author': {'username': 'John'},
    'body': "beautiful day in Portland!"
    },

    {'author': {'username': 'Susan'},
    'body': "The avengers movie was so cool!"

    },
    {'author':{'username':'Om'},
    'body':"Roses are red, Sky are blue, you are nerver a fool to love, Really?"}
    ]
    return render_template('index.html', user=user, title="Home", posts=posts)


# @app.route('/hello/<name>')
# def hello(name):
#
#     return "Hey there,{}".format(name)
#
# @app.route('/new/')
# def new():
#     return "Hello world"
#
# @app.route('/another')
# def another():
#     return "Hey there I am another route"
#
# @app.route('/add/<int:num1>/<int:num2>')
# @app.route('/add/<float:num1>/<float:num2>')
# @app.route('/add/<float:num1>/<int:num2>')
# @app.route('/add/<int:num1>/<float:num2>')
# def add(num1, num2):
#     return render_template("add.html", num1 = num1, num2 = num2)
#
# @app.route('/power/<int:number>')
# def power(number):
#     # square = number*number
#     # return '{}*{} = {}'.format(number,number*number)
#     # return "The square of {} is {}".format(number,square)
#     return render_template('squareOf.html', number = number)

@app.route('/login',methods =['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user,remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',title="Sign In",form= form)
    #
    #     flash('login reuested for user{}, remember_me{}'.format(
    #     form.username.data, form.remember_me.data))
    #     return redirect('/index')
    # return render_template('login.html',title='sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user =User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html',title = 'Register', form=form)


@app.route('/user/<username>')
# allow only for authorized users
@login_required
# the view for user routes
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test Post #1'},
            {'author': user, 'body': 'Test Post #2'}
            ]
    # render template with the posts above
    return render_template('user.html', user=user, posts=posts)
