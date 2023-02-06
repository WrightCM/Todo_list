from flask import Flask, render_template, abort, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class TodoList(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    on = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['POST', 'GET'])
def homepage():
    todos = TodoList.query.all()
    if request.method == 'POST':
        text = request.form.get('todo')
        new_todo = TodoList(
            text = text,
            on = 0
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('index.html', todos=todos)

@app.route('/check/<int:id>', methods=['POST', 'GET'])
def check(id):
    todo = TodoList.query.filter_by(id=id).first()
    todo.on = 1
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/uncheck/<int:id>', methods=['POST', 'GET'])
def uncheck(id):
    todo = TodoList.query.filter_by(id=id).first()
    todo.on = 0
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    todo = TodoList.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)
