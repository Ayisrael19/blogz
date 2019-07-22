from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    body = db.Column(db.String(500))

    def __init__(self, title,body):
        self.title = title
        self.body = body        

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')
    

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
            new_blog = Blog(title_name,body_name)
            db.session.add(new_blog)
            db.session.commit()
            blogs = Blog.query.filter_by().all()
            ld = blogs[-1].id
        return redirect(f'/blog?id={ld}')
    else:
        return render_template('newpost.html', title = "Blog Entry")


@app.route('/blog', methods = ['POST','GET'])
def home():
    rule = request.url
    if rule == 'http://localhost:5000/blog':
        return render_template('todos.html',title="Build-A-Blog", 
    blogPosts=Blog.query.filter_by().all())
    else:
        blogs = Blog.query.filter_by().all()
        ld = ""
        for i in rule[21::]:
            if i in "0123456789":
                ld += i
        ld = int(ld)-1
        if ld >= 12:
            ld =ld - 5
        blogTitle = blogs[int(ld)].title
        blogBody = blogs[int(ld)].body
        return render_template('blog.html', title = blogTitle, body = blogBody)
        
        
            
        

if __name__ == '__main__':
    app.run()
