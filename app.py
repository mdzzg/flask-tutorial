from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Lines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Integer)
    content1 = db.Column(db.Integer)
    content2 = db.Column(db.Integer)
    content3 = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['sequence']
        task_content1 = request.form['node_from']
        task_content2 = request.form['node_to']
        task_content3 = request.form['suseptance']
        new_line = Lines(content=task_content, content1=task_content1, content3=task_content3, content2=task_content2)

        try:
            db.session.add(new_line)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        lines = Lines.query.order_by(Lines.date_created).all() #sqlalchemy
        return render_template('index.html', lines=lines)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Lines.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Lines.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
