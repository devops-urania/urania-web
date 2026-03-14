# UraniaSmartAccount

El contrato `UraniaSmartAccount` es el gestor principal y administrador (Smart Account) del ecosistema de contratos inteligentes de Urania. Implementa un sistema de cuenta inteligente personalizado en la red Stellar/Soroban, diseñado específicamente para manejar los procesos multifirma (multisig) críticos de la empresa y del Proyecto PERSONA.

Este contrato está construido tomando como referencia los modelos y estándares de seguridad de OpenZeppelin, garantizando un control de acceso robusto y una ejecución delegada segura.

---

## Arquitectura y Configuración Inicial

Al momento de su despliegue, el contrato se inicializa con un contexto base (`base_founders_signatures`) que establece las reglas fundamentales de gobernanza. 

La configuración implementa una política de **umbral 3 de 4 (3/4)**, donde cada firma tiene un peso de `1`. Los cuatro firmantes delegados (`Delegated` en el estándar de OpenZeppelin) configurados son:

1. **Matías** (Fundador)
2. **Franco** (Fundador)
3. **Julia** (Fundadora)
4. **Cuenta Institucional de Urania**

Esta configuración asegura que cualquier acción crítica administrativa requiera el consenso de la mayoría de las partes interesadas.

---

## Interfaces y Traits Implementados

El contrato integra múltiples módulos funcionales para operar como una cuenta inteligente completa:

* **`CustomAccountInterface`**: Define el comportamiento principal de autenticación interceptando la verificación de firmas nativa de Soroban a través de la función `__check_auth`.
* **`SmartAccount`**: Proporciona el conjunto de herramientas para administrar dinámicamente las reglas de contexto, agregar o eliminar firmantes (`add_signer`, `remove_signer`) y gestionar políticas de acceso.
* **`ExecutionEntryPoint`**: Permite que el contrato actúe como un proxy para invocar funciones en otros contratos administrados mediante el método `execute`.
* **`UpgradeableInternal`**: Facilita la actualización segura del código del contrato (WASM), restringiendo esta capacidad exclusivamente a la propia cuenta administradora para evitar vulnerabilidades (`ContractError::Unauthorized`).

---

## Métodos Principales

A continuación se detallan las operaciones de escritura más relevantes del contrato. **Nota:** Todas estas funciones requieren autorización previa (`require_auth()`) del propio contrato.

| Método | Propósito |
| :--- | :--- |
| `add_context_rule` | Crea una nueva regla de contexto definiendo un nombre, vigencia, firmantes autorizados y políticas asociadas. |
| `update_context_rule_name` | Modifica el nombre identificador de una regla de contexto existente. |
| `update_context_rule_valid_until`| Actualiza el tiempo de expiración (vigencia) de una regla de contexto. |
| `add_signer` / `remove_signer` | Agrega o elimina un firmante delegado (`Signer`) de una regla de contexto específica. |
| `add_policy` / `remove_policy` | Asocia o desvincula una política (`Address` con sus parámetros) a una regla de contexto. |
| `execute` | Punto de entrada para que la cuenta inteligente envíe transacciones y ejecute funciones (`target_fn`) en contratos destino (`target`). |

---

## Manejo de Errores

El contrato define errores personalizados para un debugging más claro durante su ejecución:

* `ContractError::Unauthorized (1)`: Se dispara cuando una cuenta que no es el administrador (el propio contrato) intenta ejecutar una función reservada, como la actualización del contrato (Upgrade).
