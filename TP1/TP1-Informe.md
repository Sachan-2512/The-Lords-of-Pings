# TP1: Simulación de envío de paquetes, ARP y ruteo entre redes

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
| **Nicolas Melia** | _nicolas.melia@mi.unc.edu.ar_ |
| **Saqib D. Mohammad Cabrejos** | _saqib.mohammad@mi.unc.edu.ar_ |


### 1) Identificación de dispositivos y armado de la topología.

En esta primera etapa, establecimos la base operativa de la simulación. El aula se transformó en una red heterogénea compuesta por múltiples LANs interconectadas a través de una WAN.

La topología general consistió en varios grupos actuando como redes de área local (LAN). Cada grupo contaba con tres dispositivos finales (Hosts) y un Router que actuaba como Gateway por defecto. A su vez, existieron grupos de routers intermedios que conformaron la infraestructura WAN, permitiendo el ruteo de paquetes entre redes distantes

### Identificación de Dispositivos del Grupo

De acuerdo a la consigna del Trabajo Práctico, cada integrante del grupo asumió una identidad de red única para conformar la topología de la LAN.

| Rol | Dirección IP | Dirección MAC | Máscara de Subred | Gateway por Defecto |
| :--- | :--- | :--- | :--- | :--- |
| Host 1 | 10.5.0.101 | AD:95:21 | 255.255.0.0 | 10.5.0.1 |
| Host 2 | 10.5.0.102 | AD:44:11 | 255.255.0.0| 10.5.0.1 |
| Host 3 | 10.5.0.103 | AA:39:26 | 255.255.0.0 | 10.5.0.1 |
| Router / GW | 10.5.0.1 | AC:44:52 | 255.255.0.0 | N/A |

### 2) Armado de topologia.

Una vez establecidas las identidades de red, procedimos al armado físico de la topología en el aula, conectando las LANs a través de los routers centrales para conformar la WAN. Antes de iniciar el envío de mensajes, realizamos una simulación de rutina ARP para que cada dispositivo construyera su mapa de direcciones lógicas (IP) versus direcciones físicas (MAC).

### Proceso de Descubrimiento ARP.

Cada router y host descubrió a sus vecinos directos mediante el protocolo ARP. En esta etapa, el router de nuestro grupo identificó a los tres hosts y al router central al que estaba conectado.

### Tabla ARP de nuestro Router (Default Gateway).
Esta tabla representa el mapa de direcciones IP vs. direcciones físicas (MAC) que el router del grupo construyó durante la fase de descubrimiento para poder entregar los frames a sus vecinos directos.

| Dirección IP | Dirección MAC | Interfaz | Dispositivo / Rol |
| :--- | :--- | :--- | :--- |
| 10.5.0.101 | 	AD:95:21 | LAN | Host 1 (Local) |
| 10.5.0.102 | AD:44:11 | LAN | Host 2 (Local) |
| 10.5.0.103 | AA:39:26 | LAN | Host 3 (Local) |
| 10.10.0.1 | AC:45:70 | WAN | Router Central  |

### 3) Conformación de paquetes
En esta fase, cada Host recibió un Payload en formato hexadecimal y dos destinos posibles. Nuestra tarea fue realizar la encapsulación siguiendo el modelo de capas, transformando los datos en un Frame Ethernet que contenía un Paquete IP.

A continuación, se detallan los frames Ethernet y paquetes IP construidos por cada integrante del grupo. Se destaca que, aunque los destinos finales son distintos, todos los frames apuntan físicamente al Default Gateway para iniciar el ruteo.

#### Host 1

* **MAC DESTINO**: AC:44:52
* **MAC ORIGEN**: AD:95:21
* **IP ORIGEN**: 10.5.0.101
* **IP DESTINO**: 10.5.0.105
* **TTL**: 6
* **PAYLOAD**: 0000 1011 1110 1101
* **CRC**:

#### Host 2

* **MAC DESTINO**: AC:44:52
* **MAC ORIGEN**: AD:44:11
* **IP ORIGEN**: 10.5.0.102
* **IP DESTINO**: 10.7.0.105
* **TTL**: 6
* **PAYLOAD**: 0011 1100 0010 1111
* **CRC**:

#### Host 3

* **MAC DESTINO**: AC:44:52
* **MAC ORIGEN**: AA:39:26
* **IP ORIGEN**: 10.5.0.103
* **IP DESTINO**: 10.9.0.101
* **TTL**: 6
* **PAYLOAD**: 1110 1101 1011 0010
* **CRC**:

### 4) Simular las transmisiones y recepciones
Una vez conformados los paquetes, procedimos a la simulación del tráfico en el aula. En esta etapa, el rol de los routers fue crítico, ya que debieron realizar el proceso de desencapsulación y re-encapsulación en cada salto.

### Proceso de Ruteo Hop-by-Hop

