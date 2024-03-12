import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators

    @validates('name')
    def validate_name(self, key, name):
        if not name:     # name is None/False/0/
            raise ValueError("All Authors should have a name")
        # if db.session.query(Author).filter(Author.name == name).first():
        #     raise ValueError('No two authors have the same name')
        return name
    
    @validates('phone_number')
    def validate_phone(self, key, value):
        value = str(value)
        if len(value) != 10 or not value.isdigit():
            raise ValueError('phone_number must be exactly 10 digits and contain only numbers')
        return value
    
   

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
# Add author function
def add_author(name, phone_number):
    author = Author(name=name, phone_number=phone_number)
    db.session.add(author)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("A unique constraint was violated.")

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators

    @validates('title')
    def post_title(self, key, title):
        clickbait_phrases = ["won't believe", "secret", "top [0-9]+","guess"]
        if not any(re.search(phrase, title.lower()) for phrase in clickbait_phrases):
            raise ValueError("Title must not be clickbait")
        if not title:     # name is None/False/0/
            raise ValueError("All posts have a title")
        return title
    
    @validates('content')
    def post_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content is at least 250 characters long")
        return content
    
    @validates('summary')
    def post_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary is a maximum of 250 characters")
        return summary
       
    @validates('category')
    def post_category(self, key, category):
        if (category != "Fiction") and (category != "Non-Fiction"):
            raise ValueError("Post category is either Fiction or Non-Fiction")
        return category



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'


