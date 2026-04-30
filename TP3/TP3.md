# TP2: Introducción a infraestructura de servicios web con perspectiva de redes

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


### 1) Investigación conceptual (respuestas breves). Responder en forma concisa.

#### a) ¿Qué es SSH y qué problema resuelve?

SSH (Secure Shell) es un protocolo de red que permite conectarse a otra computadora de forma remota y segura. Resuelve el problema de que antes (ej: Telnet) los datos viajaban sin protección, mientras que SSH cifra la comunicación y evita que la intercepten.

#### b) Diferencia entre autenticación y cifrado

Autenticación: verifica quién sos (tu identidad).
Cifrado: protege la información para que nadie la pueda leer mientras viaja.

#### c) ¿Qué es una clave pública y una clave privada?

Son dos claves que funcionan juntas:

Clave pública: se puede compartir con cualquiera.
Clave privada: es secreta y solo la tiene el dueño.
Se usan para autenticar y cifrar datos en sistemas como SSH.

#### d) ¿Por qué la clave privada no debe compartirse?

Porque es la que demuestra tu identidad. Si alguien la obtiene, puede hacerse pasar por vos y acceder a sistemas como si fuera el dueño.

#### e) ¿Qué ventajas tienen las claves SSH frente a contraseñas?

Son más seguras (no se envían por la red). Difíciles de adivinar o romper. Permiten automatizar conexiones sin escribir contraseña.
Reducen riesgos como phishing o robo de credenciales



