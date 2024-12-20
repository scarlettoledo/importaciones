from datetime import datetime
class Importacion:
    def __init__(self, id = None, cantidad_unidades = 0, costo_unitario = 0.0, nombre_articulo = "", codigo_articulo = "",      
                nombre_proveedor = "", costo_envio = 0.0, valor_dolar = 0.0, costo_pedido_clp = 0.0, valor_cif_clp = 0.0, 
                tasa_importacion_clp = 0.0, valor_iva_clp = 0.0, total_impuestos_clp = 0.0, costo_total_clp = 0.0, costo_total_dolares = 0.0, fecha = None, usuario = "", id_usuario=None):    
        self.id = id
        self.cantidad_unidades = cantidad_unidades
        self.costo_unitario = costo_unitario
        self.nombre_articulo = nombre_articulo
        self.codigo_articulo = codigo_articulo
        self.nombre_proveedor = nombre_proveedor
        self.costo_envio = costo_envio      

        #Valor del dolar y valores calculados
        self.valor_dolar = valor_dolar
        self.costo_pedido_clp = costo_pedido_clp
        self.valor_cif_clp = valor_cif_clp
        self.tasa_importacion_clp = tasa_importacion_clp
        self.valor_iva_clp = valor_iva_clp
        self.total_impuestos_clp = total_impuestos_clp
        self.costo_total_clp = costo_total_clp
        self.costo_total_dolares = costo_total_dolares

        self.fecha = fecha if fecha else datetime.now ()
        self.usuario = usuario
        self.id_usuario = id_usuario

    def __str__(self):
        return f"Importacion(id = {self.id}, cantidad_unidades = {self.cantidad_unidades}, costo_unitario = {self.costo_unitario}, nombre_articulo = {self.nombre_articulo}, codigo_articulo = {self.codigo_articulo},  nombre_proveedor = {self.nombre_proveedor}, costo_envio = {self.costo_envio} , valor_dolar = {self.valor_dolar}, costo_pedido_clp = {self.costo_pedido_clp}, valor_cif_clp = {self.valor_cif_clp}, tasa_importacion__clp = {self.tasa_importacion_clp}, valor_iva_clp = {self.valor_iva_clp}, total_impuestos_clp = {self.total_impuestos_clp},costo_total_clp = {self.costo_total_clp}, costo_total_dolares = {self.costo_total_dolares},fecha = {self.fecha}, usuario = {self.usuario}, id_usuario = {self.id_usuario})"