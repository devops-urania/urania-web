# UraniaEPublisher

El contrato `UraniaEPublisher` (Event Publisher) es una pieza fundamental de la arquitectura del **Proyecto PERSONA** y del ecosistema de Urania. Actúa como un notario digital descentralizado, encargado de emitir sellos de integridad criptográficos en la red Stellar/Soroban.

Su propósito principal es garantizar la autenticidad e integridad de la información antes de que esta sea persistida en la base de datos central de Urania. Toda carga de información requiere la revisión y autorización del consenso de los fundadores mediante la cuenta `UraniaSmartAccount`, la cual administra este contrato. Si la información carece del evento válido emitido por este contrato, es rechazada por el sistema.

---

## Arquitectura y Seguridad

* **Administración Centralizada:** Durante su despliegue (`__constructor`), el contrato asigna una dirección administradora (`DataKey::Admin`). En el entorno de producción de Urania, esta dirección corresponde a la `UraniaSmartAccount`.
* **Validación de Umbral:** Dado que `UraniaSmartAccount` es el administrador exclusivo, cualquier ejecución en `UraniaEPublisher` exige implícitamente que se haya alcanzado el umbral de firmas configurado (mayoría de los fundadores y/o cuenta institucional).
* **Control de Ciclo de Vida (TTL):** El contrato gestiona activamente la vigencia de sus datos en el estado de Soroban, extendiendo automáticamente el *Time-To-Live* (TTL) en cada ejecución entre un mínimo de ~3 días (`LOW_TTL`) y un máximo de ~15 días (`HIGH_TTL`).

---

## Flujo de Publicación y Eventos

El contrato ofrece dos vías principales para proponer y sellar información, emitiendo eventos específicos que luego son escuchados por un *Watcher* (monitor de eventos) conectado a la base de datos central.

### 1. Sello Criptográfico (Hash)
La función `publish_proposal` recibe un `proposal_hash` (de 32 bytes) que representa la huella digital de la información validada. 
* **Evento Emitido:** `Event`
* **Datos del Evento:** `proposal_hash` y el estado de la acción (`action`).

### 2. Sello de Texto Plano (String)
Para casos de prueba, o donde la propuesta requiere legibilidad directa en la blockchain, la función `publish_proposal_string` procesa la información como una cadena de texto.
* **Evento Emitido:** `EventTest`
* **Datos del Evento:** `proposal_string` y el estado de la acción (`action`).

---

## Ejecución Delegada (Proxy)

Ambas funciones de publicación están diseñadas para, opcionalmente, ejecutar lógica externa simultáneamente a la emisión del evento de integridad. 

Si se proveen los parámetros correspondientes (`target_contract`, `function_name`, `args`), el `UraniaEPublisher` invocará dicho contrato actuando como proxy. 
    
Dependiendo de si se realiza esta ejecución externa, el evento emitido registrará uno de los siguientes estados en el campo `action`:
* `LOG_ONLY`: Solo se registró el evento de integridad (no se proporcionaron datos para ejecución externa).
* `EXECUTED`: Se registró el evento y se ejecutó exitosamente la llamada al contrato destino.

---

## Métodos Administrativos

Las siguientes operaciones requieren estrictamente la autorización del administrador (`require_auth()`) y fallarán con un error `Unauthorized` si son llamadas por otra cuenta:

| Método | Propósito |
| :--- | :--- |
| `set_admin` | Permite transferir el rol de administrador a una nueva cuenta (útil para rotación de claves u optimización de la estructura). |
| `extend_ttl` | Permite al administrador extender manualmente la vigencia de la instancia del contrato en la red sin necesidad de publicar un evento. |
| `upgrade` | Actualiza el código compilado (WASM) del contrato, funcionalidad heredada de la interfaz `UpgradeableInternal`. |
