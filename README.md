# Cálculo de Costo de Importaciones
Este proyecto fue realizado como parte de la asignatura Programación orientada a objeto, para calcular el costo de importaciones, considerando el **impuesto ad valorem**, el **IVA** (solicitados en Chile), y obteniendo el valor del dólar a través de una API externa.
## Descripción:
Este sistema calcula el costo total de las importaciones utilizando datos de la **API de Mindicador.cl**, que proporciona el valor del dólar actualizado en tiempo real. La aplicación también realiza los cálculos para obtener el costo final considerando los impuestos correspondientes.
## Herramientas utilizadas:
- **API Mindicador.cl**: Obtención del valor actualizado del dólar.
- **Postman**: Herramienta utilizada para realizar las peticiones HTTP a la API y probar el flujo de datos.
- **Lenguaje de programación**:Python
- **MySQL Workbench**: Base de datos utilizada para almacenar los datos relacionados con las importaciones, el valor del dólar y el resultado de los cálculos.
- **Máquina Virtual**: Se utilizó VirtualBox con Centos 8 para conectarse a la base de datos.
- **Impuestos**:
  - **Impuesto ad valorem**: Cálculo de impuesto de 6% sobre el valor del pedido
  - **IVA**: Cálculo del Impuesto al Valor Agregado (19%).
## ¿Cómo funciona?
1. Se hace una **petición HTTP** a la API de **Mindicador.cl** usando **Postman** para obtener el valor actual del dólar.
2. Se calcula el costo total de la importación sumando el **impuesto ad valorem** y el **IVA** al valor de la mercancía y al valor del envío desde el extranjero.
3. El resultado final es el costo de la importación en pesos chilenos.
