from datetime import datetime
import getpass
import hashlib
import jwt            
from dotenv import load_dotenv
import os
from operaciones.importacion_operaciones import ImportacionOperaciones
from operaciones.usuario_operaciones import UsuarioOperaciones, disponibilidad_usuario
from operaciones.importacion_operaciones import ImportacionOperaciones
from modelos.importacion import Importacion       
from modelos.usuarios import Usuario
from conexion_bd import get_connection

load_dotenv()

def menu_inicio():
    while True:
        print("\n=== Bienvenido al sistema de importaciones ===")
        print("\n1. Crear usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("\nSeleccionar una opción: ")
        if opcion == "1":
            insertar_usuario() 
        elif opcion == "2":
            token, usuario = login() 
            if token:
                menu_usuario(usuario)
            else:
                print("Autenticación fallida, intentar de nuevo.")
        elif opcion == "3":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Intentar nuevamente.")

def menu_usuario(usuario):
    while True:
        print("\n=== Menú del Usuario ===")
        print("1. Calcular una importación")
        print("2. Consultar historial de importaciones")
        print("3. Listar Usuarios")
        print("4. Actualizar Usuarios")
        print("5. Eliminar Usuarios")
        print("6. Salir al menú principal")
        
        opcion = input("\nSeleccionar una opción: ")
        
        if opcion == "1":
            crear_simulacion(usuario)  # Método para realizar calcular los costos de una importacion
        if opcion == "2":
            listar_importaciones()  # Método para ver el historial de importaciones
        if opcion == "3":
            listar_usuarios()
        if opcion == "4":
            actualizar_usuarios()
        if opcion == "5":
            eliminar_usuario()
        if opcion == "6":
            print("Saliendo al menú principal...")
            break

# Sistema de autenticación
def login():
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    # Hash de la contraseña
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password_hash = %s",
                      (username, password_hash))
        user = cursor.fetchone()
        if user:

            usuario = {
                'username': user ['username'],
                'id' : user ['id']
            } 

            # Generar token JWT
            token = jwt.encode(
                {'user_id': user['id'], 'username': user['username']},
                os.getenv('JWT_SECRET', 'your-secret-key'),
                algorithm='HS256'
            )
            return token, usuario
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def menu_principal():
    token = login()
    if not token:
        print("Autenticación fallida")
        return
    
