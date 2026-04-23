TP3

1) Investigación conceptual (respuestas breves). Responder en forma concisa.

a) ¿Qué es SSH y qué problema resuelve?

SSH (Secure Shell) es un protocolo de red que permite conectarse a otra computadora de forma remota y segura.
Resuelve el problema de que antes (ej: Telnet) los datos viajaban sin protección, mientras que SSH cifra la comunicación y evita que la intercepten.

b) Diferencia entre autenticación y cifrado

Autenticación: verifica quién sos (tu identidad).
Cifrado: protege la información para que nadie la pueda leer mientras viaja.

c) ¿Qué es una clave pública y una clave privada?

Son dos claves que funcionan juntas:

Clave pública: se puede compartir con cualquiera.
Clave privada: es secreta y solo la tiene el dueño.
Se usan para autenticar y cifrar datos en sistemas como SSH.

d) ¿Por qué la clave privada no debe compartirse?

Porque es la que demuestra tu identidad.
Si alguien la obtiene, puede hacerse pasar por vos y acceder a sistemas como si fuera el dueño.

e) ¿Qué ventajas tienen las claves SSH frente a contraseñas?

Son más seguras (no se envían por la red).
Difíciles de adivinar o romper.
Permiten automatizar conexiones sin escribir contraseña.
Reducen riesgos como phishing o robo de credenciales