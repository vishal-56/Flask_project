from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user, logout_user
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database and secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config["SECRET_KEY"] = "thisissecrete"
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect here if not logged in

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Blog {self.title}'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
@login_required
def index():
    data = Blog.query.all()
    return render_template("index.html", data=data)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/index')
        else:
            flash('Invalid Credentials', 'danger')
            return redirect('/login')

    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("User has been registered successfully!", 'success')
        return redirect("/login")

    return render_template("register.html")

@app.route("/forshow")
def forshow():
    return "for show"
@app.route('/blogpost', methods=['GET', 'POST'])
def blogpost():
    if request.method == 'POST':
        # Handle the form submission (POST request)
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Create a new blog post entry
        blog = Blog(title=title, author=author, content=content)
        db.session.add(blog)
        db.session.commit()

        # Flash a success message and redirect to home
        flash("Your post has been submitted successfully", 'success')
        return redirect("/")

    # For GET request, render the form
    return render_template("blog.html")

@app.route("/blog_detail/<int:id>", methods=['GET', 'POST'])
def blogdetail(id):
    blog=Blog.query.get(id)
    return render_template('blog_detail.html',blog=blog)



@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete_post(id):
    blog=Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash("Post has been deleted",'success')
    return redirect("/")


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_post(id):
    # Fetch the blog post or show 404 if not found
    blog = Blog.query.get(id)

    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')

        # Update the blog post
        blog.title = title
        blog.content = content
        blog.author=author

        # Commit changes to the database
        db.session.commit()

        flash('Post has been updated!', 'success')
        return redirect("/") # Redirect to the updated post or another page

    # Render the form template with the current blog post data
    return render_template('edit.html', blog=blog)




if __name__ == "__main__":
    app.run(debug=True)