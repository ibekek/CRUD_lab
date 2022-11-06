from flask_sqlalchemy import SQLAlchemy

db =SQLAlchemy()

class HumanModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    human_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    best_game = db.Column(db.String(80))
    best_actor = db.Column(db.String(80))


    def __init__(self, human_id,name,age,best_game,best_actor):
        self.human_id = human_id
        self.name = name
        self.age = age
        self.best_game = best_game
        self.best_actor = best_actor

    def __repr__(self):
        return f"{self.name}:{self.human_id}"

from flask import Flask,render_template,request,redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        human_id = request.form['human_id']
        name = request.form['name']
        age = request.form['age']
        best_game = request.form['best_game']
        best_actor = request.form['best_actor']
        human = HumanModel(human_id=human_id, name=name, age=age, best_game=best_game, best_actor=best_actor)
        db.session.add(human)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    humans = HumanModel.query.all()
    return render_template('datalist.html', humans=humans)


@app.route('/data/<int:id>')
def RetrieveHuman(id):
    human = HumanModel.query.filter_by(human_id=id).first()
    if human:
        return render_template('data.html', human = human)
    return f"Human with id ={id} Doesn't exist"


@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    human = HumanModel.query.filter_by(human_id=id).first()
    if request.method == 'POST':
        if human:
            db.session.delete(human)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            best_game = request.form['best_game']
            best_actor = request.form['best_actor']
            human = HumanModel(human_id=id, name=name, age=age, best_game=best_game, best_actor=best_actor)
            db.session.add(human)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Human with id = {id} Doesn't exist"

    return render_template('update.html', human = human)


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    human = HumanModel.query.filter_by(human_id=id).first()
    if request.method == 'POST':
        if human:
            db.session.delete(human)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')

app.run(host='localhost', port=3000)





