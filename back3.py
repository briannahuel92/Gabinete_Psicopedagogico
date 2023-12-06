'''
Programa para el BackEnd'''

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
import random

# Instalar con pip install Flask
from flask import Flask, jsonify, request
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
        print('Agregar: ', nombre, apellido, matricula, especialidad, imagen)
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
personal = Personal(host='localhost', user='root', password='', database='dbpersonal')

# Borramos la tabla de profesionales
''' INTENCIONALMENTE NO PONGO EL WHERE
    BORRO TODA LA TABLA DE PROFESIONALES '''
personal.cursor.execute("DELETE FROM profesionales")
personal.conn.commit()

# Fonoaudiologa
# Psicologa
# Psicopedagoga

personal.agregar_profesional(1, 'Ana', 'Alpha', 'MN-1001', 'Fonoaudiologa', '1.jpg')
personal.agregar_profesional(2, 'Beatriz', 'Bravo', 'MN-1002', 'Psicologa', '2.jpg')
personal.agregar_profesional(3, 'Clara', 'Charlie', 'MN-1003', 'Psicopedagoga', '3.jpg')
personal.agregar_profesional(**cPR3Crea(Personal._codigo_siguiente, 'Fonoaudiologa'))
personal.agregar_profesional(**cPR3Crea(Personal._codigo_siguiente, 'Psicologa'))
personal.agregar_profesional(**cPR3Crea(Personal._codigo_siguiente, 'Psicopedagoga'))


# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/imagenes/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
#RUTA_DESTINO = '/home/USUARIO/mysite/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los profesionales
#--------------------------------------------------------------------
#La ruta Flask /profesionales con el método HTTP GET está diseñada para proporcionar los detalles de todos los profesionales almacenados en la base de datos.
#El método devuelve una lista con todos los profesionales en formato JSON.
@app.route("/profesionales", methods=["GET"]) #GET: método para obtener respuestas a nuestras peticiones.
def listar_profesionales():
    profesionales = personal.listar_profesionales()
    return jsonify(profesionales)


#--------------------------------------------------------------------
# Mostrar un sólo profesional según su código
#--------------------------------------------------------------------
#La ruta Flask /profesionales/<int:codigo> con el método HTTP GET está diseñada para proporcionar los detalles de un profesional específico basado en su código.
#El método busca en la base de datos el profesional con el código especificado y devuelve un JSON con los detalles del profesional si lo encuentra, o None si no lo encuentra.
@app.route("/profesionales/<int:codigo>", methods=["GET"])
def mostrar_profesional(codigo):
    profesional = personal.consultar_profesional(codigo)
    if profesional:
        return jsonify(profesional), 201
    else:
        return "Profesional no encontrado.", 404


#--------------------------------------------------------------------
# Agregar un profesional
#--------------------------------------------------------------------
@app.route("/profesionales", methods=["POST"])
#La ruta Flask `/profesionales` con el método HTTP POST está diseñada para permitir la adición de un nuevo profesional a la base de datos.
#La función agregar_profesional se asocia con esta URL y es llamada cuando se hace una solicitud POST a /profesionales.
def agregar_profesional():
    #Recojo los datos del form
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    matricula = request.form['matricula']
    especialidad = request.form['especialidad']  
    imagen = request.files['imagen']
    nombre_imagen=""

    print("Por Agregar: ", nombre, apellido, matricula, especialidad, imagen)

    # Me aseguro que el producto exista
    profesional = personal.consultar_profesional(codigo)
    if not profesional: # Si no existe el profesional...
        # Genero el nombre de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.
        
        #Se agrega el profesional a la base de datos
        print("Nuevo Profesional no encontrado, Intento Agregar.")
        if personal.agregar_profesional(codigo, nombre, apellido,
            matricula, especialidad, imagen):
            print("Agregar Profesional devolvio TRUE.")
            imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

            #Si el profesional se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
            return jsonify({"mensaje": "Profesional agregado correctamente.", "imagen": nombre_imagen}), 201
        else:
            #Si el profesional no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
            return jsonify({"mensaje": "Error al agregar el profesional."}), 500

    else:
        #Si el profesional ya existe (basado en el código), se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 400 (Solicitud Incorrecta).
        return jsonify({"mensaje": "Profesional ya existe."}), 400


#--------------------------------------------------------------------
# Modificar un profesional según su código
#--------------------------------------------------------------------
@app.route("/profesionales/<int:codigo>", methods=["PUT"])
#La ruta Flask /profesionales/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un profesional existente en la base de datos, identificado por su código.
#La función modificar_profesional se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /profesionales/ seguido de un número (el código del profesional).
def modificar_profesional(codigo):
    #Se recuperan los nuevos datos del formulario
    nuevo_nombre = request.form.get("nombre")
    nuevo_apellido = request.form.get("apellido")
    nueva_matricula = request.form.get("matricula")
    nueva_especialidad = request.form.get("especialidad")
    imagen = request.files['imagen']

    # Procesamiento de la imagen
    nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    # Busco el profesional guardado
    profesional = profesional = personal.consultar_profesional(codigo)
    if profesional: # Si existe el profesional...
        imagen_vieja = profesional["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe la borro.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
    
    # Se llama al método modificar_profesional pasando el codigo del profesional y los nuevos datos.
    if personal.modificar_profesional(codigo, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_especialidad, nombre_imagen):
        #La imagen se guarda en el servidor.
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Profesional modificado"}), 200
    else:
        #Si el profesional no se encuentra (por ejemplo, si no hay ningún profesional con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Profesional no encontrado"}), 403


#--------------------------------------------------------------------
# Eliminar un profesional según su código
#--------------------------------------------------------------------
@app.route("/profesionales/<int:codigo>", methods=["DELETE"])
#La ruta Flask /profesionales/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un profesional específico de la base de datos, utilizando su código como identificador.
#La función eliminar_profesional se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /profesionales/ seguido de un número (el código del profesional).
def eliminar_profesional(codigo):
    # Busco el profesional en la base de datos
    profesional = personal.consultar_profesional(codigo)
    if profesional: # Si el profesional existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = profesional["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el profesional del listado de personal
        if personal.eliminar_profesional(codigo):
            #Si el profesional se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Profesional eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el profesional no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el profesional"}), 500
    else:
        #Si el profesional no se encuentra (por ejemplo, si no existe un profesional con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Profesional no encontrado"}), 404


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