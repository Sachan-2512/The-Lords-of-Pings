# TP3: Introducción a infraestructura de servicios web con perspectiva de redes

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
SSH (*Secure Shell*) es un protocolo de red que permite conectarse a otra computadora de forma remota y segura. Resuelve el problema de la exposición de datos en texto plano que presentaban protocolos anteriores (como Telnet), ya que SSH cifra la comunicación y evita que la información sea interceptada o leída por terceros.

#### b) Diferencia entre autenticación y cifrado
* **Autenticación:** Es el proceso que verifica la identidad del usuario (quién sos).
* **Cifrado:** Es el mecanismo que protege la información alterando su formato para que nadie pueda leerla mientras viaja por la red.

#### c) ¿Qué es una clave pública y una clave privada?
Son un par de claves utilizadas en criptografía asimétrica que funcionan en conjunto para autenticar y cifrar datos en sistemas como SSH:
* **Clave pública:** Puede compartirse libremente con cualquier sistema o usuario.
* **Clave privada:** Es secreta y debe permanecer únicamente bajo el control de su dueño.

#### d) ¿Por qué la clave privada no debe compartirse?
Porque es el elemento criptográfico que demuestra y garantiza tu identidad. Si un tercero obtiene acceso a tu clave privada, puede suplantar tu identidad y acceder a los sistemas con tus mismos privilegios.

#### e) ¿Qué ventajas tienen las claves SSH frente a contraseñas?
Son considerablemente más seguras porque no se transmiten a través de la red, lo que las hace resistentes a ataques de fuerza bruta, suplantación (*phishing*) o robo de credenciales. Además, permiten automatizar conexiones seguras sin necesidad de ingresar una contraseña manualmente en cada inicio de sesión.

---
#### 2) Verificar conexión SSH con alguna de las VMs que reservaron. Documentar su paso por la VM creando una carpeta con el nombre de su grupo.

Primero, se descargaron las claves proporcionadas por la cátedra. Luego, se ajustaron los permisos de la clave localmente para restringir su lectura, una medida de seguridad requerida para su uso. Finalmente, ingresamos a la Máquina Virtual (VM) ejecutando el siguiente comando:

```bash
ssh -i <path/a/la/clave>pc2_key.pem pc-alumnos-2@4.206.217.29
```

