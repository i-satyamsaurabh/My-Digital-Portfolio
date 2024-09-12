from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['Name']
        comment = request.form['comment']
        new_review = Review(name=name, comment=comment)
        db.session.add(new_review)
        db.session.commit()

    all_reviews = Review.query.all()
    return render_template('index.html', all_reviews=all_reviews)

@app.route('/show')
def project():
    all_reviews = Review.query.all()
    print(all_reviews)
    return "This is Project page"

@app.route('/interesting-links')
def interesting_links():
    return render_template('interesting_links.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/delete/<int:id>')
def delete(id):
    review = Review.query.filter_by(id=id).first()
    if review:
        db.session.delete(review)
        db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>')
def update(id):
    review = Review.query.filter_by(id=id).first()
    if review:
        db.session.delete(review)
        db.session.commit()
    return render_template('update.html', review=review)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables before running the app
    app.run(debug=True, port=5500)