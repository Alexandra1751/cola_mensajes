Aquí tienes el README estructurado para las entregas 2, 3 y 4 del proyecto de Sistemas Distribuidos:

## Proyecto Integrador - Sistemas Distribuidos

### Índice
1. [Introducción](#introducción)
2. [Entrega 2: Cola de Mensajes](#entrega-2-cola-de-mensajes)
   - [Descripción del Proyecto](#descripción-del-proyecto)
   - [Requisitos](#requisitos)
   - [Instalación](#instalación)
   - [Uso](#uso)
   - [Ejecución de los Scripts](#ejecución-de-los-scripts)
   - [Estructura del Proyecto](#estructura-del-proyecto)
   - [Capturas de Pantalla](#capturas-de-pantalla)
   - [Video de Demostración](#video-de-demostración)
   - [Autores](#autores)
   - [Licencia](#licencia)
3. [Entrega 3: Coordinación de Instancias del Módulo de Almacenamiento](#entrega-3-coordinación-de-instancias-del-módulo-de-almacenamiento)
   - [Descripción](#descripción-1)
   - [Requisitos](#requisitos-1)
   - [Instalación](#instalación-1)
   - [Mecanismo de Asignación y Manejo de Roles](#mecanismo-de-asignación-y-manejo-de-roles)
   - [Comunicación entre Nodos](#comunicación-entre-nodos)
   - [Roles y Restricciones](#roles-y-restricciones)
   - [Ejecución](#ejecución-1)
4. [Entrega 4: Replicación en el Módulo de Almacenamiento y Funcionamiento de los Módulos Adicionales](#entrega-4-replicación-en-el-módulo-de-almacenamiento-y-funcionamiento-de-los-módulos-adicionales)
   - [Descripción](#descripción-2)
   - [Requisitos](#requisitos-2)
   - [Instalación](#instalación-2)
   - [Pruebas de Replicación y Recuperación de Fallos](#pruebas-de-replicación-y-recuperación-de-fallos)
   - [Ejecución](#ejecución-2)

## Introducción
Este proyecto es parte de la asignatura de Sistemas Distribuidos y tiene como objetivo principal la construcción de un prototipo funcional de los módulos necesarios para la transmisión, almacenamiento y verificación de datos de un censo poblacional.

## Entrega 2: Cola de Mensajes

### Descripción del Proyecto
Este proyecto consta de los siguientes módulos:
- Módulo de Cola de Mensajes
- Módulo de Captura de Datos
- Módulo de Validación

### Requisitos
- Python 3.x
- RabbitMQ
- Librerías de Python: pika

### Instalación

#### Paso 1: Instalación de RabbitMQ
##### Windows
1. Descarga e instala Erlang.
2. Descarga e instala RabbitMQ.
3. Agrega `sbin` de RabbitMQ al `PATH` (ejemplo: `C:\Program Files\RabbitMQ Server\rabbitmq_server-3.x.x\sbin`).
4. Inicia RabbitMQ:
   ```sh
   rabbitmq-server.bat
   ```

##### Ubuntu
1. Actualiza el sistema e instala RabbitMQ:
   ```sh
   sudo apt-get update
   sudo apt-get install rabbitmq-server
   sudo systemctl enable rabbitmq-server
   sudo systemctl start rabbitmq-server
   ```

##### Arch Linux
1. Actualiza el sistema e instala RabbitMQ:
   ```sh
   sudo pacman -Syu
   sudo pacman -S rabbitmq
   sudo systemctl enable rabbitmq.service
   sudo systemctl start rabbitmq.service
   ```

#### Paso 2: Instalación de las Librerías de Python
Asegúrate de tener `pip` actualizado:

##### Windows
```sh
python -m pip install --upgrade pip
```

##### Ubuntu y Arch Linux
```sh
sudo apt-get install python3-pip # Ubuntu
sudo pacman -S python-pip # Arch Linux
pip install --upgrade pip
```

Instala la librería `pika`:
```sh
pip install pika
```

#### Paso 3: Clonación del Repositorio
Clona este repositorio en tu máquina local:
```sh
git clone https://github.com/tu-usuario/proyecto-distribuidos.git
cd proyecto-distribuidos
```

### Uso

#### Módulo de Cola de Mensajes
El script `cola_mensajes.py` contiene la lógica para crear una conexión a RabbitMQ, enviar mensajes y recibir mensajes.

#### Módulo de Captura de Datos
El script `captura_datos.py` genera formularios de censo llenos de forma aleatoria y los envía a través de la cola de mensajes en formato JSON.

#### Módulo de Validación
El script `validacion.py` recibe formularios de la cola de mensajes, valida los datos y muestra el resultado de la validación.

### Ejecución de los Scripts
1. **Ejecutar el Módulo de Cola de Mensajes:**
   ```sh
   python cola_mensajes.py
   ```

2. **Ejecutar el Módulo de Captura de Datos:**
   ```sh
   python captura_datos.py
   ```

3. **Ejecutar el Módulo de Validación:**
   ```sh
   python validacion.py
   ```

### Estructura del Proyecto
- `cola_mensajes.py`: Módulo de Cola de Mensajes.
- `captura_datos.py`: Módulo de Captura de Datos.
- `validacion.py`: Módulo de Validación.
- `README.md`: Este archivo, que proporciona una guía detallada del proyecto.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

### Capturas de Pantalla
- Cola de Mensajes
- Captura de Datos
- Validación
- Interfaz RabbitMQ
- Verificación de Funcionamiento

### Video de Demostración
[Video de Demostración](https://drive.google.com/drive/folders/1xTfATcHGdZhrNQrjYwLuD7WDWdFdbilh?usp=sharing)

### Autores
- Marjorie Alexandra Monta Portilla
- David Antonio Fernandez Quituizaca
- Jessye Javier Solorzano Soriano

### Licencia
Este proyecto está licenciado bajo la Licencia MIT. Para más información, consulta el archivo LICENSE.

## Entrega 3: Coordinación de Instancias del Módulo de Almacenamiento

### Descripción
En esta entrega, se evaluará principalmente la coordinación de instancias del Módulo de Almacenamiento. Implementamos un modelo de líder-seguidores para manejar las operaciones de lectura y escritura.

### Requisitos
- Python 3.x
- Flask
- Requests

### Instalación

#### Paso 1: Instalación de las Librerías de Python
Asegúrate de tener `pip` actualizado:
```sh
pip install --upgrade pip
```

Instala las librerías necesarias:
```sh
pip install flask requests
```

### Mecanismo de Asignación y Manejo de Roles
El sistema utiliza un modelo de líder-seguidores. Al iniciar, una instancia puede ser configurada como líder y las demás como seguidores. El líder maneja tanto las lecturas como las escrituras, mientras que los seguidores solo manejan las lecturas.

### Comunicación entre Nodos
La comunicación entre nodos se realiza mediante endpoints REST, asegurando que todas las interacciones se realicen a través de la red IP.

#### Código Relevante
- **Añadir réplica:**
  ```python
  @app.route('/add_follower', methods=['POST'])
  def add_follower():
      follower_url = request.json.get('url')
      followers.append(follower_url)
      return jsonify({'message': 'Follower added'}), 200
  ```

- **Promover líder:**
  ```python
  @app.route('/leader', methods=['POST'])
  def promote_leader():
      new_leader_url = request.json.get('url')
      Thread(target=sync_data_with_leader, args=(new_leader_url,)).start()
      return jsonify({'message': 'Leader promoted'}), 200
  ```

### Roles y Restricciones
- **Líder:** Acepta tanto lecturas como escrituras y replica los datos a los seguidores.
- **Seguidores:** Solo aceptan operaciones de lectura y se sincronizan con el líder cuando se reconectan.

### Ejecución

1. **Ejecutar instancias del Módulo de Almacenamiento en diferentes puertos:**
   ```sh
   python almacenamiento.py
   ```

2. **Añadir réplicas en cada instancia:**
   ```sh
   curl -X POST http://localhost:5004/add_follower -H "Content-Type: application/json" -d '{"url": "http://localhost:5005"}'
   ```

## Entrega 4: Replicación en el Módulo de Almacenamiento y Funcionamiento de los Módulos Adicionales

### Descripción
Esta entrega se enfoca en la replicación de datos entre las réplicas activas y en el funcionamiento de los módulos adicionales.

### Requisitos
- Python 3.x
- Flask
-

 Requests

### Instalación

#### Paso 1: Instalación de las Librerías de Python
Asegúrate de tener `pip` actualizado:
```sh
pip install --upgrade pip
```

Instala las librerías necesarias:
```sh
pip install flask requests
```

### Pruebas de Replicación y Recuperación de Fallos

#### Enviar Formulario al Sistema
```sh
curl -X POST http://localhost:5004/formulario -H "Content-Type: application/json" -d '{"id": "form_1", "field1": "data", ...}'
```

#### Verificar que el Formulario está Presente en Ambas Instancias
```sh
curl http://localhost:5004/formulario/form_1
curl http://localhost:5005/formulario/form_1
```

#### Simular Caída del Nodo Líder y Promover un Nuevo Líder
```sh
curl -X POST http://localhost:5005/leader -H "Content-Type: application/json" -d '{"url": "http://localhost:5005"}'
```

#### Desconexión Temporal del Seguidor y Reconexión
- Detén una instancia seguidora y vuelve a iniciarla.
- Asegúrate de que la instancia seguidora se sincroniza con el líder al reconectarse.

### Ejecución

1. **Ejecutar instancias del Módulo de Almacenamiento en diferentes puertos:**
   ```sh
   python almacenamiento.py
   ```

2. **Configurar réplicas:**
   ```sh
   curl -X POST http://localhost:5004/add_follower -H "Content-Type: application/json" -d '{"url": "http://localhost:5005"}'
   ```

3. **Promover líder si es necesario:**
   ```sh
   curl -X POST http://localhost:5005/leader -H "Content-Type: application/json" -d '{"url": "http://localhost:5005"}'
   ```

4. **Ejecutar Módulos Adicionales:**
   - **Cola de Mensajes:**
     ```sh
     python cola_mensajes.py
     ```

   - **Validación/Deduplicación:**
     ```sh
     python validacion.py
     ```

   - **Captura de Datos:**
     ```sh
     python captura_datos.py
     ```

   - **Reportes:**
     ```sh
     python reportes.py
     ```
## Autores

- [Marjorie Alexandra Monta Portilla](https://github.com/Alexandra1751)
- [David Antonio Fernandez Quituizaca](https://github.com/Gudrum)
- [Jessye Javier Solorzano Soriano](https://github.com/jessyesolorzano)

Esperamos que esta guía sea de ayuda para entender y ejecutar correctamente el proyecto. ¡Gracias por su atención!