from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'noodles'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title,body,owner):
        self.title = title
        self.body = body        
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():
    blogUsers=User.query.filter_by().all()
    return render_template("index.html", blogUsers = blogUsers, title = "Home")
    

@app.route('/newpost',methods = ['POST','GET'])
def new_post():
    error_m = ''
    error2_m = ''
    if request.method == 'POST':
        title_name = request.form['Title']
        body_name = request.form['blog-post']
        if title_name == '':
            error_m = False
        if body_name == '':
            error2_m = False
        if error_m == False or error2_m == False:
            if error_m == False:
                error_m = 'Please fill in the title'
            if error2_m == False:
                error2_m = 'Please fill in the body'
            return render_template('newpost.html',title = 'Blog Entry', error = error_m, error2 = error2_m)
        else:
            owner = User.query.filter_by(username=session['user']).first()
            new_blog = Blog(title_name,body_name,owner)
            db.session.add(new_blog)
            db.session.commit()
            # blogs = Blog.query.filter_by().all()
            # ld = blogs[-1].id
        return redirect(f'/blog?id={new_blog.id}')
    else:
        return render_template('newpost.html', title = "Blog Entry")

@app.before_request
def require_login():
    allowed_routes = ['login', 'home',"sign_up","index"]
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/login',methods = ['POST','GET'])
def login():
    error_m = ""
    error2_m = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        if user and password == user.password:
            session['user'] = user.username
            session['id']= user.id
            return redirect('/newpost')
        else:
            if not user:
                error_m += "Incorrect Username"
                return render_template("login.html", error = error_m, error2 = error2_m)
            if password != user.password:
                error2_m = "Incorrect Password"
            return render_template("login.html", error = error_m, error2 = error2_m)
    else:
        return render_template("login.html", title= "Login")

@app.route('/logout',methods = ['POST','GET'])
def logout():
    del session['id']
    del session['user']
    return redirect('/blog')

@app.route('/signup',methods = ['POST','GET'])
def sign_up():
    usernames = []
    userInfo = User.query.filter_by().all()
    for info in userInfo:
        usernames.append(info.username)
    if request.method == "POST":
        username1 = True
        username = request.form['username']
        password = request.form['password']
        verify = request.form['retype_password']

        if not 3 <= len(username) <= 20 or " " in username or username in usernames:
            username1 = False
        if not 3 <= len(password) <= 20 or " " in password:
            password = False
        if password != verify:
            verify = False
        if username1 == False or password == False or verify == False:
            if username1 == False:
                if username in usernames:
                    username1 = "Username already taken"
                    username = ""
                else:
                    username1 = " Invalid username"
                    username = ""
            else:
                username1 = ""
            if password == False:
                password = " Invalid password"
            else:
                password = ""
            if password != verify:
                verify = " Password does not match."
            else:
                verify = ""
            return render_template("signup.html",error1=username1,error2=password,error3=verify)
        existing_user = User.query.filter_by(username = username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
        return redirect('/newpost')
    else:
        return render_template("signup.html")
    
            


@app.route('/blog', methods = ['POST','GET'])
def home():
    rule = request.url
    blogUsers = User.query.filter_by().all()
    if 'http://localhost:5000/blog?id' in rule or "127.0.0.1:5000/blog?id" in rule:
        ld = ""
        num = 21
        if "127.0.0.1:5000/blog?user" in rule:
            num = 23
        for i in rule[num::]:
            if i in "0123456789":
                ld += i
        ld = int(ld)
        blogs = Blog.query.filter_by(id = ld).first()
        return render_template('singleUser.html',blogUsers = blogUsers,blogPost = blogs) 
    elif 'http://localhost:5000/blog?user' in rule or "127.0.0.1:5000/blog?user" in rule:
        ld = ""
        num = 21
        if "127.0.0.1:5000/blog?user" in rule:
            num = 23
        for i in rule[num::]:
            if i in "0123456789":
                ld += i
        ld = int(ld)
        blogs = Blog.query.filter_by(owner_id = ld).all()
        return render_template('blog.html',blogUsers = blogUsers,blogPosts = blogs)       
    else:
        return render_template('todos.html',title="Blogz", 
        blogPosts=Blog.query.filter_by().all(), blogUsers = blogUsers)
       
        
if __name__ == '__main__':
    app.run()