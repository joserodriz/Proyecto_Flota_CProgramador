
import traceback

from flask import (Flask, Response, jsonify, redirect, render_template,
                   request, url_for)

import graficar
import movil

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///moviles.db"
movil.db.init_app(app)

@app.route("/")
def index():
    try:
        print("Renderizar index.html")
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/moviles")
def moviles():
    try:

        limit_str = str(request.args.get('limit'))
        offset_str = str(request.args.get('offset'))

        limit = 0
        offset = 0

        if(limit_str is not None) and (limit_str.isdigit()):
            limit = int(limit_str)

        if(offset_str is not None) and (offset_str.isdigit()):
            offset = int(offset_str)

        data = movil.report(limit=limit, offset=offset)

        data = movil.report()

        return render_template('tabla.html', data=data)
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/cargar", methods=['GET', 'POST'])
def cargar():
    if request.method == 'GET':
        try:
            return render_template('cargar.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            fecha = ""
            num_movil = 0
            tiempo = 0
            recaudado = 0

            fecha = str(request.form.get('fecha'))
            num_movil = str(request.form.get('num_movil'))
            tiempo = str(request.form.get('tiempo'))
            recaudado = str(request.form.get('recaudado'))

            if(fecha is None or num_movil is None or tiempo.isdigit() is False or recaudado.isdigit() is False):
                    return Response(status=400)

            if(int(num_movil) > 100 and int(num_movil) <= 999 and len(fecha) == 8):
                movil.insert(fecha, int(num_movil), int(tiempo), int(recaudado))

            else:
                return render_template('error.html')

            return redirect(url_for('moviles'))
        
        except:
            return jsonify({'trace': traceback.format_exc()})


@app.route("/grafica", methods=['GET', 'POST'])
def grafica():
    
     if request.method == 'GET':
        try:
            return render_template('resumir_recaudado.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

     if request.method == 'POST':        
        try:

            fecha = ""
            
            fecha = str(request.form.get('fecha'))
            x, y = movil.datos_grafica(fecha)

            eje_x = fecha
            eje_y = 'Recaudado'
            titulo = 'Grafico de Recaudado'

            image_html = graficar.graficar(x, y, eje_x, eje_y, titulo)

            return Response(image_html.getvalue(), mimetype='image/png')
        except:
            return jsonify({'trace': traceback.format_exc()})

@app.route("/resumen_movil", methods=['GET', 'POST'])
def resumen_movil():

    if request.method == 'GET':
        try:
            return render_template('resumir_movil.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            fecha = ""
            num_movil = 0

            fecha = str(request.form.get('fecha'))
            num_movil = str(request.form.get('num_movil'))

            if(fecha is None or num_movil is None or num_movil.isdigit() is False):
                return Response(status=400)

            data = movil.resumen(fecha, num_movil)

            return render_template('tabla_resumen.html', data=data)
        
        except:
            return jsonify({'trace': traceback.format_exc()})


@app.before_first_request
def before_first_request_func():
    movil.db.create_all()
    print("Base de datos generada")


if __name__ == '__main__':
    print('Inove@Server start!')

    app.run(host="127.0.0.1", port=5000)