Durante la actividad, observamos el siguiente flujo para los paquetes que salieron de nuestra LAN (10.5.0.0):

1. Envío del Host al Default Gateway: Cada host de nuestro grupo entregó su tarjeta (frame) al compañero que representaba al default gateway. El frame tenía la MAC destino del default gateway, pero la IP destino de un host remoto.

2. Procesamiento en el Router (DG): El default gateway recibió el frame y verificó que la MAC coincidía con la suya.

    * Desencapsuló el frame para leer el paquete IP.

    * Decremento de TTL: El router restó 1 al valor del TTL (pasando de 6 a 5).

    * Consultó su tabla de ruteo y determinó cuales paquetes debían ir hacia el Router Central y cuales a host dentro de la LAN.

    * Re-encapsulación: Construyó un nuevo frame Ethernet con su propia MAC como origen y la MAC del Router Central como destino, manteniendo intacto el paquete IP original.

 3. Tránsito en la WAN: El paquete atravesó los routers centrales, repitiendo el proceso de decremento de TTL y cambio de direcciones MAC en cada enlace.

 4. Recepción Final: El host destino recibió el frame, verificó su MAC e IP, y finalmente leyó el Payload en binario.

## Resultado de recepción

### Recepcion exitosa
El Host identificado con la IP 10.5.0.103 recibió correctamente un paquete proveniente de una red externa.

El Default Gateway de nuestra red recibió el frame desde el Router Central, verificó en su Tabla ARP  que la IP 10.5.0.103 pertenecía a su LAN y encapsuló el paquete en un frame final con la MAC destino del Host .103.

| HOST RECEPTOR | IP ORIGEN | IP DESTINO | TTL FINAL| ESTADO |
|:---|:---|:---|:---|:---|
|H3|10.12.0.101|10.5.0.103| 3 | Entregado|

### Paquete Devuelto (Destination Unreachable)

El paquete enviado por nuestro Host 2 no pudo llegar a su destino final.

Al no encontrar una ruta válida o no obtener respuesta ARP en la red de destino, el router encargado de ese segmento descartó el paquete e informó la imposibilidad de entrega (simulando el retorno del paquete al emisor).

| HOST RECEPTOR | IP ORIGEN | IP DESTINO | TTL FINAL| ESTADO |
|:---|:---|:---|:---|:---|
|H2|10.5.0.102|10.7.0.105| 4 | Fallido|

### 5) Reflexiones y documentación

#### a) Durante el laboratorio, la dirección IP destino del paquete se mantuvo constante mientras que la dirección MAC destino cambió en cada salto. ¿Por qué ocurre esto y qué nos dice sobre la diferencia entre direccionamiento lógico (IP) y direccionamiento físico (MAC)?

Esto ocurre porque la IP identifica el destino final de manera global a través de diferentes redes (capa 3), mientras que la MAC solo tiene validez dentro de un mismo segmento físico o enlace local (capa 2).
* IP: Es la dirección "lógica" que permite el ruteo de extremo a extremo.
* MAC: Es la dirección "física" necesaria para que dos dispositivos conectados al mismo medio (como el Host y su Gateway) puedan hablarse.

#### b) Cuando un host quiere enviar un paquete a un dispositivo en otra red, no intenta descubrir directamente la MAC del host destino, sino la del default gateway. ¿Por qué se utiliza este mecanismo y qué problema resolvería el gateway que el host no puede resolver por sí solo?

Cuando un host quiere enviar un paquete fuera de su red local, no intenta descubrir la MAC del destino final porque el protocolo ARP solo funciona por difusión (broadcast) dentro de su propia subred.

El host utiliza el Gateway porque este actúa como el nodo que sabe cómo alcanzar redes externas que el host desconoce.

El problema que resuelve es el aislamiento, sin el gateway, el host solo podría comunicarse con dispositivos que tengan su mismo prefijo de red (en nuestro caso, 10.5).

#### c) Cada router toma decisiones basándose únicamente en su tabla de ruteo local y no en el camino completo hacia el destino. ¿Qué ventajas tiene este modelo de ruteo hop-by-hop para redes grandes como Internet?

Este modelo permite que los routers tomen decisiones basadas únicamente en su tabla local, sin conocer el camino completo. Esto permite:

* Escalabilidad: Ningún router necesita conocer la topología de todo Internet, solo necesita saber a quién entregarle el paquete para que esté "un paso más cerca" del destino.
* Robustez: Si un enlace cae, los routers pueden actualizar sus tablas locales y desviar el tráfico por otra ruta sin afectar al emisor original.

#### d) En el laboratorio observamos que los routers desencapsulan y vuelven a encapsular el paquete en cada enlace. ¿Por qué es necesario reconstruir el frame Ethernet en cada salto y qué ocurriría si los routers intentaran reenviar exactamente el mismo frame?

Es necesario reconstruir el frame en cada salto porque las direcciones MAC de origen y destino deben actualizarse para reflejar los dos nodos que están comunicándose en ese enlace específico.

