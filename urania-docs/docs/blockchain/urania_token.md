# UraniaTokenContract (URN)

El contrato `UraniaToken` implementa el token interno de la empresa, denominado **"Urania Token" (URN)**. 

Aunque su emisión y distribución son gestionadas de forma transversal por los agentes autónomos del **Proyecto PERSONA**, su utilidad principal está ligada a las políticas internas de Urania. El token está diseñado como un sistema para recompensar las contribuciones del equipo, estableciendo la base técnica para que en el futuro estos tokens puedan ser intercambiados por dinero o utilizados como poder de voto en la gobernanza interna.

El contrato cumple con funciones básicas del estándar SEP-41 de Stellar, pero añade una capa estricta de control de acceso (basada en roles de OpenZeppelin) y una *AllowList* (lista blanca) nativa para restringir quién puede operar con el activo.

---

## Configuración Inicial y Roles

Al momento de su despliegue (`__constructor`), el contrato inicializa la metadata del token (Nombre: "Urania Token", Símbolo: "URN", Decimales: 7) y distribuye los permisos operativos en un esquema de tres roles jerárquicos:

1. **Admin (Administrador):** Asignado a la `UraniaSmartAccount`. Posee el control absoluto sobre la gobernanza del contrato.
2. **Writer (Emisor):** Asignado inicialmente a `UraniaEPublisher`. Es el rol técnico encargado de la creación (minting) de nuevos tokens, operado en la práctica por los agentes autónomos bajo autorización del Admin.
3. **Manager (Gestor):** Asignado inicialmente a la cuenta del fundador Matías. Es el rol operativo encargado de administrar qué usuarios tienen permitido interactuar con el token.

*Nota: Al desplegarse el contrato, el Admin (`UraniaSmartAccount`) es agregado automáticamente a la AllowList.*

---

## Sistema de Lista Blanca (Native AllowList)

A diferencia de un token público, URN es un token permisionado. Ninguna cuenta puede recibir o enviar tokens a menos que haya sido explícitamente autorizada.

Las funciones que controlan este sistema son de acceso exclusivo para el rol **Manager**:

* **`allow_user`**: Autoriza a una cuenta (`user`) a poseer y transferir tokens URN.
* **`disallow_user`**: Revoca la autorización de una cuenta.
* **`is_allowed`**: Función de consulta pública que devuelve un valor booleano indicando si una cuenta está autorizada.

*Importante: Si un usuario intenta realizar o recibir una transferencia sin estar en la AllowList, la transacción fallará (`panic!("Una de las cuentas no esta autorizada para operar")`).*

---

## Emisión y Quema de Tokens (Mint & Burn)

La gestión del suministro total (`TotalSupply`) está dividida por razones de seguridad:

| Método | Rol Requerido | Propósito |
| :--- | :--- | :--- |
| **`writer_mint`** | `Writer` | Permite crear (`mintear`) una cantidad positiva de tokens y asignarlos a una cuenta destino (`to`). |
| **`admin_burn`** | `Admin` | Permite destruir (`quemar`) tokens de cualquier cuenta específica (`from`) sin requerir la firma del poseedor. Esto es vital para aplicar políticas internas estrictas. |

---

## Operaciones Estándar y Metadatos

El contrato expone las funciones estándar de lectura y transferencia requeridas por las wallets y la red Soroban:

* **`transfer`**: Transfiere tokens de la cuenta `from` a la cuenta `to`. Requiere la firma del emisor (`from.require_auth()`) y que ambas cuentas estén en la AllowList.
* **`balance`**: Devuelve el saldo actual de una cuenta específica.
* **`total_supply`**: Devuelve la cantidad total de tokens URN en circulación.
* **`name` / `symbol` / `decimals`**: Devuelven los metadatos estáticos del token ("Urania Token", "URN", 7).

---

## Gestión Administrativa y Actualizaciones

Las siguientes funciones de infraestructura están reservadas exclusivamente para el **Admin** (`UraniaSmartAccount`):

* **`set_admin`**: Transfiere el rol de administrador a una nueva cuenta y la añade a la AllowList.
* **`add_manager` / `add_writer`**: Permite al administrador delegar estos roles operativos a nuevas cuentas según cambien las necesidades de infraestructura de Urania o del Proyecto PERSONA.
* **`upgrade`**: Permite la actualización del código WASM del contrato de forma segura mediante la interfaz `UpgradeableInternal`.
