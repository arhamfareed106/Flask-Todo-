from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:  # Check if title and desc are not empty
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is product'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:  # Check if title and desc are not empty
            todo.title = title
            todo.desc = desc
            db.session.commit()
            return redirect('/')
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables for our data models
    app.run(debug=True)
