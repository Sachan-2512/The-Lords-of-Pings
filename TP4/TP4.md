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

#### b) ¿Cuál es la diferencia entre serialización binaria y no binaria? Buscar ejemplos, ventajas y desventajas de cada una.



### 2) Desplegaremos un servidor TCP multi-hilo: 

**- Si realizas esta actividad de forma presencial, lo desplegamos en una PC virtual en clases que usaremos entre todos.**

#### a) Serializaremos nuestros paquetes en JSON, con la siguiente morfología:

```
{
“group”: “The Lords of Pings”,
“payload”: “Jueves 14 de Mayo TP4”
}
```
#### Y lo enviaremos utilizando PacketSender; verificar que nuestro mensaje llega correctamente al servidor y documentar.
#### Se recomienda tildar “persistent TCP” así no se abre y cierra conexión cada que se envía un mensaje:


### 3) Programaremos ahora una aplicación de cliente que nos permita enviar mensajes al servidor a través de una consola.

#### a) Nuestro cliente deberá poder configurarse con la IP y puerto de destino del servidor, estableciendo conexión con el mismo.

#### b) Nuestro cliente deberá serializar la información previo al envío de la misma, en el formato que el servidor admite.

#### c) Ejecutar nuestro cliente y verificar que los mensajes enviados lleguen correctamente al servidor.



### 4) Vamos a imbuir un poco de seguridad en nuestro sistema. Investiga e implementa alguna técnica de encriptación que te guste e implementar para cifrar la payload, SOLO LA PAYLOAD, de tu mensaje.

#### a) Implementa el cifrado en el lado del cliente.

#### b) Verificar que la carga útil llega cifrada al servidor.

#### c) Documentar las principales características de la técnica de cifrado que utilizaste.


### 5) OPCIONAL: Modifica el servidor para que sea capaz de descifrar tu carga útil. Desplega servidor y cliente en tu local, captura paquetes mostrando que los mismos están cifrados mientras viajan pero el servidor es capaz de decodificar la carga útil.
