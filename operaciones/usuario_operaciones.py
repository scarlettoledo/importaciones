from conexion_bd import get_connection
from modelos.usuarios import Usuario   #en este archivo se tiene que realizar el proceso de encriptar la clave. 
from mysql.connector import Error
import hashlib
from modelos.usuarios import Usuario

@staticmethod
def disponibilidad_usuario(username): #verifica si un usuario ya existe en la base de datos
    connection = get_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query= " select *from usuarios where username = %s"
        cursor.execute(query, (username,))
        return cursor.fetchone () is not None #devuelve la primera coincidencia de username
    except Error as e:
        print(f"Error al verificar el usuario:{e}")
        return False
    finally:
        cursor.close()
        connection.close()
            
@staticmethod 
def encriptar_password(password):
    #función para encriptar la constraseña usando sha-256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def buscar_id_por_username(username):
    connection = get_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query="select id from usuarios where username = %s" #Se busca el id del usuario según el username
        cursor.execute(query, (username,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    except Error as e:
            print(f"Error en la base datos: {e}")
            return None
    finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class UsuarioOperaciones: 

    def insertar_usuario (usuarios):
        connection = get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            password_hash= encriptar_password(usuarios.password) #Se llama a la función para encriptar la password ingresada por el usuario

            query = """
            INSERT INTO usuarios (username, password_hash)
            VALUES(%s,%s) 
            """
            valores=(usuarios.username, password_hash)

            cursor.execute(query,valores)
            connection.commit()
            return True
                
        except Error as e:
                print(f"Error al crear usuario {e}.")
                return False
        finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        
    def listar_usuarios():
        connection = get_connection()
        if connection is None:
            return False       
        usuarios = []
            
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username from usuarios")
            for row in cursor.fetchall():
                usuario = Usuario(**row)
                usuarios.append(usuario)
                
            return usuarios
                
        except Error as e:
                print(f"Error al listar usuarios: {e}")
                return []
        finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        
    def actualizar_usuarios(username, nuevo_username, password):
        connection = get_connection()
        if connection is None:
            return False
               
        try:    
            id_usuario=buscar_id_por_username(username)

            if not id_usuario: #Si el usuario no es encontrado, se imprime ese mensaje
                print("Usuario no encontrado")
                return False
            
            password_hash = encriptar_password(password) #se encripta la contraseña que actualiza el usuario
            
            cursor= connection.cursor()
            query = "update usuarios set username= %s, password_hash= %s where id = %s" 
            cursor.execute(query, (nuevo_username, password_hash, id_usuario))
            connection.commit() #con esto se guardan todos los cambios realizados hasta este paso

            return cursor.rowcount == 1 #esto es para asegurar que sólo una fila sea afectada por las modificaciones   
                               
        except Error as e:
            print(f"Error al actualizar datos de Usuario : {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def eliminar_usuarios (id):
        connection= get_connection ()
        if connection is None:
            return False  

        try:
            cursor = connection.cursor()
            query = "delete from usuarios where id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar el Usuario : {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()