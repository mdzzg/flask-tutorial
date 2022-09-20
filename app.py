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
    line_name_prop = db.Column(db.Integer)
    node_from_prop = db.Column(db.Integer)
    node_to_prop = db.Column(db.Integer)
    susceptance_prop = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    return redirect('/lines')

@app.route('/lines', methods=['POST', 'GET'])
def arbitrary():
    if request.method == 'POST':
        line_name = request.form['line_name']
        node_from = request.form['node_from']
        node_to = request.form['node_to']
        susceptance = request.form['susceptance']
        add_line = Lines(line_name_prop=line_name, node_from_prop=node_from, node_to_prop=node_to, susceptance_prop=susceptance)

        try:
            db.session.add(add_line)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        lines = Lines.query.order_by(Lines.date_created).all() #sqlalchemy
        return render_template('index.html', lines=lines)


@app.route('/lines/delete/<int:id>')
def delete(id):
    line_to_delete = Lines.query.get_or_404(id)

    try:
        db.session.delete(line_to_delete)
        db.session.commit()
        return redirect('/lines')
    except:
        return 'There was a problem deleting that task'

@app.route('/lines/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    line = Lines.query.get_or_404(id)

    if request.method == 'POST':
        line.line_name_prop = request.form['line_name']
        line.node_from_prop = request.form['node_from']
        line.node_to_prop = request.form['node_to']
        line.susceptance_prop = request.form['susceptance']
        
        try:
            db.session.commit()
            return redirect('/lines')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', line=line)


if __name__ == "__main__":
    app.run(debug=True)
