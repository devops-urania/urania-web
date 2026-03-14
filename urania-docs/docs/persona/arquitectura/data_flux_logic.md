# Arquitectura y Flujo de Datos (Logic A)

## Visión General
El flujo **Logic A**  describe el ciclo de vida de almacenamiento y validación criptográfica de las decisiones algorítmicas dentro del Proyecto PERSONA. 

Este diseño garantiza que ninguna propuesta generada por agentes humanos o autónomos pase a formar parte de la memoria institucional o del data lake sin haber sido auditada, validada criptográficamente en la blockchain, y enriquecida correctamente.

## Fases del Flujo de Datos

### 1. Génesis y Bifurcación
El proceso se inicia cuando un **Agente** de primera línea emite una propuesta en formato JSON, denotada como $\{P\}$. En este punto, el flujo de datos se divide en dos caminos simultáneos:
* **Almacenamiento en Tránsito:** La propuesta $\{P\}$ se guarda de manera temporal en una base de datos de Firestore designada como `auxiliary-data`.
* **Aseguramiento Criptográfico:** A la propuesta original se le calcula un hash utilizando el algoritmo SHA-256, denotado como $\{\#\}$. Este hash es enviado al smart contract **EPublisher** en la red blockchain.

### 2. Consenso y Validación (StellarSigner y UraniaSmartAccount)
El smart contract `EPublisher` actúa como una sala de espera segura. La ejecución del flujo se detiene hasta que se cumplan las estrictas condiciones de gobernanza criptográfica:

* **Mecanismo de Aprobación:** La lógica de validación está implementada mediante un smart contract independiente llamado `UraniaSmartAccount`.
* **Política Multifirma (Umbral 3/4):** El contrato establece una topología multisig que exige un peso mínimo de 3 sobre 4 para autorizar la transacción en la red.
* **Distribución de Pesos:** Las firmas están distribuidas entre los tres fundadores (Matías, Franco y Julia), representados en el esquema como los nodos **M, F, J**. La firma criptográfica de cada fundador tiene un peso individual de 1.
* **Redundancia Institucional:** Por cuestiones de seguridad y continuidad de negocio, existe una cuarta firma delegada a la cuenta principal de Stellar (*Urania Institucional*).
* **Ejecución y Emisión:** Las autorizaciones son inyectadas por los fundadores utilizando la aplicación móvil nativa **StellarSigner**. Una vez que el contrato `UraniaSmartAccount` verifica que se ha alcanzado el umbral 3/4, el sistema libera la transacción y la red emite un **Evento de Stellar** que certifica la validez inmutable del hash $\{\#\}$.

### 3. Orquestación y Procesamiento (El Rol de Lucien)
El componente **Lucien** actúa como el nodo maestro de este flujo. Su función es auditar la blockchain y gestionar los permisos de escritura del sistema:
* **Monitoreo Activo:** Lucien audita el smart contract `UraniaEPublisher` en intervalos regulares de 24 horas.
* **Recuperación:** Al detectar eventos que contienen los hashes de las propuestas aprobadas, Lucien busca el JSON original ($\{P\}$) en la colección temporal de Firestore (`auxiliary-data`).
* **Delegación Controlada:** Lucien es la única entidad de la arquitectura con privilegios de escritura sobre las bases de datos permanentes. Para continuar el proceso, invoca al agente analítico **Distiller** y le cede temporalmente sus permisos de escritura.
* **Destilación:** Distiller procesa la propuesta y almacena la versión final e inmutable ($\{P^*\}$) en las bases de datos permanentes de Firestore.

### 4. Consolidación en el Lakehouse
Para cerrar el ciclo, Lucien retoma el control del flujo. Toma la propuesta original ($\{P\}$) y la enriquece con metadatos críticos:
* El comprobante del Evento de Stellar.
* Los costos computacionales y operativos incurridos por el agente Distiller.

Este paquete de información consolidada (`data`) es finalmente empaquetado y cargado por Lucien  en el repositorio central de Urania, bajo la ruta `gcs://urania-lakehouse/raw/`.
