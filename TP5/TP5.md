# TP5: Infraestructura vs Tráfico de Red

### Asignatura: Redes de Computadoras

**Facultad de Ciencias Exactas, Físicas y Naturales (UNC)**

---

* **Grupo:** The Lords of Pings
* **Profesores:** Facundo Oliva Cuneo y Santiago Martin Henn

### Integrantes y Contacto

| Nombre y Apellido | Correo Electrónico |
| :--- | :--- |
| **Pablo Castilla** | _pablo.castilla@mi.unc.edu.ar_ |
| **Javier A. Fatu** | _javier.fatu@mi.unc.edu.ar_ |
| **Enzo L. Laura Surco** | _enzo.laura.surco@mi.unc.edu.ar_ |
| **Saqib D. Mohammad Cabrejos** | _saqib.mohammad@mi.unc.edu.ar_ |

---

**Objetivos:** 
- Comprender cómo una arquitectura de servicios responde ante distintos tipos de tráfico.
- Relacionar componentes de infraestructura cloud con conceptos de redes: ruteo, balanceo de carga, almacenamiento, bases de datos, caché, colas y filtrado de tráfico malicioso.
- Analizar fallas, cuellos de botella y decisiones de escalabilidad.

**Requisitos:**
- Computadora(s) con acceso a internet.
- Navegador web moderno.

## Contexto

En este laboratorio se utilizó *Server Survival* como simulador de infraestructura. El juego representa un sistema que recibe tráfico de distintos tipos y debe procesarlo correctamente, manteniendo equilibrio entre presupuesto, reputación y salud de los servicios.

Aunque el entorno es lúdico, los conceptos subyacentes son reales: un sistema mal diseñado puede colapsar por sobrecarga, distribución ineficiente del tráfico, ausencia de caché, falta de filtrado ante ataques o saturación de la base de datos.

## Despliegue del juego

El simulador se encuentra disponible clonando el repositorio <https://github.com/pshenok/server-survival> o accediendo a la versión desplegada en <https://pshenok.github.io/server-survival/> (aunque esta opción podría no estar disponible). Basta con abrir `index.html` en el navegador para comenzar.

## Desarrollo

### 1) Reconocimiento de arquitectura

Se ingresó al juego y se identificaron los componentes disponibles junto con la función que cumple cada uno.

#### Para cada componente se respondió brevemente:

* a) ¿Qué problema resuelve?
* b) ¿En qué capa o capas del modelo TCP/IP podríamos ubicar su función principal?
* c) ¿Qué pasaría si ese componente falta en una arquitectura real?

