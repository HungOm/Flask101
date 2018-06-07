from flask import request
from app import app
from flask import render_template,flash,redirect
from app.forms import LoginForm

@app.route('/')
def index():
    user = {'username':'Om'}
    posts =[
    {'author':{'username':'John'},
    'body':"beautiful day in Portland!"
    },

    {'author':{'username':'Susan'},
    'body':"The avengers movie was so cool!"

    },
    {'author':{'username':'Om'},
    'body':"Roses are red, Sky are blue, you are nerver a fool to love ,Really?"}
    ]
    return render_template('index.html', user =user, title ="Home", posts =posts)


@app.route('/hello/<name>')
def hello(name):

    return "Hey there,{}".format(name)

@app.route('/new/')
def new():
    return "Hello world"

@app.route('/another')
def another():
    return "Hey there I am another route"

@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
@app.route('/add/<int:num1>/<float:num2>')
def add(num1, num2):
    return render_template("add.html", num1 = num1, num2 = num2)

@app.route('/power/<int:number>')
def power(number):
    # square = number*number
    # return '{}*{} = {}'.format(number,number*number)
    # return "The square of {} is {}".format(number,square)
    return render_template('squareOf.html', number = number)

@app.route('/login',methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('login reuested for user{}, remember_me{}'.format(
        form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',title='sign In', form=form)
