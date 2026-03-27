# TP2: Armado y verificación de cables Cat5/Cat5e y Utilizacion de Equipos de Red y Analisis de Red

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


## Parte 1: Armado y verificación de cables Cat5/Cat5e bajo estándar T568A/B.

### 1) Investigar los pasos para crimpar un cable bajo la norma T568A/B DERECHO. No cruzado. Ver Fig:

![image](https://hackmd.io/_uploads/r1YM8w7sWl.png)

Para la construcción del cable se utilizaron los siguientes materiales:

* Cable UTP Cat5
* Conectores RJ45
* Pinza crimpeadora
* Trincheta y tijera

#### Procedimiento realizado:

En primer lugar, se realizó un corte del cable de aproximadamente 1 a 1.5 metros. Luego, utilizando una trincheta, se retiró alrededor de 5 cm de la cubierta externa del cable, dejando visibles los pares trenzados internos.

A continuación, con ayuda de un pequeño tubo de PVC o manualmente , se separaron y desenrollaron los conductores internos para facilitar su manipulación. Posteriormente, los cables fueron ordenados según la norma T568B (cable derecho), respetando la siguiente secuencia de colores:

1. Blanco/Naranja
2. Naranja
3. Blanco/Verde
4. Azul
5. Blanco/Azul
6. Verde
7. Blanco/Marrón
8. Marrón

![WhatsApp Image 2026-03-26 at 7.26.54 PM](https://hackmd.io/_uploads/SyOtFDQibl.jpg)


Una vez ordenados, se alinearon y estiraron los conductores, recortándolos de forma pareja para asegurar una correcta inserción en el conector.

Luego, se introdujeron los cables dentro del conector RJ45 verificando que cada conductor llegara hasta el fondo del mismo y respetando el orden establecido.

Finalmente, se utilizó la pinza crimpeadora para fijar el conector, asegurando el contacto entre los conductores y los pines metálicos del RJ45. Este procedimiento se repitió en ambos extremos del cable, manteniendo la misma norma, obteniendo así un cable derecho (no cruzado).

![WhatsApp Image 2026-03-26 at 7.26.55 PM](https://hackmd.io/_uploads/HkgiKDms-g.jpg)

**Nota: Obviamente hubo experiencias fallidas**

![WhatsApp Image 2026-03-26 at 7.26.54 PM (1)](https://hackmd.io/_uploads/Skf6KwXobx.jpg)


### 2) Construir 1 (un) cable por grupo, de 1 - 1.5 m. aproximadamente. Tipo DERECHO, NO CRUZADO.

Se construyó un cable UTP Cat5 de aproximadamente 1.2 metros de longitud, configurado como cable derecho bajo norma T568B en ambos extremos.

### 3) VERIFICAR la buena construcción de un cable. Para ello, buscar otro grupo e intercambiar cables. Realizarán:

#### a) Inspección visual para la calidad constructiva 

Se realizó una inspección visual del cable, verificando:

* Correcto orden de los colores según norma

* Que los conductores lleguen hasta el fondo del conector

* Que la cubierta externa del cable esté correctamente insertada en el RJ45

* Ausencia de cables sueltos o mal posicionados

* Corte uniforme de los conductores

#### b) Verificación eléctrica utilizando un tester para cables ethernet.

Para la verificación eléctrica, se utilizó un tester de cables Ethernet.

El procedimiento consistió en conectar ambos extremos del cable al tester y observar la secuencia de encendido de los indicadores.

Se obtuvo como resultado una correcta continuidad en los 8 pines (1 al 8), sin presencia de fallas como cortes, inversiones o cortocircuitos.

Esto indica que el cable se encuentra correctamente armado y funcional.

![Screenshot at 2026-03-26 22-45-25](https://hackmd.io/_uploads/SyfOcvXoWx.png)


### 4) Documentar con que grupo intercambiaron cables (pueden intercambiar más de una vez, no importa, mientras no tengan su propio cable). Tomar fotografías que evidencien el proceso técnico de verificación.

Se realizó el intercambio de cables con el grupo “Ethernautas V2”.

#### Evaluación del cable recibido:

Durante la inspección visual se observó que:

* El cable presentaba una correcta terminación
* No había separación entre la ficha RJ45 y la cubierta del cable
* Los conductores estaban correctamente alineados
* No se observaron cables sueltos ni mal posicionados

##### Prueba con tester:

Al verificar el cable con el tester, se observó continuidad completa desde el pin 1 hasta el pin 8, indicando una conexión correcta.

![Screenshot at 2026-03-26 22-46-02](https://hackmd.io/_uploads/r1uh5vmsbe.png)


Por lo tanto, se concluye que el cable del grupo evaluado está correctamente implementado y en buen estado de funcionamiento.



## Parte 2: Equipamiento físico, verificación y utilización de equipos de red y análisis de tráfico.

### 1) Utilizando internet y el datasheet del switch Cisco, documentar las características principales del mismo.

El switch Cisco Catalyst 2950 es un dispositivo de red diseñado para proporcionar conectividad en redes LAN, principalmente en la capa 2 del modelo OSI, permitiendo la conmutación eficiente de tramas Ethernet entre dispositivos.

a. El dispositivo es un switch administrable (managed) de configuración fija.

b. El switch dispone de: 12, 24 o 48 puertos 10/100 Mbps (Fast Ethernet). Algunos modelos incluyen puertos Gigabit uplink.

c. El switch ofrece rendimiento wire-speed, es decir, puede operar a máxima velocidad en todos sus puertos.

d. Hasta 13.6 Gbps de capacidad interna

e. Soporta hasta 8000 direcciones MAC y el switch permite crear redes virtuales (VLANs).

f. El switch puede administrarse mediante: CLI (línea de comandos), Interfaz web (Cisco Device Manager), SNMP.


### 2) Elaborar checklists (manuales, indicaciones) de procedimientos para las siguientes actividades:

Equipo utilizado: Cisco Catalyst 2950 Series
Software: PuTTY
Sistema operativo: Linux Mint

#### a) Conectar una PC al puerto de consola del switch Cisco a 9600 baudios utilizando PUTTY. Turnense para verificar el acceso a la consola del Switch.

1. Conexión física
2. Conectar el cable consola (RJ45–Serial)
3. Conectar el adaptador USB–Serial a la PC
4. Conectar el RJ45 al puerto de consola del switch
5. Verificación del puerto en Linux

Ejecutar en terminal:

```
dmesg | tail
```

Identificar el puerto asignado (ejemplo: /dev/ttyUSB0)

Permisos del dispositivo

Otorgar permisos al puerto serial:

```
sudo chmod 666 /dev/ttyUSB0
```

**Configuración en PuTTY**

* Tipo de conexión: Serial
* Serial line: /dev/ttyUSB0
* Speed (baud rate): 9600
* Data bits: 8
* Stop bits: 1
* Parity: None
* Flow control: None
Acceso a la consola

Abrir conexión en PuTTY
Presionar Enter
Verificar acceso a la CLI del switch

Se logró acceder correctamente a la interfaz de línea de comandos del switch.

![WhatsApp Image 2026-03-26 at 7.26.55 PM (1)](https://hackmd.io/_uploads/S1Y40PmjZg.jpg)

![WhatsApp Image 2026-03-26 at 7.26.55 PM (2)](https://hackmd.io/_uploads/rJzrCPXobl.jpg)


#### b) Acceder a las opciones de administración del switch y modificar claves de acceso.

Se logró acceder a la CLI del switch. No fue posible modificar las claves debido a:
- Desconocimiento de la contraseña previa
- Restricción de acceso al modo privilegiado

Aunque se podria haber hecho un RESET al switch devolviendolo al estado de fabrica pero no se realizo.

Sin embargo el procedimiento teorico es el siguiente:

Una vez dentro de la CLI:

```
enable
configure terminal
```

Configurar contraseña de modo privilegiado:

```
enable secret NUEVA_CLAVE
```

Configurar contraseña de consola:

```
line console 0
password NUEVA_CLAVE
login
exit
```

Guardar configuración:

```
write memory
```

#### c) Conectar computadoras al switch, configurar una red y testear conectividad.

No se realizo pero el procedimiento teorico seria el siguiente: 

**Conexión física***

a. Conectar cada computadora al switch mediante cables Ethernet (Parte 1)

b. Configuración de red (IP manual)

A las PCs se haria lo siguiente:

**PC1:**

```
IP: 192.168.1.1
Máscara: 255.255.255.0
```

**PC2:**

```
IP: 192.168.1.2
Máscara: 255.255.255.0
```

Verificación de conectividad

Desde una PC ejecutar:

```
ping 192.168.1.2
```

Análisis de resultados:

Si hay respuesta → conectividad correcta 
Si no → revisar:

1. Cableado
2. Configuración IP
3. Conexiones físicas

### 3) De a dos o más grupos por switch, conectarán una computadora por cada grupo al mismo utilizando los cables que tengan de la parte 1 de este TP. Por el amor de todo lo que es bueno espero que hayan verificado bien el cable. Verificar que pueden llegar a la PC de otro grupo usando ping o captura de paquetes.

NO SE IMPLEMENTO

Pero el procedimiento teorico es el siguiente:

1) Conexión física:

Cada grupo conecta su computadora al switch utilizando un cable Ethernet armado en la Parte 1 (cable derecho).
Se utilizan distintos puertos del switch para cada equipo.

* Resultado esperado:
Los LEDs de los puertos deben encenderse indicando conexión física (link).

2) Configuración de direcciones IP:

Cada computadora debe tener una dirección IP dentro de la misma red.

Ejemplo:

```
PC Grupo 1:
IP: 192.168.1.10
Máscara: 255.255.255.0
PC Grupo 2:
IP: 192.168.1.20
Máscara: 255.255.255.0
```

* Importante:

-  Las IP deben ser distintas
-  La máscara debe ser igual
- No es necesario gateway (porque están en la misma red)

3) Verificación de conectividad (Ping)

Desde una computadora, ejecutar:

```
ping 192.168.1.20
```

Y el resultado esperado:

Respuestas exitosas (Reply)
Indica que hay comunicación entre equipos.