def crear_simulacion(usuario):

    while True:
        try:
            cantidad_unidades= int(input("\nIngrese la cantidad de unidades                   : "))
            if cantidad_unidades <= 0:
                print("Debe ingresar un número mayor o igual 1")
                continue
            
            while True:
                try:
                    costo_unitario = float(input("Ingrese el costo de cada unidad                   : "))
                    if costo_unitario <= 0:
                        print("Debe ingresar un número mayor o igual 1")
                        continue
                    break
                except ValueError:
                    print("Ingrese un número válido")

            while True: 
                nombre_articulo = input("Ingrese el nombre del artículo                    : ")
                if not nombre_articulo:
                    print("Debe ingresar un parámetro")
                    continue
                break
            
            while True:
                codigo_articulo = input("Ingrese el código del artículo                    : ")
                if not codigo_articulo:
                    print("Debe ingresar un parámetro")
                    continue
                break

            while True:
                nombre_proveedor = input("Ingrese el nombre del proveedor                   : ")
                if not nombre_proveedor:
                    print("Debe ingresar un parámetro")
                    continue
                break
                
            while True:
                try: 
                    costo_envio = float(input("Ingrese el costo del envío en dólares hasta Chile : "))
                    if costo_envio <0: #en este caso se acepta un valor cero, en caso de que el proveedor no cobre el envío
                        print("El valor debe ser igual o mayor cero")        
                        continue
                    break
                except ValueError:
                    print("Ingrese un número válido")

            break

        except ValueError as e:
            print(f"Error en el formato de los datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
                    
    valor_dolar = ImportacionOperaciones.obtener_valor_dolar()
    if not valor_dolar:
        print("Error al obtener valor del dólar")
        return
        
    costo_envio_clp = costo_envio * valor_dolar
    costo_pedido_clp = round(ImportacionOperaciones.calcular_costo_pedido_CLP(cantidad_unidades, costo_unitario),2)
    valor_cif_clp = round(ImportacionOperaciones.calcular_valor_cif_CLP(costo_pedido_clp, costo_envio_clp),2)
    tasa_importacion_clp = round(ImportacionOperaciones.calcular_tasa_importacion_CLP(valor_cif_clp),2)
    valor_iva_clp = round(ImportacionOperaciones.calcular_iva_CLP(valor_cif_clp),2)
    costo_total_clp = round(valor_cif_clp + tasa_importacion_clp + valor_iva_clp,2)
    costo_total_dolares = round(costo_total_clp / valor_dolar,2)
    total_impuestos_clp = round(tasa_importacion_clp + valor_iva_clp,2)

    fecha_actual= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("\n=== Resultados de los costos de importación ===")
    print(f"\nValor del dolar a la fecha {fecha_actual}        : {valor_dolar}")
    print(f"Costo del pedido                             : {costo_pedido_clp}       CLP")
    print(f"Valor CIF                                    : {valor_cif_clp}       CLP")
    print(f"Costo de envío                               : {costo_envio_clp}       CLP")
    print(f"6% tasa de aduana                            : {tasa_importacion_clp}       CLP")
    print(f"19% IVA                                      : {valor_iva_clp}       CLP")
    print(f"Total de Impuestos                           : {total_impuestos_clp}       CLP")
    print(f"Costo total de la compra (CLP)               : {costo_total_clp}       CLP")
    print(f"Costo total de la compra (dólares)           : {costo_total_dolares}      Dólares")

    id_usuario = ImportacionOperaciones.obtener_id_usuario(usuario['username'])

    importacion = Importacion (
        cantidad_unidades = cantidad_unidades,
        costo_unitario = costo_unitario,
        nombre_articulo = nombre_articulo,
        codigo_articulo = codigo_articulo,
        nombre_proveedor = nombre_proveedor,
        costo_envio = costo_envio,
        valor_dolar = valor_dolar,
        costo_pedido_clp = costo_pedido_clp,
        valor_cif_clp = valor_cif_clp,
        tasa_importacion_clp = tasa_importacion_clp,
        valor_iva_clp = valor_iva_clp,
        total_impuestos_clp = total_impuestos_clp,
        costo_total_clp = costo_total_clp,
        costo_total_dolares = costo_total_dolares,
        fecha = fecha_actual,
        usuario = usuario,
        id_usuario = id_usuario
)
    if ImportacionOperaciones.ingresar_importacion(importacion, usuario, id_usuario):
        print("\nCálculo de importación registrado")
    else:
        print("Error al registrar información")

def listar_importaciones():
    try:
        cantidad_importaciones = int(input("Indique la cantidad de importaciones a consultar: "))
        
        if cantidad_importaciones <= 0:
            print("Ingrese un número mayor a cero.")
            return
        
        importaciones = ImportacionOperaciones.listar_importaciones(cantidad_importaciones)

        if not importaciones:
            print("No hay importaciones registradas")
            return
        
        print(f"\nSe encontraron {len(importaciones)} de las {cantidad_importaciones} importaciones solicitadas: ")
        print("\n=== Listado de Importaciones ===")
        for importacion in importaciones:
            print(f"\nID:                       {importacion.id}")
            print(f"Nombre del Artículo:        {importacion.nombre_articulo}")
            print(f"Código del Artículo:        {importacion.codigo_articulo}")
            print(f"Nombre del Proveedor:       {importacion.nombre_proveedor}")
            print(f"Cantidad de Unidades:       {importacion.cantidad_unidades}")
            print(f"Costo Unitario:             {importacion.costo_unitario}")
            print(f"Costo de Envío:             {importacion.costo_envio}")
            print(f"Valor Dólar:                {importacion.valor_dolar}")
            print(f"Costo Pedido (CLP):         {importacion.costo_pedido_clp}")
            print(f"Valor CIF (CLP):            {importacion.valor_cif_clp}")
            print(f"Tasa de Importación (CLP):  {importacion.tasa_importacion_clp}")
            print(f"IVA (CLP):                  {importacion.valor_iva_clp}")
            print(f"Costo Total (CLP):          {importacion.costo_total_clp}")
            print(f"Costo Total (USD):          {importacion.costo_total_dolares}")
            print(f"Fecha:                      {importacion.fecha.strftime('%d-%m-%Y')}")
            print(f"Usuario:                    {importacion.usuario}" )

    except ValueError:
        print("Ingrese un número válido")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def insertar_usuario():
    try:
        while True:
            username = input ("Ingrese nombre de usuario: ")
            if disponibilidad_usuario(username):
                print("Usuario no disponible.")
            else:                    
                password = input ("Ingrese password: ")
                usuarios = Usuario(username=username, password=password)

            if UsuarioOperaciones.insertar_usuario(usuarios):
                print("Usuario regitrado exitosamente.")
                break
            else:
                print("Error al registrar usuario.")

    except Exception as e:
            print(f"Error inesperado: {e}")

def listar_usuarios(): 
    usuarios= UsuarioOperaciones.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    print("\n=== Listado de usuarios ===")
    for usuario in usuarios:
        print(f"\n N° Usuario: {usuario.id}")
        print(f"Usuario: {usuario.username}")

def actualizar_usuarios():
    usuario=UsuarioOperaciones()
    print("\n=== Sistema para actualizar usuarios ===")
    username = input("Ingrese su usuario actual: ")
    nuevo_username = input("Ingrese su nuevo nombre de usuario: ")
    nueva_password = input("Ingrese la nueva contraseña: ")

    if UsuarioOperaciones.actualizar_usuarios(username, nuevo_username,nueva_password):
        print("Registros actualizados")
    else:
        ("No se pudo realizar la actualización")

def eliminar_usuario():
    print("\n=== Eliminar Usuario ===")
    id = input("Ingrese el id del usuario a eliminar: ")
    if UsuarioOperaciones.eliminar_usuarios(int(id)):
        print("Usuario eliminado correctamente.")
    else:
        print("El usuario no se ha podido eliminar.")
        

if __name__ == "__main__":
    menu_inicio()