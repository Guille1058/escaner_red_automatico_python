import os          
import platform 
import socket     
import subprocess 
import sys         
import time    

#Función que detecta la IP privada del equipo.
def obtener_ip_local():
    # Creación de un socket UDP para obtener la IP local.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Intentamos conectar al DNS de Google en el puerto 80.
        s.connect(("8.8.8.8", 80))
        # Obtenemos la dirección IP asignada al socket.
        ip_local = s.getsockname()[0]
    except Exception:
        # Si lo anterior falla, la IP local se consigue mediante nombre de host.
        ip_local = socket.gethostbyname(socket.gethostname())
    finally:
        # Se cierra el socket.
        s.close()
    # La función devuelve la IP local.
    return ip_local

def obtener_segmento_red(ip):  
    #Devuelve la dirección de red convertida a string.
    return ".".join(ip.split(".")[:3])

#Función que intenta resolver el nombre de dispositivo (Hostname) asociado a una dirección IP.
def obtener_hostname(ip):
    # Configuramos un tiempo de espera máximo de 0.5 segundos.
    socket.setdefaulttimeout(0.5)
    try:
        # Se intenta llamar a la resolución inversa de DNS. Devuelve una tupla pero solo guardamos el nombre.
        nombre, _, _ = socket.gethostbyaddr(ip)
        return nombre
    except (socket.herror, socket.gaierror, socket.timeout):
        # Si el equipo no tiene nombre configurado o se agota el tiempo de respuesta, devuelve 'Desconocido'.
        return "Desconocido"

#Función que lanza un paquete ping a la dirección IP especificada y mide el tiempo de respuesta.
#La sintáxis del comando ping será diferente dependiendo del sistema operativo.
def comprobar_ping_con_latencia(ip_destino):
    # Detecta el nombre del sistema operativo y lo convierte a minúsculas.
    sistema = platform.system().lower()
    
    # Configuración de los argumentos del comando según el sistema detectado.
    # En cualquier caso, solo se envía un paquete ya que solo queremos medir la latencia y saber si el host está activo.
    if "windows" in sistema:
        # Windows: 1 paquete con 500ms de espera.
        comando = ["ping", "-n", "1", "-w", "500", ip_destino]
    else:
        # Resto: 1 paquete con 1 segundo de espera.
        comando = ["ping", "-c", "1", "-W", "1", ip_destino]
    
    # Se guarda el instante de tiempo exacto (en segundos con decimales) antes de lanzar el comando
    tiempo_inicio = time.time()
    try:
        # Se ejecuta el subproceso para ocultar la salida (output) y mensajes de error.
        resultado = subprocess.run(
            comando, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, 
            timeout=2.0                
        )
        # Guarda el instante de tiempo exacto tras finalizar el subproceso
        tiempo_fin = time.time()
        # Calcula la diferencia de tiempo y la multiplica por 1000 para pasarla a milisegundos (redondeando a 2 decimales)
        latencia_ms = round((tiempo_fin - tiempo_inicio) * 1000, 2)
        
        # Si el returncode es 0 el host responde, si es diferente no se puede conectar.
        if resultado.returncode == 0:
            return True, latencia_ms
        else:
            return False, 0.0
            
    #Manejo de errores: si el flujo falla se captura la excepción.
    except (subprocess.TimeoutExpired, Exception):
        return False, 0.0

#Función inicial del escaner.
def escanear_infraestructura():
    print("==================================================")
    print("   ESCÁNER AVANZADO: IPs, LATENCIA Y HOSTNAMES    ")
    print("==================================================")
    
    # Llamadas a las funciones para obtener IP local, segmento de red y hostname del equipo local.
    ip_propia = obtener_ip_local()
    segmento_base = obtener_segmento_red(ip_propia)
    hostname_propio = socket.gethostname()
    
    # Imprimimos por pantalla la información del entorno de red.
    print(f"[+] IP local detectada: {ip_propia} ({hostname_propio})")
    print(f"[+] Segmento objetivo: {segmento_base}.1 al {segmento_base}.254")
    print(f"[+] Entorno operativo: {platform.system()}")
    print("--------------------------------------------------")
    print("Escaneando red local... Por favor, espere.\n")
    
    # Todos los dispositivos activos se guardarán en esta lista. (cada entrada será un diccionario y las claves serán: "ip", "hostname" y "latencia")
    dispositivos_activos = []
    
    # Se genera un rango numérico que va del 1 al 254 (el número 255 se excluye por ser la dirección de broadcast)
    rango_ips = range(1, 255) 
    
    # Bucle que recorrerá cada una de las 254 IP.
    for host in rango_ips:
        # Guardamos la IP hipotética y la formateamos a cadena para la visualización.
        ip_a_probar = f"{segmento_base}.{host}"
        
        # Nuestra IP no la escaneamos.
        if ip_a_probar == ip_propia:
            print(f"   -> {ip_a_probar} [ACTIVO] | Hostname: {hostname_propio} (Este equipo) | Latencia: 0.0 ms")
            dispositivos_activos.append({
                "ip": ip_a_probar,
                "hostname": hostname_propio,
                "latencia": 0.0
            })
            continue
            
        # Enviamos el paquete ping y recibimos actividad y latencia.
        activo, latencia = comprobar_ping_con_latencia(ip_a_probar)
        
        # Si el dispositivo está activo, se imprime y se añade como entrada a la lista.
        # Si el dispositivo no responde, se muestra un punto que simula la barra de progreso.
        if activo:
            nombre_equipo = obtener_hostname(ip_a_probar)
            print(f"   -> {ip_a_probar} [ACTIVO] | Hostname: {nombre_equipo} | Latencia: {latencia} ms")
            dispositivos_activos.append({
                "ip": ip_a_probar,
                "hostname": nombre_equipo,
                "latencia": latencia
            })
        else:
            sys.stdout.write(".")
            sys.stdout.flush()

    # Generación del resumen por pantalla imprimiendo todos los datos como strings formateados, incluyendo los dispositivos activos encontrados.
    print("\n\n==================================================")
    print("               RESUMEN DEL ESCANEO                ")
    print("==================================================")
    print(f"Total de dispositivos activos detectados: {len(dispositivos_activos)}")
    print("--------------------------------------------------")
    for dev in dispositivos_activos:
         print(f"   - IP: {dev['ip']:<15} | Hostname: {dev['hostname']:<20} | Respuesta: {dev['latencia']} ms")
    print("==================================================")
    
    #Se escribe el informe generado en un archivo de texto (Ampliación Opcional).
    nombre_archivo = "dispositivos_activos.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("=== AUDITORÍA DE RED: DISPOSITIVOS DETECTADOS ===\n")
        f.write(f"Segmento evaluado: {segmento_base}.0/24\n")
        f.write(f"Total encontrados: {len(dispositivos_activos)}\n\n")
        f.write(f"{'DIRECCIÓN IP':<18}{'HOSTNAME / NOMBRE':<30}{'LATENCIA':<15}\n")
        f.write("-" * 63 + "\n")
        for dev in dispositivos_activos:
            f.write(f"{dev['ip']:<18}{dev['hostname']:<30}{str(dev['latencia']) + ' ms':<15}\n")
    print(f"\n[INFO] Reporte de auditoría guardado en: {nombre_archivo}")

    # Inicio del programa.
    try:
        escanear_infraestructura()
    except KeyboardInterrupt:
        # Si deseamos salir podemos hacerlo en cualquier momento con Ctrl+C.
        print("\n[!] Escaneo interrumpido de forma manual.")