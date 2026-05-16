# TP4: Infraestructura de servicios web con perspectiva de redes

### Asignatura: Redes de Computadoras

**Facultad de Ciencias Exactas, Físicas y Naturales (UNC)**

---

* **Grupo:** The Lords of Pings
* **Profesores:** Facundo Oliva Cuneo y Santiago Martin Henn

---

### Integrantes y Contacto

| Nombre y Apellido | Correo Electrónico |
| :--- | :--- |
| **Pablo Castilla** | _pablo.castilla@mi.unc.edu.ar_ |
| **Javier A. Fatu** | _javier.fatu@mi.unc.edu.ar_ |
| **Enzo L. Laura Surco** | _enzo.laura.surco@mi.unc.edu.ar_ |
| **Saqib D. Mohammad Cabrejos** | _saqib.mohammad@mi.unc.edu.ar_ |


## Desarrollo

### 1) Sabemos que la información viaja a través de internet “empaquetada” según el protocolo de capa de transporte que utilicemos. Sin embargo, dentro de la carga útil de estos paquetes, la información debe estar organizada para poder realizar una interpretación correcta de su significado.

#### a) ¿Qué es la serialización en redes de computadoras?

La serialización es el proceso de convertir una estructura de datos compleja o el estado de un objeto (que vive en la memoria RAM de tu programa, con sus punteros y referencias) en un formato lineal estándar que pueda ser fácilmente transmitido a través de una red o almacenado en un archivo.

Imagina que tienes un mueble armado en tu casa (tu objeto en memoria). No puedes enviarlo por correo así como está porque ocupa mucho espacio y tiene una forma irregular. La serialización equivale a desarmar ese mueble, guardar las piezas de forma ordenada en una caja plana (secuencia de bytes) y enviarlo. El destinatario, al recibir la caja, hace el proceso inverso (deserialización) para volver a armar el mueble y poder usarlo.

Dado que los cables de red solo entienden un flujo de bits/bytes, la serialización es el puente que permite que un programa escrito en Python pueda enviarle un diccionario complejo a un programa escrito en C++ y que ambos se entiendan perfectamente.

#### b) ¿Cuál es la diferencia entre serialización binaria y no binaria? Buscar ejemplos, ventajas y desventajas de cada una.

La diferencia principal radica en cómo se codifican esos bytes resultantes. La serialización no binaria (también llamada basada en texto) prioriza que el mensaje sea legible por humanos, mientras que la binaria prioriza la eficiencia y velocidad de las máquinas.

Aquí tienes la comparativa detallada:

Serialización No Binaria (Basada en Texto)

* Codifica los datos utilizando caracteres estándar (generalmente en ASCII o UTF-8).

* Ejemplos comunes: JSON, XML, YAML.

**Ventajas:**

Legibilidad humana: Si interceptas el paquete en la red o lo imprimes en consola, puedes leer y entender exactamente qué datos viajan (muy útil para depurar errores).

Universalidad: Prácticamente todos los lenguajes de programación tienen librerías nativas o muy accesibles para procesar texto plano.

**Desventajas:**

* Mayor tamaño (Overhead): Ocupa mucho más espacio en la red porque requiere caracteres extra para la estructura (como las llaves {} y comillas "" en JSON).

* Lentitud de procesamiento: Convertir texto plano a tipos de datos nativos (como transformar la cadena de texto "12345" a un número entero real en la memoria) consume más ciclos de CPU.

Serialización Binaria

* Codifica los datos directamente en un formato compacto de ceros y unos, optimizado matemáticamente, sin preocuparse por representar caracteres legibles.

* Ejemplos comunes: Protocol Buffers (Protobuf de Google), MessagePack, BSON (usado por MongoDB), FlatBuffers.

**Ventajas:**

* Eficiencia de tamaño: El payload es muchísimo más pequeño. Un número entero gigante viaja simplemente como sus 4 u 8 bytes correspondientes, en lugar de un carácter por cada dígito.

* Alta velocidad: El proceso de serializar y deserializar es rapidísimo porque los datos ya vienen en un formato muy cercano a como la CPU los maneja en memoria.

**Desventajas:**

* Ilegible para humanos: Si miras el paquete en crudo, solo verás caracteres basura o símbolos extraños. Requiere herramientas especiales para decodificarlo y leerlo.