Si un router intentara reenviar el frame original sin cambios, el siguiente salto lo descartaría porque la MAC destino seguiría siendo la del primer nodo y no la suya propia.

#### e) El campo TTL se decrementa en cada router. ¿Qué problema de la red previene este mecanismo y qué podría suceder si el TTL no existiera?

El TTL se decrementa en cada router para evitar que los paquetes circulen infinitamente en la red en caso de que existan bucles o errores en las tablas de ruteo.

Si el TTL llegara a cero, el router descarta el paquete.

Sin este mecanismo, un paquete "perdido" (como el de nuestro Host 2) podría saturar los enlaces de la red al dar vueltas por siempre.

---

### Parte 2 Inyeccion y Deteccion de errores

#### 1. Discutiremos en clases acerca de EDAC y los lineamientos precisos del laboratorio. El ejercicio es simple:

#### a. Routers no default gateway (sin LAN debajo): al momento de re-empaquetar los paquetes, modificar (o no) en uno o más bits la payload. Documentar de manera secreta qué paquetes fueron modificados y que paquetes no (registrar payload + destino). Reenviar el paquete.

De acuerdo a la consigna, los routers intermedios debían reempaquetar los paquetes y modificar (o no) en uno o más bits el payload, documentando de manera secreta estos cambios antes de reenviarlos.

En este punto del trabajo practico, este rol de inyección de errores fue asumido por el profesor. Él se encargó de interceptar los mensajes enviados, cambiar un bit (modificando así el valor hexadecimal original) de manera secreta, y enviarlo a otro grupo para que este, mediante el EDAC, determinara si el mensaje era correcto o incorrecto.


#### b. Hosts / End devices: al enviar paquetes aplicar técnicas de EDAC. Al recibir paquetes, determinar si fueron o no modificados. Justificar.

Como dispositivos finales (Hosts), aplicamos técnicas de detección de errores tanto al enviar como al recibir paquetes para determinar si fueron modificados. Durante esta practica, utilizamos dos métodos distintos: XOR (simulando CRC) para el envío y Paridad Par para la recepción.

#### a. Generación de mensaje original y transmision:

Para enviar nuestro mensaje, generamos un EDAC aplicando una operación lógica XOR secuencial sobre los bloques de nuestro payload. El procedimiento consistió en pasar el payload hexadecimal a binario y realizar la operación XOR entre cada bloque de 4 bits unos con otros hasta obtener el resultado final.

| Parámetro | Valor |
| :--- | :--- |
| **Nombre de mi Grupo** | The lords of Pings |
| **IP origen (nuestra IP)** | 10.5.0.1 |
| **Payload original a enviar** | `9C25` |
| **Payload convertido a binario** | `1001 1100 0010 0101` |
| **Cálculo del EDAC (XOR)** | `1001` XOR `1100` = `0101`<br>`0101` XOR `0010` = `0111`<br>`0111` XOR `0101` = `0010` |
| **EDAC final enviado** | `0010` |

#### b. Recepción y Comprobación (Reporte de Rx):

Posteriormente, recibimos un mensaje modificado por el profesor (el cual podía estar adulterado o no). Para esta etapa de recepción, se nos indicó que el EDAC adjunto fue calculado utilizando paridad par, conformado por 4 bits por payload. La regla indicaba que si un dígito hexadecimal convertido a binario tenía una cantidad impar de "unos", el bit de paridad correspondiente era 1 (para volverlo par); si ya era par, era 0.

#### Reporte Recibido Rx:

|||
| :--- | :--- |
| **Nombre de mi Grupo** | The lords of Pings |
| **IP de mi grupo** | 10.5.0.1 |
| **IP Origen del paquete recibido** | 10.4.0.1 |
| **Payload Recibido** | `03BF EB97` |
| **CRC / EDAC recibido** | `0010 1001` |
| **Payload Íntegro** | NO |

#### Justificación de la detección de errores:

Comprobando el mensaje mediante la regla de paridad par contra el EDAC de 4 bits recibido, detectamos que de los dos payloads que conformaban el mensaje, uno era correcto (03BF) y el otro era incorrecto (EB97).

Dado que respondimos NO a la integridad del payload EB97, procedimos a analizar cuáles podrían ser las secuencias hexadecimales potencialmente correctas que mantuvieran la paridad esperada. Entonces:


#### Reporte de Rx

* **Nombre de mi Grupo:**  The lords of Pings 
* **IP de mi grupo:** 10.5.0.1

#### Paquete Recibido:

* **IP Origen:** 10.4.0.1
* **Payload Recibida:** 03BF EB97
* **CRC:** 0010 1001 -> EDAC
* **Payload Integrador:** NO

Las posibles tramas originales válidas identificadas fueron:

**EB97 → MAL POSIBLES: E097, E397, E597, E697, E997, EA97, EC97, EF97.**