| Componente | Problema que resuelve | Capa TCP/IP | Si falta |
|---|---|---|---|
| 🔥 Firewall | Bloquea tráfico malicioso (DDoS, bots, fraude) antes de que alcance el sistema | Red / Transporte | El tráfico malicioso ingresa sin restricciones, provocando pérdida de reputación por *Fraud Leak* y posible caída del sistema |
| 🛡️ API Gateway | Limita las solicitudes entrantes por segundo (*rate limiting*: 20/40/80 RPS según *tier*); las solicitudes excedentes se regulan con una penalización de reputación reducida (−0.2 vs. −1.0 por fallo) | Aplicación | El tráfico excesivo alcanza los componentes internos sin regulación, sobrecargando colas y nodos de cómputo de forma directa |
| ⚖️ Load Balancer | Distribuye el tráfico entrante entre múltiples nodos mediante Round Robin | Transporte / Aplicación | Un único nodo concentra toda la carga, se satura y falla |
| 📬 Queue | Actúa como búfer de hasta 200 solicitudes, absorbiendo picos de tráfico antes del nodo de cómputo | Aplicación | Los picos de solicitudes por segundo desbordan directamente el nodo de cómputo, desencadenando fallos en cascada |
| ⚙️ Compute | Procesa todos los tipos de solicitudes y las enruta hacia el servicio de *backend* correspondiente | Aplicación | Sin procesamiento, ninguna solicitud puede completarse |
| ⚡ Serverless Function | Variante de cómputo con autoescalado (capacidad de 30) y facturación por solicitud ($0.03/req); resulta ideal para tráfico esporádico o de bajo volumen | Aplicación | Se pierde la capacidad de escalar automáticamente, lo que incrementa los costos fijos al requerir nodos de cómputo permanentemente activos |
| 🗄️ SQL DB | Almacena datos estructurados y gestiona tráfico READ, WRITE y SEARCH (300 ms por solicitud) | Aplicación | Sin persistencia de datos, las solicitudes READ, WRITE y SEARCH fallan |
| 📄 NoSQL | Procesa solicitudes READ y WRITE con mayor velocidad y menor costo que SQL (150 ms vs. 300 ms), aunque no soporta SEARCH | Aplicación | Toda la carga de datos no relacionales recae sobre la SQL DB, reduciendo su rendimiento |
| 🧠 Cache | Capa de memoria intermedia con un *hit rate* del 35–65 %; las consultas resueltas en caché no impactan la base de datos | Aplicación | Todas las solicitudes acceden directamente a la base de datos, incrementando la latencia y la carga del sistema |
| 🌍 CDN | Sirve tráfico STATIC (imágenes, CSS, JS) con un 90 % de *cache hit rate* desde el almacenamiento | Aplicación | El tráfico estático consume recursos de cómputo de forma innecesaria |
| 🗃️ Storage | Almacena archivos estáticos y *uploads* (imágenes, audio, etc.); destino del tráfico STATIC y UPLOAD | Aplicación | Las solicitudes STATIC y UPLOAD fallan al carecer de almacenamiento persistente |
| 🔍 Search Engine | Procesa tráfico SEARCH tres veces más rápido que SQL DB (100 ms vs. 300 ms); acepta exclusivamente consultas SEARCH | Aplicación | Las búsquedas se derivan a la SQL DB, saturando conexiones y triplicando la latencia |
| 🔁 Réplica | Procesa tráfico READ con mayor velocidad que la base de datos principal (200 ms vs. 300 ms); requiere conexión a una SQL o NoSQL DB | Aplicación | Toda la carga de lectura recae sobre la base de datos principal, limitando su capacidad para atender escrituras y búsquedas |

### 2) Tipos de tráfico

| Tipo de tráfico | Ejemplo real | Componente recomendado | Riesgo si se procesa incorrectamente |
|---|---|---|---|
| **STATIC** | Logotipos, archivos CSS, paquetes de JavaScript | Storage → CDN (caché) | Sin CDN ni Storage, el tráfico estático consume recursos de cómputo innecesariamente; dado su 90 % de *cache hit rate*, prescindir de estos componentes triplica la carga sobre el *backend* |
| **READ** | Consultar un *feed* de inicio, visualizar un perfil de usuario | Cache → Réplica → SQL DB | Con solo un 40 % de *cache hit rate* y sin réplica de lectura, toda la carga recae sobre la base de datos principal, saturando conexiones y elevando los tiempos de respuesta |
| **WRITE** | Registrar una cuenta, publicar un artículo, confirmar una compra | Queue → Compute → SQL/NoSQL DB | Sin cola, los picos de escritura desbordan el nodo de cómputo; sin base de datos, se produce pérdida de datos críticos o *deadlocks* en el motor transaccional |
| **UPLOAD** | Subir una foto de perfil, adjuntar un archivo de audio | Compute → File Storage | Es el tipo de tráfico con mayor demanda de procesamiento y nunca se almacena en caché; sin File Storage dedicado, agota el disco de los servidores y colapsa el servicio |
| **SEARCH** | Buscar productos mediante palabras clave en una barra de *e-commerce* | Cache → Search Engine | Con solo un 15 % de *cache hit rate* y procesamiento intensivo, sin Search Engine las consultas se derivan a la SQL DB (300 ms vs. 100 ms), lo que triplica la latencia y bloquea conexiones concurrentes |
| **ATTACK** | Ataque DDoS o *bots* maliciosos | Firewall (WAF) | Sin Firewall, el tráfico malicioso alcanza el nodo de cómputo como *Fraud Leak*: se degrada la reputación de inmediato, se consumen recursos legítimos y se incrementa el riesgo de *downtime* total |

### 3) Prueba de colas (*Queues*)

Se construyó una infraestructura mínima para evaluar el comportamiento de las colas. En modo Sandbox se desplegó el siguiente esquema:

El flujo sigue un orden secuencial de izquierda a derecha: el tráfico se origina en Internet, atraviesa el Firewall, ingresa a la Cola (*Queue*) y finaliza en el nodo de cómputo.