### 2) Verificar conexión SSH con alguna de las VMs que reservaron. Documentar su paso por la VM creando una carpeta con el nombre de su grupo.
Primero se descargaron las claves proporcionadas por el docente, y haciendo un cambio de permisos en una de las claves a utilizar dandole permisos minimos para la lectura de la clave. y ademas: utilizando el siguiente comando para ingresar a la VM: 
```bash
ssh -i <path/a/la/clave>pc2_key.pem pc-alumnos-2@4.206.217.29
```
![2_CreacionDirGrupo&Index.html](https://hackmd.io/_uploads/ByOY4_e0Zx.png)
i
instalacion de netcat de manera loca
![4_Instalacion_ncat_local](https://hackmd.io/_uploads/rymUwdeRWl.png)

instalacion de netcar de manera remota
![4_instalacion_ncat_remoto](https://hackmd.io/_uploads/BywoDOlRbl.png)



#### a) Montar un servidor TCP en alguno de los puertos habilitados en la VM:

Tenemos puertos disponibles a utilizar en este laboratorio desde 5000 hasta 6000:

```bash
ncat -l <puerto>
```
Desde la terminal de la VM ejecutamos el comando mencionado y seleccionamos el puerto siendo asi este nuestro servidor


Luego configuramos nuestro wireshark desde el cliente para escuchar conexiones TCP no SSH hacia la VM con el filtro **ip.dst == 4.206.217.29 and !ssh** 

Ahora configuramos el cliente para poder enviar mensajes con el comando: 

```bash
ncat <VM_IP> <PUERTO>
```

![4_tcp_server_config_port](https://hackmd.io/_uploads/HyAFK_x0be.png)

Como podemos observar en la anterior imagen aqui podemos mirar el como en distintos puertos logramos la comunicacion permitiendo enviar mensajes TCP desde el cliente al servidor y tambien se puede hacer viceversa..

Ahora se quiere analizar unos de los paquete TCP mas el handshake que se crea entre los lados. Aqui podemos visualizar el mensaje "Hola :P" en el puerto 5050:

![Mensaje_TCP](https://hackmd.io/_uploads/H1C6ndlRbg.png)

Tambien analizando el mismo paquete podemos intuir que dentro del grupo de mensajes el primer mensaje del grupo de mensajes tcp es el handshake:

![handshakeSYN](https://hackmd.io/_uploads/SJiUT_lCZx.png)

y tambien ack: 
![handshakeACK](https://hackmd.io/_uploads/ByudT_gAbe.png)


#### b) Repetir el punto anterior pero utilizando protocolo UDP (investigar cómo enviar tráfico UDP con netcat).

Ahora repetiremos los mismos pasos anteirores en la conexion TCP , pero sin documentar el hankdshake debido a que no existe handshake en UDP. Ademas el comando para establecer el servidor en la VM sera el siguiente:

```bash
ncat -l -u <puerto>
```

De la misma forma que en el punto anterior nos establecemos la conexion del cliente mediante el mismo comando usando la Ip y el numero de puerto.

Ahora analizando mediante el wireshark podemos filtrar el paquete ya no por TCP sino por UDP, como se puede visualizar en la siguiente imagen:

![Mensaje-UDP](https://hackmd.io/_uploads/BkKpJYgAbe.png)


#### c) Conectarse a otra VM (mantener dos sesiones en dos terminales distintas) y establecer conexión con netcat entre ellas. Documentar un ida y vuelta de frases al estilo chat entre las instancias.
--

### 5) Navegar a la carpeta de su grupo (la que crearon en el ítem 2). Crear un archivo index.html dentro con un mensaje dentro al estilo “Hola Mundo”. Pero sean más creativos... Luego, desplieguen un servidor HTTP:

Como mencionamos anteriormente creamos un archivo index.html en la carpeta de la VM con el nombre de nuestro grupo ahora, y editando mediante el editor "nano" el index.html podemos armar una minipagina y desplegarla mediante el sigiuente comando y los puertos entre 5000-6000 por ejemplos:

```bash
python3 -m http.server <puerto>
```

Como se observa en la imagen:

![5_3_despliegue_ok_port_5003](https://hackmd.io/_uploads/HJHzWYlCWg.png)


ahora desde otra pc o inclusive un con el celuar podremos visualizar la pagina desplegada colocando en nuestro navegador:

```bash
http://4.206.217.29:5001
```


![5_4_get_http_port_5003](https://hackmd.io/_uploads/r1JTZYlCbg.jpg)

Ademas tambien podemos operar de la misma forma que operamos antes osea podemos capturar filtrar y capturar el paquete HTTP desde el lado del cliente, el resultado es el siguiente:


![CapturaWiresharkHTTP](https://hackmd.io/_uploads/BkFHXFe0be.png)

![PaqueteHTTP](https://hackmd.io/_uploads/SynUQYeA-e.png)
a


Podemos observar que al ser protocolo HTTP y no HTTPS podemos descifrar el contenido del mensaje mediante el wireshark; ademas si podemos intervenirlo


### 6) Ver el siguiente video de Veritasium en YouTube: **https://www.youtube.com/watch?v=PPJ6NJkmDAo**

#### a) Relacionar el problema que aborda el video con los TPs 1), 2) y 3). ¿Qué cosas que hemos aprendido se aplican directamente al problema demostrado?

Al igual que en el TP1, donde los routers desencapsulan la trama Ethernet, examinan el paquete IP y lo reencapsulan para el siguiente salto, en este ataque se observa un comportamiento análogo de intermediario (Man-in-the-Middle). Los atacantes utilizan un dispositivo para interceptar la señal NFC del celular, procesan los datos en una laptop y finalmente retransmiten la información al posnet real a través de un celular secundario. En la parte dos del TP1, donde simulamos el envío de paquetes y estos podían sufrir modificaciones en el payload al ser interceptados, tenemos una analogía directa de lo que muestran en el video: cómo al interceptar el NFC modificaron los bits a su beneficio y luego lo retransmitieron. Esto refuerza la necesidad de diseñar sistemas más robustos ante modificaciones de bits.
En el TP2 adquirimos práctica con la Capa Física (Capa 1) al armar y verificar cables UTP. En el video, se observa cómo la intercepción de la señal NFC se realiza explotando directamente el medio físico inalámbrico. Esto demuestra que la simple proximidad o la conexión física no garantizan la confidencialidad de los datos, dejándonos como lección que no debemos fiarnos únicamente de la seguridad inherente a la capa física.
En este TP3 comprobamos que protocolos como SSH utilizan un par de claves (pública y privada) para autenticar la conexión de forma segura mediante criptografía asimétrica. De manera análoga, las tarjetas de crédito emplean este mismo concepto matemático para crear firmas digitales que el lector debe verificar. El hackeo demostrado funciona porque Visa decide omitir esta validación asimétrica cuando el lector de tarjetas está conectado a internet, lo que rompe la seguridad del sistema.

#### b) ¿Qué cosas deberíamos tener en cuenta dado el principio de confidencialidad en las redes de computadoras y los resultados obtenidos en este laboratorio?

En el laboratorio se comprobo que al capturar tráfico HTTP con Wireshark, la información viaja en texto plano y puede ser leída fácilmente. El video demuestra lo mismo para las señales inalámbricas NFC. De esto aprendemos que la confidencialidad no depende del medio físico, sino del cifrado lógico. Tambien que si los datos no están cifrados, un atacante Man-in-the-Middle no solo puede espiar, sino también intervenir el contenido y modificar los bits del payload. En el fraude del video, los atacantes logran alterar banderas (flags) críticas del payload, en el video se muestra especificamente que lo hacen con el tipo de trasaccion (engañando al celular para que crea que es un lector de transporte offline) y la de categoria de seguridad (etiquetándola como low value), esto es justamente por que esta informacion no esta encriptada, en caso de estarlo esto no se podria hacer.
En el TP tambien vimos con SSH utiliza claves publicas y privadas para mantener la confidencialidad, en el video pudimos ver como el hackeo es posible devido a que VISA saltarse una validación criptográfica similar cuando asume que el posnet está online. Esto nos deja con la conclución de que el cifrado debe realizarce de extremo a extremo, para mantener la comunicación segura.