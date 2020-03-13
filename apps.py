from flask import Flask,render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#a must step
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:user@localhost/movie_apps' #use for configuration 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug=True
db = SQLAlchemy(app)

#note that all model inherited from the 
class User(db.Model):  
    #to name the table, use below or by default the table name is model
    __tablename__ = 'user'
    #create 3 table
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80),unique =True)
    email = db.Column(db.String(60),unique =True)

    def __init__(self,username,email):
        self.username = username
        self.email = email
    
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    myuser = User.query.all() # assign value to do query in the db
    #return list of object to be passed through our template
    oneItem = User.query.filter_by(username = 'fatin').first() #note that first(): to remove duplicate
    return render_template('add-user.html', myuser=myuser, oneItem=oneItem)

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['username'],request.form['email'])
    db.session.add(user) #adding the data(create object)
    db.session.commit() #to save the data
    return redirect(url_for('index'))