![image](https://hackmd.io/_uploads/ry0TRikbfg.png)
##### Figura 1: Infraestructura mínima para la prueba de colas

### 3.1. Fase de incremento del tráfico

Al incrementar el ***Traffic Rate***, se produjo un aumento en el volumen de tráfico entrante desde Internet. La composición de este tráfico dependió de la configuración previamente establecida para los distintos tipos de solicitudes (STATIC, READ, WRITE, UPLOAD, SEARCH, ATTACK), descriptos en el inciso anterior. Dicho volumen atravesó el Firewall y comenzó a acumularse en la cola. La cantidad de tráfico retenido en este punto quedó condicionada exclusivamente por las características técnicas de la cola: el tamaño de su búfer y la velocidad de liberación hacia el nodo de cómputo.

![image](https://hackmd.io/_uploads/ry0Gx3kWzl.png)
##### Figura 2: Fase de incremento del tráfico

### 3.2. Fase de reducción de tráfico

Al disminuir el ***Traffic Rate*** abruptamente a 0 %, el ingreso de nuevo tráfico desde Internet se interrumpió por completo. Sin embargo, el sistema continuó operando: las solicitudes que ya se encontraban almacenadas en el búfer de la cola se fueron liberando de manera progresiva hacia el nodo de cómputo para su procesamiento, hasta que la cola se vació.

![image](https://hackmd.io/_uploads/rJdXQn1ZMx.png)
##### Figura 3: Fase de reducción del tráfico

### 4) Primera infraestructura mínima

La arquitectura propuesta debía resolver el procesamiento de:

- Tráfico estático y *uploads*.
- Lecturas y escrituras de datos.
- Búsquedas.
- Ataques o tráfico malicioso.

En **modo Sandbox**, se modificaron tanto la distribución porcentual del tráfico como la tasa general. A continuación se documenta cada etapa con capturas:

- a) La arquitectura inicial.
- b) El presupuesto inicial.
- c) El estado de salud de los servicios.
- d) El momento en que la arquitectura comenzó a fallar, si ocurrió.

***Para esta configuración, la composición porcentual de los distintos tipos de solicitudes se conservó en sus valores por defecto. La prueba consistió en someter la infraestructura a una carga creciente, escalando únicamente la tasa de tráfico general.***