* Mayor complejidad de implementación: Generalmente requiere definir un "esquema" o contrato estricto previo entre el cliente y el servidor para que ambos sepan exactamente en qué byte empieza y termina cada variable.

### 2) Desplegaremos un servidor TCP multi-hilo: 

**- Se realiza esta actividad de forma presencial, lo desplegamos en una PC virtual en clases que usaremos entre todos.**

#### a) Serializaremos nuestros paquetes en JSON

Se crea entonces un archivo al cual llamaremos paquete.json, el mismo debe tener un contenido similar a:

```
{
"group": "The Lords of Pings",
"payload": "Jueves 14 de Mayo TP4"
}
```
Las claves del paquete JSON group y payload deben ser nombradas de esa forma debido a que el servidor solo esta programado para recibir la infromacion de esa forma.

#### Y lo enviaremos utilizando PacketSender; 

#### Se recomienda tildar “persistent TCP” (puede no ser necesario en algunos casos) así no se abre y cierra conexión cada que se envía un mensaje:
Nombramos nuestro paquete, cargamos el paquete.json en ASCII y nuestro profesor de la materia quien levanto el servidor, nos provee la IP y el numero de puerto: 34.68.162.122 y 5050 respectivamente

![image](https://hackmd.io/_uploads/BycvB5mkMx.png)

Podemos verficar el contenido de nuestro paquete:

![image](https://hackmd.io/_uploads/Sy8YB5Qyfx.png)

Y aqui verificamos correctamente que el paquete fue recibido por el servidor quien tambien nos envia mensajes de respuesta o "bienvenida".

![image](https://hackmd.io/_uploads/ByM41Arkzg.png)
![image](https://hackmd.io/_uploads/BkSr1CH1zl.png)


### 3) Programaremos ahora una aplicación de cliente que nos permita enviar mensajes al servidor a través de una consola.

En esta etapa nuestro grupo como cliente escribio un pequeño script en python para poder, con ayuda de las librerias socket y json(para serializar la informacion)


#### a) Nuestro cliente deberá poder configurarse con la IP y puerto de destino del servidor, estableciendo conexión con el mismo.

```
import socket
import json
.
.
.
HOST = "34.68.162.122"  
PORT = 5050          

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
```

![image](https://hackmd.io/_uploads/HkLNo57yzx.png)

#### b) Nuestro cliente deberá serializar la información previo al envío de la misma, en el formato que el servidor admite.

Como sabemos ya el servidor acepta la informacion serializada en JSON por ende haremos uso de la libreria JSON en python para darle un formato al mensaje previo al envio.

```
message = {
        "group": "The Lords of Pings",
        "payload": user_input_encrypted.decode("utf-8")
    }

    client.sendall(json.dumps(message).encode("utf-8"))
```

![image](https://hackmd.io/_uploads/Skdri5XJfe.png)

#### c) Ejecutar nuestro cliente y verificar que los mensajes enviados lleguen correctamente al servidor.

NUestro esta configurado para que primero establezca una conexion con el servidor y en ese momemtno podemos enviar un mensaje cualquiera por consola que sera serializado en JSON y pueda ser recibido por el servidor. Lo que se busco es una interaccion Cliente-Servidor tipo chat(para asi tener una aproximacion al proximo trabajo practico).

![image](https://hackmd.io/_uploads/BJeKIs5QkMe.png)

![image](https://hackmd.io/_uploads/B1Lti5QJGl.png)

Redactamos algunos mensajes de paz y amor para el servidor.

![image](https://hackmd.io/_uploads/rJZ3jcX1Mx.png)

Comprobamos la recepcion mediante la terminal del servidor y podemos observar que los mensajes son recibidos y procesados por el servidor y por ende nos respondera con mensajes de bienvenida.

![WhatsApp Image 2026-05-14 at 4.00.25 PM](https://hackmd.io/_uploads/ryh4MkIkMx.jpg)



### 4) Vamos a imbuir un poco de seguridad en nuestro sistema. Investiga e implementa alguna técnica de encriptación que te guste e implementar para cifrar la payload, SOLO LA PAYLOAD, de tu mensaje.

EL sistema que se decidio implementar es AES, con encriptacion simetrica de nuestro payload. Para nuestro codigo en python instalaremos la librearia cryptography y haremos uso de "fernte" para la generacion de la clave y el cifrado del payload en cada mensaje al cual enviaremos.

Usaremos el comando de instalacion dentro de una libraria virtual:
```
pip install cryptography
```

#### a) Implementa el cifrado en el lado del cliente.

Y nuestro codigo ya con la libreria implementada seria:

```
import socket
import json
from cryptography.fernet import Fernet


clave = Fernet.generate_key()
cipher = Fernet(clave)

HOST = "34.68.162.122"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    user_input = input("Ingresa tu mensaje (o escribe 'adios' para salir): ")
    user_input_encrypted = cipher.encrypt(user_input.encode("utf-8"))

    if user_input.strip().lower() == 'adios':
        print("Cerrando conexión...")
        client.close()
        break

    message = {
        "group": "The Lords of Pings",
        "payload": user_input_encrypted.decode("utf-8")
    }

    client.sendall(json.dumps(message).encode("utf-8"))

```

Y enviamos algunos mensajes que en nuetro punto de vista podemos leerlo y podemos entenderlo desde el lado del cliente.

![image](https://hackmd.io/_uploads/SyRvR5X1Ml.png)

#### b) Verificar que la carga útil llega cifrada al servidor.

Podemos entonces observar que desde el lado del server se logro recibir el mensaje con payload encriptado segun el formao sleccionado.

![WhatsApp Image 2026-05-14 at 4.10.49 PM](https://hackmd.io/_uploads/r1rlzyI1fl.jpg)


#### c) Documentar las principales características de la técnica de cifrado que utilizaste.

AQUI DESCRIBE EL CONCEPTO DE AES Y SUS PRINCIPALES CARACTERISTICAS. + ENTENDIENDO LO QUE ES CIFRADO SIMETRICO.


### 5) OPCIONAL: Modifica el servidor para que sea capaz de descifrar tu carga útil. Desplega servidor y cliente en tu local, captura paquetes mostrando que los mismos están cifrados mientras viajan pero el servidor es capaz de decodificar la carga útil.

Para poder realizar esto primero en un cifrado simetrcio tanto cliente como servidor deben saber la clave osea la clave que tiene el cliente la tiene el servidor y con eso puede decifrar el contenido del payload. Modificamos el servidor para que se aconfigurado localmente desde una de las computadores de uno de los miembros del grupo. Utilizando ademas un celular como router o como acces point las dos computadoras tanto la del cliente como la del servidor estaran conectadas a ese acces opoitn por ende se les asiganara una IP que sera usado como para lograr la conexion:

Desde el lado del cliente usamos la IP de mquien sera mi server:
![image](https://hackmd.io/_uploads/rJwGbomJfx.png)

Asi tenemos que ver el coo llega el mesnaje a el seridor ya cifrado
![image](https://hackmd.io/_uploads/BJhHZi7Jzl.png)


 
 
 
no una clave aleatoria sino una fija la cueal la sabra el cliente y el servidor Como ya comprobamos que podemos realizar una conexion entre Cliente y servidor dentro de nuestra misma red, modificamos un poco nuestro codigo para agregar una clave fija que ser aocnocida por ambaas partes.
 
 COdigo del lado del server:
 ![image](https://hackmd.io/_uploads/B11L7iQkGe.png)
 
 con la ayuda del msiam librearia podemos desncriptar el mensaje enviado:
```
 # Desencriptamos el payload que envió el cliente
                    try:
                        # Convertimos el string nuevamente a bytes, desencriptamos y luego lo pasamos a string
                        payload_encriptado = message["payload"].encode("utf-8")
                        payload_desencriptado = cipher.decrypt(payload_encriptado).decode("utf-8")
                        
                        print(f"{message['group']}: {payload_desencriptado}")
                    except Exception as e:
                        print(f"Error al desencriptar el mensaje de {ip_address}: {e}")
                        
```

Codigo del lado del cliente:

![image](https://hackmd.io/_uploads/ByrdQsXyMl.png)


Como se observo en las terminales de ambos lados el mensaje fue legible pero encriptado osea que nadie por fuera del del lciente o el servidor uede descifrar el mensaje.