![2_CreacionDirGrupo&Index.html](https://hackmd.io/_uploads/ByOY4_e0Zx.png)

Se comprobó el acceso exitoso a la VM al observar el cambio de usuario en el prompt de la terminal. Posteriormente, se creó un directorio en el home de la VM con el nombre del grupo y, dentro de este, un archivo index.html que será utilizado en el punto 5.

### 3) Usando Wireshark, capturar tráfico SSH y analizar alguno de los paquetes. ¿Podés descifrar el contenido?

Utilizando Wireshark, se aplicó un filtro utilizando la IP de destino correspondiente a la VM para aislar y analizar los paquetes de red pertinentes.

![3_CapturaSSH_Wireshark1](https://hackmd.io/_uploads/HJTbIdgR-l.png)

Al inspeccionar un paquete SSH específico, se constató que no es posible descifrar su contenido en texto plano. Esto evidencia el funcionamiento del protocolo SSH, el cual cifra el payload del mensaje garantizando la confidencialidad de la comunicación.

![3_CapturaSSH_Wireshark2](https://hackmd.io/_uploads/BJBfIdeR-l.png)


### 4) Nuestras VMs (virtual machines) están corriendo un SO Debian en una arquitectura x64. Vamos a utilizar netcat para desplegar servidores simples y capturar tráfico. Instalar netcat en la VM si no está instalado (sudo apt install ncat) y en sus computadoras locales. 

En primer lugar, se procedió a instalar netcat tanto en los dispositivos locales como en el entorno remoto mediante el siguiente comando:

```bash
sudo apt install ncat
```
Instalación de netcat de manera local:
![4_Instalacion_ncat_local](https://hackmd.io/_uploads/rymUwdeRWl.png)

Instalación de netcat de manera remota:
![4_instalacion_ncat_remoto](https://hackmd.io/_uploads/BywoDOlRbl.png)



#### a) Montar un servidor TCP en alguno de los puertos habilitados en la VM:

Utilizando los puertos disponibles para este laboratorio (rango 5000 a 6000), se ejecutó el siguiente comando en la terminal de la VM para establecerla como servidor:

```bash
ncat -l <puerto>
```
A continuación, configuramos Wireshark en la máquina cliente para escuchar las conexiones TCP (excluyendo SSH) dirigidas hacia la VM, utilizando el filtro: ip.dst == 4.206.217.29 and !ssh.

Para iniciar la comunicación desde el cliente hacia el servidor, se utilizó:

```bash
ncat <VM_IP> <PUERTO>
```

![4_tcp_server_config_port](https://hackmd.io/_uploads/HyAFK_x0be.png)

Como se observa en la imagen anterior, se logró establecer la comunicación en distintos puertos, permitiendo el envío de mensajes TCP bidireccionales entre el cliente y el servidor.

Al analizar la captura de los paquetes TCP, identificamos específicamente el envío del mensaje "Hola :P" a través del puerto 5050:


![Mensaje_TCP](https://hackmd.io/_uploads/H1C6ndlRbg.png)

Dentro de esta secuencia de paquetes, se puede visualizar claramente el proceso de establecimiento de conexión inicial (Three-way Handshake):

Paquete SYN:
![handshakeSYN](https://hackmd.io/_uploads/SJiUT_lCZx.png)

Paquete ACK:
![handshakeACK](https://hackmd.io/_uploads/ByudT_gAbe.png)


#### b) Repetir el punto anterior pero utilizando protocolo UDP (investigar cómo enviar tráfico UDP con netcat).

Se repitieron los pasos anteriores orientando la conexión al protocolo UDP. En este caso, no se documenta un handshake dado que UDP es un protocolo no orientado a la conexión. El comando utilizado para levantar el servidor UDP en la VM fue:

```bash
ncat -l -u <puerto>
```

La conexión desde el cliente se estableció de forma análoga al punto anterior. Analizando el tráfico con Wireshark y aplicando un filtro para UDP, logramos visualizar los paquetes de la siguiente manera: 

![Mensaje-UDP](https://hackmd.io/_uploads/BkKpJYgAbe.png)

#### c)​ Conectarse a otra VM (mantener dos sesiones en dos terminales distintas) y establecer conexión con netcat entre ellas. Documentar un ida y vuelta de frases al estilo chat entre las instancias.

Para esta actividad se utilizó la VM correspondiente a PC-4 como nodo central de la comunicación, configurada como broker mediante `ncat`. A partir de allí, se conectaron las VMs de PC-3, PC-2 y PC-1 al mismo servicio, lo que permitió establecer una conversación tipo chat entre las distintas instancias. De este modo, se verificó que los mensajes enviados desde cada máquina fueran reenviados a las demás participantes, reproduciendo un intercambio de mensajes entre varias instancias a través de una conexión TCP establecida con `ncat`.

![Conexion-VMs](https://hackmd.io/_uploads/rJ-LaG-RWl.png)

### 5) Navegar a la carpeta de su grupo (la que crearon en el ítem 2). Crear un archivo index.html dentro con un mensaje dentro al estilo “Hola Mundo”. Pero sean más creativos... Luego, desplieguen un servidor HTTP:

Utilizando el editor de texto nano, se modificó el archivo index.html creado en el ítem 2 para estructurar una página web sencilla. Luego, se desplegó un servidor HTTP básico escuchando en el rango de puertos habilitados (ej. 5001/5003) con el siguiente comando:

```bash
python3 -m http.server <puerto>
```

Como se observa en la imagen:

![5_3_despliegue_ok_port_5003](https://hackmd.io/_uploads/HJHzWYlCWg.png)


Despliegue del servidor:

Una vez iniciado, logramos visualizar la página web accediendo desde un navegador (incluso desde un dispositivo móvil) mediante la dirección:

```bash
http://4.206.217.29:5003
```


![5_4_get_http_port_5003](https://hackmd.io/_uploads/r1JTZYlCbg.jpg)

Al igual que en los pasos anteriores, se capturó el tráfico generado durante esta petición desde el lado del cliente:


![CapturaWiresharkHTTP](https://hackmd.io/_uploads/BkFHXFe0be.png)

![PaqueteHTTP](https://hackmd.io/_uploads/SynUQYeA-e.png)

Conclusión: Se comprobó que, al utilizar el protocolo HTTP en lugar de HTTPS, la información viaja sin cifrar. Con herramientas como Wireshark, es posible descifrar el contenido del mensaje en texto plano, lo que implica que el tráfico también es susceptible de ser intervenido o modificado.

### Pasaje de archivo HTML entre VMs y captura en Wireshark

Para demostrar la viabilidad de enviar archivos sin cifrar mediante TCP y su posterior análisis, se procedió a transferir el archivo `index.html` desde PC-2 hacia PC-4. Dado que el tráfico entre ambas VMs ocurre internamente en la nube del proveedor (Google y Azure) y no pasa por nuestra máquina local, la captura de red se realizó directamente en la VM receptora (PC-4) utilizando `tcpdump`.

El procedimiento consistió en los siguientes comandos:
1. En **PC-4** se inició la captura de tráfico en el puerto 5003: `sudo tcpdump -i any -w ~/TheLordsOfPings/captura.pcap tcp port 5003`
2. En otra terminal de **PC-4**, se dejó a `ncat` escuchando y redirigiendo la salida al archivo destino: `ncat -l 5003 > ~/TheLordsOfPings/index.html`
3. En **PC-2**, se leyó el archivo local y se envió a través de la red hacia PC-4: `cat ~/TheLordsOfPings/index.html | ncat 34.130.32.165 5003`
4. Finalmente, desde la **máquina local** se descargó el archivo resultante mediante `scp` para su análisis visual: `scp -i [ruta_clave] pc-alumnos-4@34.130.32.165:~/TheLordsOfPings/captura.pcap ./capture.pcap`

![Terminales de Transferencia y Captura](https://hackmd.io/_uploads/S1wXiVW0-l.png)

Al abrir el archivo `capture.pcap` localmente con Wireshark y aplicar el filtro `tcp.port == 5003`, observamos el establecimiento de la conexión TCP (Handshake) seguido del envío de los datos. 

Un aspecto técnico interensante que destacamos en el análisis es la **segmentación de TCP**. Dado que el peso del archivo `index.html` (alrededor de 3.2K) superaba el tamaño máximo de segmento permitido para un solo paquete en la red, TCP dividió el código fuente del documento en dos paquetes distintos para su transmisión:

1. **Primer paquete de datos (Punto de captura 4):** Contiene los primeros 2816 bytes de payload. En su formato de texto plano inspeccionado, se puede visualizar claramente el inicio de la estructura del documento con la etiqueta `<!DOCTYPE html>`.
![Wireshark Captura Parte 1](https://hackmd.io/_uploads/ByYri4WAZg.png)

2. **Segundo paquete de datos (Punto de captura 5):** Transporta los 436 bytes restantes del archivo, en donde logramos confirmar el fin del envío al observarse el cierre de las etiquetas `</footer></body></html>`.
![Wireshark Captura Parte 2](https://hackmd.io/_uploads/SJFVi4ZA-g.png)

Esto nos reafirma que, al transmitir datos en texto plano mediante HTTP o herramientas como Netcat, cualquier intruso con acceso a la red puede interceptar y reconstruir la comunicación en su totalidad. Además, al visualizar la fragmentación de los datos en distintos paquetes (segmentación TCP), se evidencia cómo la Capa de Transporte fragmenta la información subyacentemente, resaltando la necesidad de aplicar cifrado (como HTTPS o SSH) para garantizar la confidencialidad de la información compartida, incluso cuando los datos se envíen fragmentados.

### 6) Ver el siguiente video de Veritasium en YouTube: **https://www.youtube.com/watch?v=PPJ6NJkmDAo**

#### a) Relacionar el problema que aborda el video con los TPs 1), 2) y 3). ¿Qué cosas que hemos aprendido se aplican directamente al problema demostrado?

Al igual que en el TP1, donde los routers desencapsulan la trama Ethernet, examinan el paquete IP y lo reencapsulan para el siguiente salto, en este ataque se observa un comportamiento análogo de intermediario (Man-in-the-Middle). Los atacantes utilizan un dispositivo para interceptar la señal NFC del celular, procesan los datos en una laptop y, finalmente, retransmiten la información al posnet real a través de un celular secundario. En la parte dos del TP1 (donde simulamos el envío de paquetes que podían sufrir modificaciones en el payload al ser interceptados) tenemos una analogía directa de lo que muestran en el video: al interceptar el NFC, modificaron los bits a su beneficio y luego los retransmitieron. Esto refuerza la necesidad de diseñar protocolos más robustos ante alteraciones.

En el TP2 adquirimos práctica con la Capa Física (Capa 1) al armar y verificar cables UTP. En el video, se observa cómo la intercepción de la señal se realiza explotando directamente el medio físico inalámbrico. Esto demuestra que la simple proximidad física no garantiza la confidencialidad de los datos, dejándonos como lección que no debemos fiarnos únicamente de la seguridad inherente al medio físico.

En este TP3 comprobamos que protocolos como SSH utilizan un par de claves (pública y privada) para autenticar la conexión de forma segura mediante criptografía asimétrica. De manera análoga, las tarjetas de crédito emplean este mismo concepto matemático para crear firmas digitales que el posnet debe verificar. El fraude demostrado funciona porque la red de validación decide omitir esta validación asimétrica cuando asume que el lector de tarjetas está conectado a internet, lo que rompe la seguridad lógica del sistema.

#### b) ¿Qué cosas deberíamos tener en cuenta dado el principio de confidencialidad en las redes de computadoras y los resultados obtenidos en este laboratorio?

En el laboratorio se comprobó que, al capturar tráfico HTTP o usar Netcat con Wireshark, la información viaja en texto plano y puede ser leída con facilidad. El video demuestra un principio similar para las señales inalámbricas NFC: de esto aprendemos que la confidencialidad no depende del medio físico, sino del cifrado lógico.

Si los datos no están cifrados adecuadamente, un atacante posicionado como Man-in-the-Middle no solo puede espiar, sino también intervenir el contenido y modificar los bits del payload. En el fraude expuesto en el video, los atacantes logran alterar banderas (flags) críticas de la transacción, engañando al celular para que asuma que está ante un lector de transporte offline y categorizando la operación como "de bajo valor". Esto es factible precisamente porque estas variables de la transacción no están protegidas criptográficamente; en caso de estarlo, el posnet rechazaría la modificación.

Adicionalmente, en este TP vimos cómo SSH utiliza claves criptográficas para mantener la confidencialidad e integridad. En el video observamos que el hackeo es exitoso debido a que la red se salta una validación criptográfica indispensable. Esto nos deja como conclusión final que el cifrado y la autenticación rigurosa deben realizarse obligatoriamente de extremo a extremo para mantener una comunicación verdaderamente segura y confidencial.