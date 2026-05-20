## Ejercicio 2 - Escáner de Red Automático

Herramienta interna diseñada en Python para la fase de auditoría técnica que descubre dinámicamente qué hosts se encuentran levantados y operativos dentro de la LAN de la organización sin necesidad de configurar parámetros de forma manual.

### Librerías Nativas Utilizadas
* **`os`**: Permite interactuar con funciones del sistema operativo (no se usa directamente aquí, pero es útil para rutas).
* **`socket`**: Empleada para averiguar la interfaz de red activa de la máquina y deducir la IP local de forma transparente.
* **`platform`**: Utilizada para identificar si el código corre bajo entornos Windows, Linux o macOS, permitiendo modificar al vuelo las banderas (flags) del comando ping.
* **`subprocess`**: Conecta la lógica de Python con la terminal del sistema operativo subyacente para ejecutar de forma silenciosa el comando `ping`.
* **`sys`**: Proporciona funciones y variables del intérprete de Python (usado aquí para limpiar el buffer de pantalla y generar la barra de progreso).
* **`time`**: Permite realizar mediciones de tiempo (importante para calcular la latencia en milisegundos).

### Instrucciones de Ejecución
Asegúrate de ejecutar la consola con privilegios de administrador si tu sistema operativo lo requiere para el envío de paquetes ICMP raw.
```bash
python escaner_red.py

### Características Avanzadas Implementadas (Extra)
* **Medición de Latencia Activa**: El script calcula en tiempo real el tiempo de respuesta (en milisegundos) de cada host mediante marcas temporales de la librería nativa `time`, ofreciendo visibilidad sobre la congestión o la velocidad de respuesta de cada nodo de la infraestructura.
* **Persistencia en archivo**: Exportación automática de la lista estructurada de IPs junto a sus respectivas latencias a un documento de texto plano (`dispositivos_activos.txt`).

### Ejemplo de Salida Esperada con Latencia
```text
==================================================
      ESCÁNER DE RED AUTOMÁTICO CON LATENCIA      
==================================================
[+] IP de tu equipo detectada: 192.168.1.15
[+] Segmento de red a escanear: 192.168.1.1 al 192.168.1.254
[+] Sistema Operativo detectado: Windows
--------------------------------------------------
Escaneando red local... Por favor, espere.

   -> 192.168.1.1 [ACTIVO] - Latencia: 4.21 ms
...   -> 192.168.1.15 [ACTIVO] (Este equipo) - Latencia: 0.0 ms
.......   -> 192.168.1.34 [ACTIVO] - Latencia: 45.12 ms
........................................................

==================================================
               RESUMEN DEL ESCANEO                
==================================================
Total de dispositivos activos detectados: 3
--------------------------------------------------
   - 192.168.1.1 (Tiempo de respuesta: 4.21 ms)
   - 192.168.1.15 (Tiempo de respuesta: 0.0 ms)
   - 192.168.1.34 (Tiempo de respuesta: 45.12 ms)
==================================================
