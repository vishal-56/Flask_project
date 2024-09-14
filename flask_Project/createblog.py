from app import app, db, Blog

with app.app_context():
    db.create_all()  # Create tables

    # Create a new blog post if necessary
    if not Blog.query.first():  # Check if there are any blog posts
        new_blog = Blog(title="First Blog", author="dsz", content="This is the content of the first blog post.")
        db.session.add(new_blog)
        db.session.commit()

    # Print all blog posts to verify
    blogs = Blog.query.all()
    for blog in blogs:
        print(blog)
