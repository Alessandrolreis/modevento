from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2
from sqlalchemy import or_ , and_

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://teste:teste@localhost/mod_eventos'
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgres://hwfipjeyhnxxem:9da506ef9654ed04c2e32ba09c2313043d12b43d7a08654d60bfb425a12bb361@ec2-50-19-114-27.compute-1.amazonaws.com:5432/d1lf6f6gltbjpt?sslmode=require'
db = SQLAlchemy(app)

class Modulo_Eventos(db.Model):
    id = db.Column('evento_id', db.Integer, primary_key=True)
    codigo_evento= db.Column(db.String(500))
    nome_evento = db.Column(db.String(500))
    data_ = db.Column(db.String(30))
    local_ = db.Column(db.String(500))
    estado_ = db.Column(db.String(500))
    cidade_ = db.Column(db.String(500))
    rua_ = db.Column(db.String(500))
    cep_ = db.Column(db.String(500))
    site_ = db.Column(db.String(500))
    palestrante_ = db.Column(db.String(500))
    assunto_ = db.Column(db.String(500))
    telefone_ = db.Column(db.String(500))
    email_ = db.Column(db.String(120), unique=True)

    def __init__(self,codigo_evento, nome_evento, data_, local_, estado_, cidade_, rua_, cep_, site_, palestrante_,
                 assunto_, telefone_, email_):
        self.codigo_evento=codigo_evento
        self.nome_evento = nome_evento
        self.data_ = data_
        self.local_ = local_
        self.estado_ = estado_
        self.cidade_ = cidade_
        self.rua_ = rua_
        self.cep_ = cep_
        self.site_ = site_
        self.palestrante_ = palestrante_
        self.assunto_ = assunto_
        self.telefone_ = telefone_
        self.email_ = email_

@app.route("/")
def pinicial():
    return render_template("pinicial.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/busca", methods=['POST', 'GET'])
def busca():
    if request.method == 'POST':
        codigo_evento=request.form['codigo_eve']
        nome_evento = request.form['nome_eve']
        data = request.form['data_eve']
        local = request.form['local_eve']
        site = request.form['site_eve']
        palestrante = request.form['responsavel_eve']
        assunto = request.form['assunto_eve']
        telefone = request.form['telefone_eve']
        email = request.form["email_name"]
        if nome_evento == "":
            nome_evento="¨"
        if assunto == "":
            assunto="¨"
        if db.session.query(Modulo_Eventos).filter(or_(Modulo_Eventos.email_ == email , Modulo_Eventos.codigo_evento == codigo_evento , Modulo_Eventos.data_ == data, Modulo_Eventos.local_ == local, Modulo_Eventos.site_ == site, Modulo_Eventos.palestrante_ == palestrante,
        Modulo_Eventos.assunto_.ilike("%"+assunto+"%"), Modulo_Eventos.telefone_ == telefone, Modulo_Eventos.nome_evento.ilike("%"+nome_evento+"%"))).count() > 0:
            busca= db.session.query(Modulo_Eventos).filter(or_(Modulo_Eventos.email_ == email , Modulo_Eventos.codigo_evento == codigo_evento , Modulo_Eventos.data_ == data, Modulo_Eventos.local_ == local, Modulo_Eventos.site_ == site, Modulo_Eventos.palestrante_ == palestrante,
            Modulo_Eventos.assunto_.ilike("%"+assunto+"%"), Modulo_Eventos.telefone_ == telefone, Modulo_Eventos.nome_evento.ilike("%"+nome_evento+"%")))
            return render_template('retorno.html' , Modulo_Eventos=busca.all())
        else:
            return render_template('busca.html'  ,  text='Dados não localizados!')
    return render_template('busca.html'  )

@app.route("/successo", methods=['POST', 'GET'])
def successo():
    if request.method == 'POST':
        codigo_evento=request.form['codigo_eve']
        nome_evento = request.form['nome_eve']
        data = request.form['data_eve']
        local = request.form['local_eve']
        estado = request.form['estado_eve']
        cidade = request.form['cidade_eve']
        rua = request.form['rua_eve']
        cep = request.form['cep_eve']
        site = request.form['site_eve']
        palestrante = request.form['responsavel_eve']
        assunto = request.form['assunto_eve']
        telefone = request.form['telefone_eve']
        email = request.form["email_name"]
        if db.session.query(Modulo_Eventos).filter(Modulo_Eventos.email_ == email).count() == 0:
            data = Modulo_Eventos(codigo_evento,nome_evento, data, local, estado, cidade, rua, cep, site, palestrante, assunto,
                                  telefone, email)
            db.session.add(data)
            db.session.commit()
            return render_template("sucesso.html")
    return render_template('cadastro.html',
                           text='Já localizamos esse endereço de e-mail. Verifique se o evento já foi cadastrado!')

@app.route('/lista')
def lita_all():
    return render_template('lista.html', Modulo_Eventos=Modulo_Eventos.query.all())

@app.route('/alterar',  methods=['POST', 'GET'])
def alterar():
    if request.method == 'POST':
        codigo_evento=request.form['codigo_eve']
        nome_evento = request.form['nome_eve']
        data = request.form['data_eve']
        local = request.form['local_eve']
        estado = request.form['estado_eve']
        cidade = request.form['cidade_eve']
        rua = request.form['rua_eve']
        cep = request.form['cep_eve']
        site = request.form['site_eve']
        palestrante = request.form['responsavel_eve']
        assunto = request.form['assunto_eve']
        telefone = request.form['telefone_eve']
        email = request.form["email_name"]
        if db.session.query(Modulo_Eventos).filter(Modulo_Eventos.codigo_evento == codigo_evento).count() >0 :
            db.session.query(Modulo_Eventos).filter(Modulo_Eventos.codigo_evento == codigo_evento).delete()
            db.session.commit()
            data = Modulo_Eventos(codigo_evento,nome_evento, data, local, estado, cidade, rua, cep, site, palestrante, assunto,
                                  telefone, email)
            db.session.add(data)
            db.session.commit()
            return render_template('alterar.html'  ,  text='Alteração realizada com sucesso!')
        else:
            return render_template('alterar.html'  ,  text='Código não localizado! Nenhuma alteração executada!')

    return render_template('alterar.html')

@app.route("/deleta", methods=['POST', 'GET'])
def deleta():
    if request.method == 'POST':
        codigo_evento=request.form['codigo_eve']
        nome_evento = request.form['nome_eve']
        data = request.form['data_eve']
        email = request.form["email_name"]
        if db.session.query(Modulo_Eventos).filter(and_(Modulo_Eventos.email_ == email , Modulo_Eventos.codigo_evento == codigo_evento , Modulo_Eventos.data_ == data, Modulo_Eventos.nome_evento==nome_evento)).count() > 0:
            db.session.query(Modulo_Eventos).filter(and_(Modulo_Eventos.email_ == email , Modulo_Eventos.codigo_evento == codigo_evento , Modulo_Eventos.data_ == data, Modulo_Eventos.nome_evento==nome_evento)).delete()
            db.session.commit()
            return render_template('deleta.html' , text='Evento excluído com sucesso!')
        else:
            return render_template('deleta.html'  ,  text='Dados não localizados!')
    return render_template('deleta.html'  )

if __name__ == '__main__':
    app.debug = False
    app.run()
