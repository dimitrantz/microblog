from flask import render_template
from app import flaskapp
from app.forms import LoginForm

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    user = { 'username': 'dimitrantz'}
    posts = [
        {
            'author': {'username': "Pocopico"},
            'body': 'Boring Day in Olympia Electronics'
            },
        {
            'author': {'username': "Pocopico"},
            'body': 'I love my little Princess Pocopico'
                        
        },
        {
            'author': {'username': "dimitrantz"},
            'body': 'I love my Pocopico very much too!'
                        
        }
    ]
    return render_template('index.html', title='Home', user=user, posts = posts)

@flaskapp.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Sign In', form=form)