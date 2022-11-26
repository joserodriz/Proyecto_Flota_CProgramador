

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Movil(db.Model):
    __tablename__ = "moviles"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String)
    num_movil = db.Column(db.Integer)
    tiempo = db.Column(db.Integer)
    recaudado = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Movil:{self.fecha} moviles {self.num_movil}"


def insert(fecha, numero, tiempo, recaudado):
    
    moviles = Movil(fecha=fecha, num_movil=numero, tiempo=tiempo, recaudado=recaudado)

    db.session.add(moviles)
    db.session.commit()


def report(limit=0, offset=0):

    query = db.session.query(Movil)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    for moviles in query:
        json_result = {'fecha': moviles.fecha, 'num_movil': moviles.num_movil, 'tiempo': moviles.tiempo, 'recaudado': moviles.recaudado}
        json_result_list.append(json_result)

    return json_result_list

def datos_grafica():
   
    query = db.session.query(Movil).filter(Movil.recaudado).filter(Movil.id)
    query_results = query.all()

    if query_results is None or len(query_results) == 0:
        
        return []

    recaudado = [x.recaudado for x in query_results]
    id = [x.id for x in query_results]

    return id, recaudado

def resumen(fecha_consulta, numero_movil):
   
    query = db.session.query(Movil).filter(Movil.fecha_consulta).filter(Movil.numero_movil).filter(Movil.recaudado).filter(Movil.tiempo)
    query_results = query.all()

    if query_results is None or len(query_results) == 0:
        
        return []

    fecha = fecha_consulta
    numero = numero_movil
    recaudado = sum([x.recaudado for x in query_results])
    tiempo = sum([x.tiempo for x in query_results])

    resumen = {'fecha': fecha ,'numero_mov': numero, 'recaudado': recaudado, 'tiempo': tiempo}

    return resumen


if __name__ == "__main__":

    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdatabase.db"
    
    db.init_app(app)
    app.app_context().push()

    db.create_all()

    db.session.remove()
    db.drop_all()