![image](https://hackmd.io/_uploads/rkrtDnkZGg.png)
##### Figura 4: Configuración inicial del tráfico

#### a) Arquitectura inicial

Se planteó la arquitectura del ejercicio anterior con la distribución de tráfico por defecto, pero se introdujeron modificaciones significativas para atender de forma "efectiva" cualquier tipo de solicitud:

![image](https://hackmd.io/_uploads/B1agDygWGl.png)
##### Figura 5: Arquitectura de la infraestructura inicial

#### b) Presupuesto inicial

El presupuesto inicial fue de $2000, que tras el despliegue de la infraestructura se redujo a $1620. Si bien existía la posibilidad de aplicar *upgrades* a los componentes, en esta instancia se optó por no hacerlo.

![image](https://hackmd.io/_uploads/SykNDkg-zx.png)
##### Figura 6: Presupuesto posterior al despliegue de la arquitectura inicial

#### c) Estado de salud de los servicios

Al momento del despliegue, todos los servicios se encontraban en estado saludable.

![image](https://hackmd.io/_uploads/HJUswJebMx.png)
##### Figura 7: Estado inicial de los servicios

#### d) Momento en que la arquitectura comenzó a fallar

Para provocar el primer fallo con esta arquitectura sin modificaciones ni *upgrades*, se incrementó el ***Traffic Rate (TR)*** de forma gradual. Los fallos iniciales se debieron a los límites de capacidad de la cola, el nodo de cómputo, el almacenamiento de archivos y la base de datos. En particular, la cola procesaba un máximo de 50 solicitudes y el único nodo de cómputo podía atender hasta 4 solicitudes simultáneas. Al superar el 5 % de TR, comenzaron a producirse fallos de tipo ***RD Read***, dado que el nodo de cómputo no era capaz de procesar el volumen de solicitudes que le llegaba desde la cola.

![image](https://hackmd.io/_uploads/B1lgmglbMx.png)
##### Figura 8: Comienzo de fallos en la arquitectura

Esta limitación en el procesamiento generó un cuello de botella en la cola, lo que provocó fallos adicionales de tipo ***WR Write***. La combinación de la saturación del nodo de cómputo con el desbordamiento de la cola desencadenó errores en cascada, incluyendo fallos de tipo ***UP Upload*** y ***SR Search***.

![image](https://hackmd.io/_uploads/BkfD8exbzx.png)
##### Figura 9: Fallos encadenados en la arquitectura

Esta situación derivó en una degradación sostenida de la reputación. Para superar estas limitaciones, fue necesario escalar la infraestructura de modo que soporte tasas de tráfico cada vez más altas, así como aumentar las capacidades de componentes clave: nodos de cómputo, bases de datos SQL/NoSQL, caché, réplica de lectura, motor de búsqueda y API Gateways. Esto se logró distribuyendo la carga de manera proporcional a la capacidad de cada componente, anticipándose así a los escenarios de mayor estrés y minimizando los errores.

**TR = 75 req/s**
![image](https://hackmd.io/_uploads/HkDYslgZzg.png)
##### Figura 10: Arquitectura bajo Traffic Rate de 75 req/s

**TR = 160 req/s**
![image](https://hackmd.io/_uploads/B1ZnU-lZfl.png)
##### Figura 11: Arquitectura bajo Traffic Rate de 160 req/s

**TR = 200 req/s**
![image](https://hackmd.io/_uploads/S1TpdZeWGe.png)
##### Figura 12: Arquitectura bajo Traffic Rate de 200 req/s

En conclusión, los fallos del sistema se originaron al depender de componentes individuales con capacidades de procesamiento restrictivas. Para mitigar este problema, resultó indispensable escalar la infraestructura de forma horizontal, distribuyendo la carga entre múltiples instancias. Sin embargo, dicho escalado no debe ser arbitrario: el diseño debe buscar siempre el equilibrio óptimo entre rendimiento y costos operativos.

### 5) Escalabilidad y balanceo

Se modificó la arquitectura del punto anterior con el objetivo de soportar un mayor volumen de tráfico. Se evaluaron al menos dos estrategias distintas:

- Agregar más capacidad de cómputo.
- Agregar balanceador de carga.
- Agregar caché.
- Agregar réplicas de lectura.
- Agregar cola de mensajes.
- Separar servicios según tipo de tráfico.

Para cada estrategia se documentó el siguiente análisis:

**¿Escalar horizontalmente siempre mejora el sistema?** Se justifica con evidencia del simulador.

**Agregar más capacidad de cómputo:**
La efectividad de esta estrategia depende del *Traffic Rate* al que se someta el sistema y de la naturaleza de las solicitudes. En el inciso anterior se demostró que un solo nodo de cómputo soportaba 4 req/s sin inconvenientes según su capacidad de carga inicial (sin evolucionar). Por lo tanto, agregar nodos adicionales resulta imprescindible cuando el volumen de solicitudes supera a la capacidad de procesamiento de los nodos, pero no aporta valor significativo si el cuello de botella se encuentra en otro componente.

**Agregar balanceador de carga:**
Esta estrategia cobra sentido únicamente cuando se dispone de múltiples instancias de cómputo, ya que su función consiste en distribuir el tráfico entre ellas de forma equitativa. Sin múltiples nodos destino, el balanceador carece de propósito.

**Agregar caché:**
Esta estrategia resulta oportuna cuando la base de datos se encuentra saturada por tráfico de tipo *READ* y *SEARCH*, especialmente si múltiples instancias de cómputo realizan consultas simultáneas. La caché reduce la carga sobre la base de datos al resolver consultas frecuentes sin acceder a ella (cabe recordar que el tráfico *WRITE* nunca se almacena en caché sino que se escribe directamente en la base de datos).

**Agregar cola de mensajes:**
Incorporar colas adicionales es pertinente en aplicaciones con picos de tráfico impredecibles, ya que permiten almacenar temporalmente las solicitudes y distribuirlas de forma controlada hacia los nodos de cómputo, evitando su saturación inmediata.

**Separar servicios según tipo de tráfico:**
Esta estrategia constituye una buena práctica desde la perspectiva de la mantenibilidad a largo plazo. La segmentación permite aislar fallos, identificar rápidamente su origen y aplicar soluciones dirigidas sin afectar al resto del sistema.

**Agregar réplicas de lectura:**
Esta estrategia es beneficiosa cuando la naturaleza del tráfico se compone predominantemente de consultas de lectura. Las réplicas procesan solicitudes READ un 33 % más rápido que la base de datos principal (200 ms vs. 300 ms), aliviando la carga sobre esta última para que se concentre en escrituras y búsquedas.

### 6) Modo Supervivencia

Se diseñó una arquitectura inicial robusta y se intentó sobrevivir el mayor tiempo posible en el modo *Survival*, mejorando la infraestructura de forma progresiva. A continuación se documenta la arquitectura final (al momento del fallo), explicando:

- Por qué se eligió cada componente.
- Qué tipo de tráfico atiende cada uno.
- Qué cuello de botella apareció primero.
- Qué componente se escalaría con mayor presupuesto.

**La arquitectura que mayor resistencia demostró en modo *Survival* fue la siguiente:**

![image](https://hackmd.io/_uploads/BkCvJw--Mg.png)
##### Figura 13: Arquitectura elegida en modo *Survival*

El criterio de diseño consistió en distribuir las cargas de forma equitativa entre los componentes, considerando sus límites de capacidad individuales y el contexto de supervivencia, donde el *Traffic Rate* se incrementa progresivamente con el transcurso del tiempo.

**Justificación de la elección de cada componente:**

* **Firewall:** Constituye la primera línea de defensa, bloqueando el tráfico malicioso durante toda la partida de supervivencia.
* **CDN:** Filtra el tráfico de tipo *STATIC* para su posterior almacenamiento en el *File Storage*, evitando que consuma recursos de cómputo.
* **File Storage:** Funciona como destino de archivos estáticos y subidos por el usuario, atendiendo tráfico de tipo *STATIC* y *UPLOAD*.
* **API Gateway:** Protege al sistema del tráfico excesivo de tipo *READ*, *WRITE*, *UPLOAD* y *SEARCH* mediante la limitación de solicitudes por segundo (*rate limiting*). De esta manera, se previene la sobrecarga de las colas y se reducen los fallos que degradan la reputación.
* **Colas:** Resultan esenciales para que la arquitectura sea resiliente ante aumentos repentinos de tráfico. No obstante, su capacidad limitada las hace dependientes de operar en paralelo cuando el volumen lo requiere. En esta configuración se utilizaron tríadas de colas por cada balanceador de carga, permitiendo una distribución más controlada de las solicitudes. Las colas heredan los mismos tipos de tráfico que la API Gateway.
* **Balanceador de carga:** Al igual que los demás componentes, posee un límite de capacidad que generaba cuellos de botella en las colas de entrada, cada vez más pronunciados conforme el *Traffic Rate* aumentaba. Por ello, se optó por seccionar una tríada de colas para cada balanceador, distribuyendo el tráfico hacia los nodos de cómputo de destino de forma más eficiente.
* **Nodo de cómputo:** Se encarga del procesamiento de los distintos tipos de solicitudes provenientes de la API Gateway; sin este componente, ninguna solicitud podría completarse. Se desplegaron cinco nodos de cómputo a la salida de cada balanceador, dado que la velocidad creciente de las solicitudes y la capacidad limitada de cada nodo exigían instancias adicionales para evitar estrés de procesamiento y cuellos de botella.
* **NoSQL DB:** Atiende solicitudes de tipo *READ* y *WRITE* con mayor velocidad que la SQL DB (150 ms vs. 300 ms), aunque carece de soporte para consultas *SEARCH*. Para cubrir esta limitación, es necesario recurrir al componente *Search Engine* o a una base de datos SQL.
* **Memory Cache:** Gestiona en memoria las consultas más frecuentes dirigidas a la base de datos (SQL o NoSQL), aliviando su carga y reduciendo la latencia de respuesta.
* **Read Replica:** Procesa una copia del tráfico de tipo *READ* que llega a la base de datos, permitiéndole concentrarse en consultas *WRITE* (SQL y NoSQL) y *SEARCH* (SQL). Esto mejora el rendimiento general cuando el volumen de consultas concurrentes es elevado.
* **SQL DB:** Gestiona las solicitudes de tipo *READ*, *WRITE* y *SEARCH* procesadas por los nodos de cómputo. Si bien posee un límite de capacidad, este no representó un problema significativo gracias a la distribución del tráfico con la base de datos NoSQL y al soporte de la caché y la réplica de lectura.

**Cuellos de botella que aparecieron (en orden cronológico):**

1. **Capacidad de los nodos de cómputo:** Fue necesario iniciar la partida con al menos dos nodos, ya que un único nodo se sobrecargaba rápidamente y generaba fallos en múltiples tipos de tráfico.
2. **Capacidad de las colas:** Al alcanzar un determinado *Traffic Rate*, una sola cola a la entrada del balanceador resultó insuficiente para sostener el flujo de solicitudes por segundo: se llenaba con rapidez y producía errores por pérdida de solicitudes. Para mitigarlo, se agregó una API Gateway que absorbía cargas mayores antes de derivarlas a las colas.
3. **Capacidad de los balanceadores de carga:** A medida que el volumen despachado por las colas crecía, el único balanceador disponible generaba demoras en la distribución hacia los nodos de cómputo, lo que producía un cuello de botella retroactivo en las colas y degradaba la reputación rápidamente. La solución consistió en agregar balanceadores adicionales, asignando a cada uno un grupo exclusivo de colas y nodos de cómputo.
4. **Capacidad de las bases de datos:** No se presentaron problemas mayores gracias a la distribución del tráfico entre las bases de datos NoSQL y SQL. En esta última, se complementó con caché y réplica de lectura, manteniendo las cargas sanitizadas. Como observación de mejora, el uso del componente *Search Engine* para las consultas de tipo *SEARCH* habría sido beneficioso, dado que según la documentación procesa dichas consultas tres veces más rápido que SQL. Adicionalmente, se podría haber aliviado la carga de la SQL DB compartiendo la caché y la réplica de lectura con el motor de búsqueda.

La siguiente imagen muestra con mayor detalle la gestión optimizada del tráfico hacia las bases de datos:

![image](https://hackmd.io/_uploads/ryEYRqZbfl.png)
##### Figura 14: Gestión del tráfico hacia la base de datos optimizada

**¿Por qué falló la arquitectura y qué componentes podrían escalarse para evitarlo?**

***Surviving Final Score:***
![image](https://hackmd.io/_uploads/BJONH9WWGg.png)
##### Figura 15: Puntaje final alcanzado

![image](https://hackmd.io/_uploads/BJx3yv-Wfg.png)
##### Figura 16: Evento que originó el fallo de la arquitectura (TRAFFIC BURST ×30)

La arquitectura parecía preparada para soportar las solicitudes por segundo del *Traffic Rate* sostenido. Sin embargo, un evento inesperado de *TRAFFIC BURST ×30* sobrecargó de forma simultánea cada grupo de colas conectadas a las API Gateway, que debían proteger al sistema del tráfico excesivo. Para resolver esta problemática, el componente a escalar horizontalmente serían las colas, acompañadas de un balanceador de carga adicional entre la API Gateway y cada grupo de colas. Además, se aprovecharía dicho balanceador para distribuir parte del tráfico hacia pares adicionales de nodos de cómputo, aliviando la presión sobre las colas y evitando su saturación ante eventos de tipo *TRAFFIC BURST ×30*. Esta solución fue validada en modo Sandbox.

![image](https://hackmd.io/_uploads/SJpe2iW-Gg.png)
##### Figura 17: Arquitectura final para soportar 250 req/s y TRAFFIC BURST ×30

## Conclusiones

La simulación interactiva permitió comprender las responsabilidades de cada componente dentro de la infraestructura y los roles que desempeñan en la segregación del tráfico proveniente de Internet. A través de la experimentación progresiva, se identificaron los tipos de errores que surgen al estresar el sistema con distintos volúmenes y tipos de solicitudes, y se desarrolló la capacidad de gestionar la infraestructura para escalar los componentes de forma anticipada a los cuellos de botella.

Asimismo, se evidenció la importancia de conocer los límites de capacidad de cada componente y de optimizar el flujo de cada tipo de tráfico. El acompañamiento de las bases de datos con caché, réplicas de lectura y motor de búsqueda demostró ser fundamental para atender las consultas de tipo *SEARCH*, *READ* y *WRITE* con la menor latencia posible. Por último, se comprendió la función crítica del Firewall como filtro de tráfico malicioso y del File Storage como gestor de las solicitudes *UPLOAD* y *STATIC*.