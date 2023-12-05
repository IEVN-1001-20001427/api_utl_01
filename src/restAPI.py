from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

app=Flask(__name__)
cn = MySQL(app)
CORS(app)


#Login
@app.route('/login', methods=['POST'])
def login():
    try:
        cursor=cn.connection.cursor()
        sql="""SELECT * FROM `usuarios` WHERE `correo` = '{0}' AND `contrasena` = '{1}' """.format(request.json['correo'],request.json['contrasena'])
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos:
            usr={'id_user':datos[0],'correo':datos[1],'contrasena':datos[2]}
            return jsonify(usr)
        else:
            return "Registro no encontrado"
    except Exception as ex:
        return ex
    
@app.route('/find/<id>', methods=['GET'])
def find(id):
    try:
        return jsonify(search(id, 'id_admin', 'administrador'))
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
#


#seach for ticket, product, client, admin and details
def search(id, field, table):
    try:
        cursor=cn.connection.cursor()
        sql='select * from {} where {} = {}'.format(table, field, id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos:
            if table == "producto":
                producto={'id_producto':datos[0],'nombre':datos[1],'precio_siva':datos[2],'descripcion':datos[3],'inventario':datos[4],'imagen':datos[5],'marca':datos[6],'provedor':datos[7]}
                return producto
            elif table == "factura":
                factura={'id_factura':datos[0],'fecha':datos[1],'id_user':datos[2],'precio':datos[3],'iva':datos[4],'total':datos[5]}
                return factura
            elif table == "lista_deseo":
                lista_deseo={'id_deseo':datos[0],'id_user':datos[1]}
                return lista_deseo
            elif table == "administrador":
                administrador={'id_admin':datos[0],'nombre':datos[1],'ap_paterno':datos[2],'ap_materno':datos[3],'telefono':datos[4],'id_user':datos[5]}
                return administrador
            elif table == "cliente":
                cliente={'id_cliente':datos[0],'nombre':datos[1],'ap_paterno':datos[2],'ap_materno':datos[3],'telefono':datos[4],'num_tarjeta':datos[5],'id_user':datos[6]}
                return cliente
        else:
            return "Registro no encontrado"
    except Exception as ex:
        return ex


def detailSearch(id, field, table):
    try:
        cursor=cn.connection.cursor()
        sql='select * from {} where {} = {}'.format(table, field, id)
        cursor.execute(sql)
        datos=cursor.fetchall()
        result=[]
        if table == "det_compra":
            for f in datos:
                item={'id_factura':f[0],'id_producto':f[1],'cantidad':f[2],'precio':f[3]}
            result.append(item)
        elif table == "det_deseo":
            for f in datos:
                item={'id_producto':f[0],'id_deseo':f[1]}
            result.append(item)
        return jsonify(result)
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
#


#PRODUCTS
@app.route('/products', methods=['GET'])
def listProducts():
    try:
        cursor=cn.connection.cursor()
        sql='select * from producto'
        cursor.execute(sql)
        datos=cursor.fetchall()
        products=[]
        for f in datos:
            product={'id_producto':f[0],
                    'nombre':f[1],
                    'precio_siva':f[2],
                    'descripcion':f[3],
                    'inventario':f[4],
                    'imagen':f[5],
                    'marca':f[6],
                    'provedor':f[7]}
            products.append(product)
        return jsonify(products)
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})


@app.route('/product/<id>', methods=['GET'])
def searchProduct(id):
    try:
        return jsonify(search(id, 'id_producto', 'producto'))
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})


@app.route('/product/<id>', methods=['PUT'])
def updateProduct(id):
    try:
        if search(id, "id_producto", "producto") != "Registro no encontrado":
            cursor=cn.connection.cursor()
            sql="""UPDATE `producto` SET `nombre` = '{1}', `precio_siva` = '{2}', `descripcion` = '{3}',
            `inventario` = '{4}', `imagen` = '{5}', `marca` = '{6}', `provedor` = '{7}' WHERE id_producto = {0} """.format(id,request.json['nombre'],request.json['precio_siva'],request.json['descripcion'],request.json['inventario'],request.json['imagen'],request.json['marca'],request.json['provedor'])
            cursor.execute(sql)
            cn.connection.commit()
            return jsonify({'msg': 'Register updated', 'done':True})
        else:
            return jsonify({'msg': 'Error this doesnt exist', 'done':False})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})


