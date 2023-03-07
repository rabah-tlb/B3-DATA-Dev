import sys
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os
import mysql.connector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
# db.init_app(app)

link = mysql.connector.connect(
    host='mysql',
    database = 'rna',
    user='root',
    password =""
  )
cur = link.cursor()

class Data(db.Model):
  __tablename__ = "data"
  id        = db.Column(db.Integer, primary_key=True)
  rna_id    = db.Column(db.String(20), nullable=True)
  rna_id_ex = db.Column(db.String(20), nullable=True)
  gestion   = db.Column(db.String(20), nullable=True)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/assos')
def assos():
  datas = Data.query.all()
  #for data in datas:
  #  print(f"{data.rna_id}")
  
  #stmt = select(Data)
  #result = db.session.execute(stmt)
  #for data in result.scalars():
  #  print(f"{data.rna_id}")

  return render_template('assos.html', datas=datas)
@app.route('/result', methods=["POST","GET"])

def result():
  rnaId = request.form.get("rnaId")
  rnaIdEx = request.form.get("rnaIdEx")
  gestion = request.form.get("gestion")
  # Ajout d'une ligne à une table
  add_line = "INSERT INTO data (rna_id, rna_id_ex, gestion) VALUES (%s, %s, %s)"
  cur.execute(add_line, (rnaId, rnaIdEx, gestion))
  link.commit()
  # Fermeture de la connexion
  cur.close()
  link.close()
  return redirect("/assos")

@app.route('/delete', methods=["POST","GET"])
def delete():
  rnaId = request.form.get("rnaIdDel")
  #créer un curseur de base de données pour effectuer des opérations SQL
  sql = "DELETE FROM data WHERE id = %s"
  idelement = (rnaId, )
  #exécuter le curseur avec la méthode execute() et transmis la requête SQL
  cur.execute(sql, idelement)
  #valider la transaction
  link.commit()
  return redirect("/assos")

@app.route('/alter', methods=["POST","GET"])
def alter():
  rnaId = request.form.get("rnaIdDel")
  #créer un curseur de base de données pour effectuer des opérations SQL
  sql = "UPDATE data WHERE id = %s"
  idelement = (rnaId, )
  #exécuter le curseur avec la méthode execute() et transmis la requête SQL
  cur.execute(sql, idelement)
  #valider la transaction
  link.commit()
  return redirect("/assos")

@app.route('/get_data_with_id')
def get_data_with_id():
    #print ("Hello",file=sys.stderr)
    rnaId = request.form.get("rnaIdModifier")
    rnaIdEx = request.form.get("rnaIdExModifier")
    gestion = request.form.get("gestionModifier")
    #créer un curseur de base de données pour effectuer des opérations SQL
    sql = "select * FROM data WHERE id = %s"
    idelement = (rnaId, )
    #exécuter le curseur avec la méthode execute() et transmis la requête SQL
    cur.execute(sql, idelement)
    #valider la transaction
    link.commit()
    return {'rna_id':'rnaId', 'rna_id_ex':'rnaIdEx', 'gestion':'gestion'  }



@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)

if __name__ == '__main__':
  app.run()