from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)
cn = MySQL(app)

def seachAlumno(matricula):
    try:
        cursor=cn.connection.cursor()
        sql='select * from alumnos where matricula = {}'.format(matricula)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos:
            alumno={'matricula':datos[0],
                    'nombre':datos[1],
                    'apaterno':datos[2],
                    'amaterno':datos[3],
                    'correo':datos[4]}
            return alumno
        else:
            return "alumno no encontrado"
    except Exception as ex:
        return None

@app.route('/alumnos', methods=['GET'])
def listAlumnos():
    try:
        cursor=cn.connection.cursor()
        sql='select * from alumnos'
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos=[]
        for f in datos:
            alumno={'matricula':f[0],
                    'nombre':f[1],
                    'apaterno':f[2],
                    'amaterno':f[3],
                    'correo':f[4]}
            alumnos.append(alumno)
            print(alumnos)
        return jsonify({'alumnos':alumnos,'msg':'list of students','done':True})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})

@app.route('/alumno/<matricula>', methods=['GET'])
def showAlumno(matricula):
    try:
        return jsonify({'alumno':seachAlumno(matricula),'msg':'the student with the matricula {}'.format(matricula),'done':True})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})

@app.route('/newAlumno', methods=['POST'])
def newAlumno():
    try:
        if seachAlumno(request.json['matricula']) != "alumno no encontrado":
            return jsonify({'msg': 'Error this student already exist', 'done':False})
        else:
            cursor=cn.connection.cursor()
            sql="""insert into alumnos(matricula,nombre,apaterno,amaterno,correo)
            values('{0}','{1}','{2}','{3}','{4}')""".format(request.json['matricula'],request.json['nombre'],request.json['apaterno'],request.json['amaterno'],request.json['correo'])
            cursor.execute(sql)
            cn.connection.commit()
            return jsonify({'msg': 'student signed on the list', 'done':True})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})

def pagina_no_encontrada(err):
    return "<h1>PAGINA NO ENCONTRADA</h1>"

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()