@app.route('/product/<id>', methods=['DELETE'])
def deleteProduct(id):
    try:
        if search(id, "id_producto", "producto") != "Registro no encontrado":
            cursor=cn.connection.cursor()
            sql=('DELETE FROM producto WHERE id_producto = {}'.format(id))
            cursor.execute(sql)
            cn.connection.commit()
            return jsonify({'msg': 'Register deleted', 'done':True})
        else:
            return jsonify({'msg': 'Error this doesnt exist', 'done':False})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})


@app.route('/product', methods=['POST'])
def newProduct():
    try:
        if search(request.json['id_producto'], "id_producto", "producto") != "Registro no encontrado":
            return jsonify({'msg': 'Error this already exist', 'done':False})
        else:
            cursor=cn.connection.cursor()
            sql="""INSERT INTO `producto` (id_producto, nombre, precio_siva, descripcion, inventario, imagen, marca, provedor) VALUES
            ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')""".format(request.json['id_producto'],request.json['nombre'],request.json['precio_siva'],request.json['descripcion'],request.json['inventario'],request.json['imagen'],request.json['marca'],request.json['provedor'])
            cursor.execute(sql)
            cn.connection.commit()
            return jsonify({'msg': 'new register signed on the list', 'done':True})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
#


#WISHES
def createListWish(id):
    try:
        cursor=cn.connection.cursor()
        sql="""INSERT INTO `lista_deseo` (`id_deseo`, `id_user`) VALUES ('{0}', '{1}') """.format(id, id)
        cursor.execute(sql)
        cn.connection.commit()
        return jsonify({'msg': 'wish list created', 'done':True})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
    

@app.route('/wish/<id>', methods=['GET'])
def detailWish(id):
    try:
        return jsonify({'contenido':detailSearch(id, 'id_deseo', 'det_deseo'),'msg':'Registers found','done':True})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
    


#


#TICKETS
@app.route('/tickets', methods=['GET'])
def listTickets():
    try:
        cursor=cn.connection.cursor()
        sql='select * from factura'
        cursor.execute(sql)
        datos=cursor.fetchall()
        facturas=[]
        for f in datos:
            factura={'id_factura':datos[0],'fecha':datos[1],'id_user':datos[2],'precio':datos[3],'iva':datos[4],'total':datos[5]}
            facturas.append(factura)
        return jsonify(facturas)
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
    
    
@app.route('/ticket/<id>', methods=['GET'])
def detailTicket(id):
    try:
        return jsonify(detailSearch(id, 'id_factura', 'det_compra'))
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
#


#USERS
@app.route('/newUser', methods=['POST'])
def newUser():
    try:
        if search(request.json['id_user'], "id_user", "usuarios") != "Registro no encontrado":
            return jsonify({'msg': 'Error this already exist', 'done':False})
        else:
            cursor=cn.connection.cursor()
            sql="""INSERT INTO `usuarios` (`id_user`, `correo`, `contrasena`) VALUES
            ('{0}','{1}','{2}')""".format(request.json['id_user'],request.json['correo'],request.json['contrasena'])
            cursor.execute(sql)
            cn.connection.commit()


            cursor=cn.connection.cursor()
            createListWish(request.json['id_user'])
            sql="""INSERT INTO `cliente` (`id_cliente`, `nombre`, `ap_paterno`, `ap_materno`, `telefono`, `num_tarjeta`, `id_user`) VALUES
            ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(request.json['id_user'],request.json['nombre'],request.json['ap_paterno'],request.json['ap_materno'],request.json['telefono'],request.json['num_tarjeta'],request.json['id_user'])
            cursor.execute(sql)
            cn.connection.commit()

            return jsonify({'msg': 'new user has signed on the list', 'done':True})
    except Exception as ex:
        return jsonify({'msg': 'Error {}'.format(ex), 'done':False})
#


#ERRORS
def pagina_no_encontrada(err):
    return jsonify({'msg': 'it seems that your URL has something wrong', 'done':False})
#


#EXECUTION
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()
#