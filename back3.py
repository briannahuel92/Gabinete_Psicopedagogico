'''
Programa para el BackEnd'''

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
import random

# Instalar con pip install Flask
from flask import Flask, jsonify
#from flask import Flask, request, jsonify, render_template


# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# Crea Profesional Random
from crea_prof_rand_3 import crea as cPR3Crea

# -------------------------------------------------------------------
# Definimos la clase Personal
# -------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Personal:
    #----------------------------------------------------------------
    _codigo_siguiente = 1
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS profesionales (
            codigo INT,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            matricula VARCHAR(20) NOT NULL,
            especialidad VARCHAR(100) NOT NULL,
            imagen_url VARCHAR(255) ) ''')

#            codigo INT,
#            descripcion VARCHAR(255) NOT NULL,
#            cantidad INT(4) NOT NULL,
#            precio DECIMAL(10, 2) NOT NULL,
#            imagen_url VARCHAR(255),
#            proveedor INT(3))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


    # ---------------------------------------------------------------
    # Método para agregar un profesional al catálogo
    # ---------------------------------------------------------------
    def agregar_profesional(self, codigo, nombre, apellido, matricula, especialidad, imagen):
        # Verificamos si el profesional ya existe en el catálogo
    #    self.cursor.execute(f"SELECT * FROM profesionales WHERE codigo = {codigo}")
    #    profesional_existe = self.cursor.fetchone()

    #    if profesional_existe:
    #        return False

        
        #Sino existe, agregamos el nuevo profesional a la tabla
        sql = f"INSERT INTO profesionales \
                (codigo, nombre, apellido, matricula, especialidad, imagen_url) \
                VALUES \
                ({Personal._codigo_siguiente}, '{nombre}', '{apellido}', '{matricula}', '{especialidad}', '{imagen}')"
        self.cursor.execute(sql)
        self.conn.commit()
        Personal._codigo_siguiente += 1
        return True



    # ---------------------------------------------------------------
    # Método para consultar un profesional por código
    # ---------------------------------------------------------------   
    def consultar_profesional(self, codigo):
        # Buscamos el profesional en la tabla
        self.cursor.execute(f"SELECT * FROM profesionales WHERE codigo = {codigo}")
        return self.cursor.fetchone() #fetchone devuelve un sólo registro


    # ---------------------------------------------------------------
    # Método para modificar los detalles de un profesional
    # ---------------------------------------------------------------
    def modificar_profesional(self, codigo, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_especialidad, nueva_imagen):

        sql = f"UPDATE profesionales SET \
                    nombre = '{nuevo_nombre}', \
                    apellido = {nuevo_apellido}, \
                    matricula = {nueva_matricula}, \
                    especialidad = {nueva_especialidad}, \
                    imagen_url = '{nueva_imagen}' \
                WHERE codigo = {codigo}"
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.rowcount > 0 #rowCount() devuelve el número de filas afectadas por la consulta


    # ---------------------------------------------------------------
    # Método para mostrar los detalles de un profesional por código
    # ---------------------------------------------------------------
    def mostrar_profesional(self, codigo):
        # Consultamos el profesional por su código
        profesional = self.consultar_profesional(codigo)
        if profesional:
            # Imprimimos los detalles del profesional
            print("-" * 50)
            print(f"Código......: {profesional['codigo']}")
            print(f"Nombre......: {profesional['nombre']}")
            print(f"Apellido....: {profesional['apellido']}")
            print(f"Matricula...: {profesional['matricula']}")
            print(f"Especialidad: {profesional['especialidad']}")
            print(f"Imagen......: {profesional['imagen']}")
            print("-" * 50)
        else:
            print("Profesional no encontrado.")


    # ---------------------------------------------------------------
    # Método para listar todos los profesionales en el catálogo
    # ---------------------------------------------------------------
    def listar_profesionales(self):
        self.cursor.execute("SELECT * FROM profesionales")
        profesionales = self.cursor.fetchall()
        return profesionales



    # ---------------------------------------------------------------
    # Método para eliminar un profesional por código
    # ---------------------------------------------------------------
    def eliminar_profesional(self, codigo):
        self.cursor.execute(f"DELETE FROM profesionales WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0 #rowCount() devuelve el número de filas afectadas por la consulta


# -------------------------------------------------------------------
# Ejemplo de uso de la clase Personal
# -------------------------------------------------------------------
personal = Personal(host='localhost', user='root', password='root', database='dbpersonal')

# Borramos la tabla de profesionales
''' INTENCIONALMENTE NO PONGO EL WHERE
    BORRO TODA LA TABLA DE PROFESIONALES '''
personal.cursor.execute("DELETE FROM profesionales")
personal.conn.commit()

# Fonoaudiologa
# Psicologa
# Psicopedagoga

personal.agregar_profesional(1, 'Ana', 'Alpha', 'MN-1001', 'Fonoaudiologa', '1.jpg')
personal.agregar_profesional(2, 'Beatriz', 'Bravo', 'MN-2002', 'Fonoaudiologa', '2.jpg')
personal.agregar_profesional(3, 'Clara', 'Charlie', 'MN-3003', 'Psicologa', '3.jpg')
# personal.agregar_profesional(**cPR3Crea(Personal._codigo_siguiente, 'Psicologa'))
# personal.agregar_profesional(**cPR3Crea(Personal._codigo_siguiente, 'Psicopedagoga'))
# personal.agregar_profesional(**cPR3Crea(Personal._codigo_siguiente, 'Psicopedagoga'))

@app.route("/profesionales", methods=["GET"]) #GET: método para obtener respuestas a nuestras peticiones.
def listar_profesionales():
    profesionales = personal.listar_profesionales()
    return jsonify(profesionales)


@app.route("/profesionales/<int:codigo>", methods=["GET"])
def mostrar_profesional(codigo):
    profesional = personal.consultar_profesional(codigo)
    if profesional:
        return jsonify(profesional), 201
    else:
        return "Profesional no encontrado.", 404


# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)


# personal.listar_profesionales()
# personal.mostrar_profesional(1)
# personal.eliminar_profeisional(2)
# personal.listar_profesionales()



#Consultamos un profesional y lo mostramos
# cod_prod = int(input("Ingrese el código profesional: "))
# profesional = personal.consultar_profesional(cod_prod)
# if profesional:
#     print(f"Producto encontrado: {profesional['codigo']} - {profesional['nombre']}")
# else:
#     print(f"Producto {cod_prod} no encontrado.")


#Modificar un profesional
# personal.modificar_profesional(1, 'Teclado Mecánico', 20, 34000, 'tecmec.jpg', 106)