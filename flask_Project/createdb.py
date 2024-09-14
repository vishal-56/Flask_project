from app import app, db, User

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created.")
    
    # Print users before adding new ones
    users_before = User.query.all()
    print(f"Users before adding: {users_before}")

    # Add the first user
    user1 = User(username='sachin', email="sdnjs@gmail.com", password="dxdf")
    db.session.add(user1)
    db.session.commit()
    print("First user added.")

    # Print users after adding the first user
    users_after_first_add = User.query.all()
    print(f"Users after adding first user: {users_after_first_add}")

    # Add the second user
    user2 = User(username='rahulds', email="sdndfa2js@gmail.com", password="123f")
    db.session.add(user2)
    db.session.commit()
    print("Second user added.")

    # Print users after adding the second user
    users_after_second_add = User.query.all()
    print(f"Users after adding second user: {users_after_second_add}")
