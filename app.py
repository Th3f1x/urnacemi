from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64, time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(1000))
    candidato = db.Column(db.String(100), nullable=False)
    votos = db.Column(db.Integer, default=0)
    foto = db.Column(db.LargeBinary)
    fotodesc = db.Column(db.String(100))

    def __init__(self, candidato, votos,desc,foto, fotodesc):
        self.desc = desc
        self.candidato = candidato
        self.votos = votos
        self.foto = foto
        self.fotodesc = fotodesc

@app.route('/')
def ini():
    return render_template('init.html')

@app.route('/votar')
def votar():
    visu = Item.query.all()
    return render_template('votar.html', visu=visu)

@app.route('/vote/<int:item_id>', methods=['POST','GET'])
def vote(item_id):
    
    item = Item.query.get(item_id)
    time1 = 2 #timer for redirect

    if request.method == 'POST':
        item.votos += 1
        db.session.commit()
        time.sleep(time1)
        return redirect(url_for('fim'))
    
    return render_template('vote.html',item=item)
    
@app.route('/fim')
def fim():
    return render_template('/Fim.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":

        candidato = request.form['candidato']
        foto_file = request.files['foto']
        desc = request.form['desc']
        fotodesc = foto_file.filename
        votos = 0

        file_data = foto_file.read()#converter image file for b64 file

        item = Item(candidato=candidato,desc=desc ,votos=votos, foto=file_data, fotodesc=fotodesc)

        db.create_all()
        db.session.add(item)
        db.session.commit()
        return redirect('/')
    
    return render_template('cadastra.html')

@app.route('/editar/<int:item_id>',methods=['GET','POST'])
def editar(item_id):
    item = Item.query.get(item_id)

    if request.method == 'POST':
        item.candidato = request.form['candidato']
        item.desc = request.form['desc']
        item.votos = request.form['votos']
        db.session.commit() 
        return redirect('/dashboard')
    
    return render_template('editar.html',item=item)

@app.route('/deletar/<int:item_cod>',methods=['GET', 'POST'])
def deleta(item_cod):
    item = Item.query.get(item_cod)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('deletar.html', item=item)


@app.route('/dashboard')
def visu():
    visu = Item.query.all()
    return render_template('dashboard.html', visu=visu)

@app.template_filter('b64encode')#translater b64 for sql and html
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')


if __name__ == '__main__':
    app.run(debug=True)

#@Th3f1x