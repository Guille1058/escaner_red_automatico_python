## Ejercicio 2 - Escáner de Red Automático

Herramienta interna diseñada en Python para la fase de auditoría técnica que descubre dinámicamente qué hosts se encuentran levantados y operativos dentro de la LAN de la organización sin necesidad de configurar parámetros de forma manual.

### Librerías Nativas Utilizadas
* **`os`**: Permite interactuar con funciones del sistema operativo (no se usa directamente aquí, pero es útil para rutas).
* **`socket`**: Empleada para averiguar la interfaz de red activa de la máquina y deducir la IP local de forma transparente.
* **`platform`**: Utilizada para identificar si el código corre bajo entornos Windows, Linux o macOS, permitiendo modificar al vuelo las banderas (flags) del comando ping.
* **`subprocess`**: Conecta la lógica de Python con la terminal del sistema operativo subyacente para ejecutar de forma silenciosa el comando `ping`.
* **`sys`**: Proporciona funciones y variables del intérprete de Python (usado aquí para limpiar el buffer de pantalla y generar la barra de progreso).
* **`time`**: Permite realizar mediciones de tiempo (importante para calcular la latencia en milisegundos).

### Características Avanzadas Implementadas (Extra)
* **Medición de Latencia Activa**: El script calcula en tiempo real el tiempo de respuesta (en milisegundos) de cada host mediante marcas temporales de la librería nativa `time`, ofreciendo visibilidad sobre la congestión o la velocidad de respuesta de cada nodo de la infraestructura.
* **Persistencia en archivo**: Exportación automática de la lista estructurada de IPs junto a sus respectivas latencias a un documento de texto plano (`dispositivos_activos.txt`).

### Instrucciones de Ejecución
Asegúrate de ejecutar la consola con privilegios de administrador si tu sistema operativo lo requiere para el envío de paquetes ICMP raw.

```bash
python escaner_red.py

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
```

### Cómo funciona (paso a paso)

El escáner realiza las siguientes acciones para descubrir dispositivos en la LAN y medir su latencia:

1. Detecta la IP local del equipo ejecutando `obtener_ip_local()`.
   - Crea un socket UDP y se conecta de forma no intrusiva a un servidor público (8.8.8.8) para obtener la IP asociada a la interfaz activa.
   - Si falla, utiliza la resolución por nombre de host como método alternativo.

2. Determina el segmento de red con `obtener_segmento_red(ip)`.
   - Se construye el prefijo de red (por ejemplo `192.168.1`) a partir de la IP local para escanear de `.1` a `.254`.

3. Para cada dirección IP del rango objetivo ejecuta `comprobar_ping_con_latencia(ip)`.
   - Lanza un único ping adaptando las opciones según el sistema operativo (Windows/Linux/MacOS).
   - Mide el tiempo transcurrido alrededor de la llamada al comando para calcular la latencia en milisegundos.
   - Interpreta el código de salida del comando para decidir si el host está activo.

4. Si un host responde, intenta resolver su nombre de equipo con `obtener_hostname(ip)` (resolución DNS inversa).

5. Presenta salida por pantalla en tiempo real mostrando IPs activas, hostname y latencia.
   - Para hosts inactivos muestra puntos (`.`) que simulan una barra de progreso.

6. Guarda un informe final en `dispositivos_activos.txt` con una tabla que incluye IP, hostname y latencia.

7. Permite interrupción manual con `Ctrl+C` para detener el escaneo en cualquier momento.

Con este flujo el script ofrece una visión rápida y reproducible de qué equipos están operativos en la subred local y cuál es su tiempo de respuesta.

## Archivos principales de proyecto

- [main.py]: Lógica del programa.
- [README.md]: Documentación del proyecto (este archivo).
