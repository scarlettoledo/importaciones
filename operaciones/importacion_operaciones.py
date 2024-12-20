import requests
import datetime
from conexion_bd import get_connection
from modelos.importacion import Importacion
from mysql.connector import Error

tasa_importacion = 0.06
tasa_iva = 0.19

class ImportacionOperaciones ():
    #variable para almacenar el valor del dolar consultado y no consultarlo al realizar cada cálculo durante una simulación
    valor_dolar_dia_actual = None 

    @staticmethod
    def obtener_valor_dolar():
        try:
            #obtenemos la fecha del día actual en el que se realiza la simulacion de la importación y la transformamos en string
            fecha_str = datetime.datetime.now().strftime("%d-%m-%Y")
            #definimos la URL a la cual nos conectaremos para efectuar la solicitud (request)
            url = f"https://mindicador.cl/api/dolar/{fecha_str}"
            #ejecutamos una solicitud get al servidor y almacenamos la respuesta en response
            response = requests.get(url)
            #si el servicio entrega codigo http 200 (ok)
            if response.status_code == 200:
                #trasformamos el string de la respuesta a formato json
                data = response.json()
                #obtenemos el valor del dolar y lo retornamos
                ImportacionOperaciones.valor_dolar_dia_actual = data['serie'][0]['valor']
                return ImportacionOperaciones.valor_dolar_dia_actual
            else:
                raise Exception("Error al obtener valor de Dolar")
        except Exception as e:
            print(f"Error al consultar API: {e}")
            return None
        
    @staticmethod
    def ingresar_importacion (importacion, usuario):
        connection = get_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            
            sql = """INSERT INTO importaciones 
                     (cantidad_unidades, costo_unitario, nombre_articulo, 
                      codigo_articulo, nombre_proveedor, costo_envio, valor_dolar, 
                      costo_pedido_clp, valor_cif_clp, tasa_importacion_clp, valor_iva_clp, 
                      total_impuestos_clp, costo_total_clp, costo_total_dolares, fecha, usuario) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s )"""
            
            valores = (importacion.cantidad_unidades, importacion.costo_unitario,
                      importacion.nombre_articulo, importacion.codigo_articulo,
                      importacion.nombre_proveedor, importacion.costo_envio, 
                      importacion.valor_dolar, importacion.costo_pedido_clp, importacion.valor_cif_clp,
                      importacion.tasa_importacion_clp, importacion.valor_iva_clp,importacion.total_impuestos_clp, importacion.costo_total_clp, importacion.costo_total_dolares, importacion.fecha, usuario['username'])
            
            cursor.execute(sql, valores)
            connection.commit()
            return True
        except Error as e:
            print(f"Error al ingresar información a la base de datos: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def calcular_costo_pedido_CLP(cantidad_unidades, costo_unitario): #cálculo del costo del pedido en CLP
        if ImportacionOperaciones.valor_dolar_dia_actual is None:
            raise ValueError("El valor del dólar no ha sido establecido.")
        costo_pedido = cantidad_unidades*costo_unitario * ImportacionOperaciones.valor_dolar_dia_actual
        return costo_pedido
    
    #De aquí en adelante se trabajará con todos los valores en CLP
    @staticmethod
    def calcular_valor_cif_CLP(costo_pedido, costo_envio): #cálculo del valor cif en CLP, aquí se usarán los valores ya convertidos a CLP
        valor_cif = costo_pedido + costo_envio
        return valor_cif
    
    @staticmethod
    def calcular_tasa_importacion_CLP(valor_cif, tasa=tasa_importacion):#Calcular tasa de importacion en CLP
        tasa_importacion = valor_cif * tasa 
        return tasa_importacion
    
    @staticmethod
    def calcular_iva_CLP(valor_cif, iva=tasa_iva): #cálculo del IVA en CLP
        valor_iva = valor_cif * iva
        return valor_iva
    
    @staticmethod
    def listar_importaciones (cantidad_importaciones):
        connection = get_connection()
        importaciones = []    

        try:
            cursor = connection.cursor(dictionary=True)

            sql = """SELECT * FROM importaciones
                           order by fecha desc limit %s"""
            
            cursor.execute(sql, (cantidad_importaciones,))
            
            for row in cursor.fetchall():
                importacion = Importacion(**row)
                importaciones.append(importacion)
            return importaciones
        except Error as e:
            print(f"Error al listar importaciones: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
