from flask import Flask,jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Conexion a la base de datos
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

#Ruta para consulta general
@app.route("/", methods=['GET'])
def consulta_general():
    """
    consulta general del baul de contraseñas
    responses:
        200:
            descripcion: lista de registro
    """
    try:
        conn= conectar('localhost', 'root', '12345678', 'gestor_contrasena')
        cur= conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []
        for row in datos:
            dato = {'id_baul': row[0], 'plataforma':row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify ({'baul': data , 'mensaje': 'baul de contraseñas'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
#Ruta para consulta individual
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    """
    Consulta individial por ID
    parameters:
        -name:codigo
        in: path
        required: true
        type: integer
    responses:
        200:
            description: registro encontrado
    """
    try:
        conn = conectar('localhost', 'root', '12345678', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM baul where id_baul = '{codigo}'")
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos:
            dato = {'id_baul': datos[0], 'plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
            return jsonify({'baul': dato, 'mensaje': 'registro encontrado'})
        else:
            return jsonify({'mensaje': 'registro no encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'error'})
        
# Ruta para registro
@app.route("/registro/",methods=['POST'])
def registro():
    """
    Registrar nueva contraseña
    ---
    parameters:
        -name:body
        in:body
        required: true
        shema:
            type:object
            properties:
            plataforma:
                type: Strig
            Usuario:
                type: String
            clave:
                type: String
    response:
        200:
        description:Registro agregado
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = conectar('localhost', 'root', '12345678', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("INSERT INTO baul (plataforma, usuario, clave) VALUES (%s,%s,%s)",
        (plataforma, usuario, clave))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
#Ruta para eliminar registro
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    """
    eliminar registro por ID
    ---
    parameters:
        -name: codigo
        in: path
        required: true
        type: integer
    responses:
        200:
        description: Regristro eliminado
    """
    try:
        conn = conectar('localhost', 'root', '12345678', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s",(codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'error'})
    
#Ruta para actualizar registro
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    """
    Actualizar registro por ID
    ---
    parameters:
    name: codigo
    in: path
    required: true
    type: integer
    -name: body
    required: true
    shema:
        type: object
            properties:
                plataforma:
                    type: string
                usuario:
                    type:string
    reponses:
    200:
    description: registro Actualizado
    """

    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].enconde('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = conectar('localhost', 'root', '12345678', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("UPDATE baul SET plataforma = %s, usuario= %s, clave = %s, WHERE id_baul = %s", (plataforma, usuario, clave, codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
if __name__ == '__main__':
    app.run(debug=True)