# 📚 TaskFlow API

API REST desarrollada con **Python**, **FastAPI** y **MongoDB** para la gestión segura de tareas. El proyecto implementa autenticación mediante **JWT** y **OAuth2 Password Bearer**, almacenamiento de contraseñas con **Argon2**, arquitectura modular y buenas prácticas de desarrollo backend.

Diseñada con un enfoque escalable y mantenible, la API permite administrar usuarios y tareas, aplicando validaciones de negocio, control de acceso y persistencia de datos en MongoDB.

---

## 🚀 Características

- Autenticación con JWT.
- OAuth2 Password Bearer.
- Hash seguro de contraseñas con Argon2 (`pwdlib`).
- Registro y autenticación de usuarios.
- CRUD completo de tareas.
- Validaciones de negocio.
- Endpoints protegidos.
- Estadísticas de tareas.
- Persistencia de datos con MongoDB.
- Configuración mediante variables de entorno (`.env`).
- Arquitectura modular.

---

# 🛠 Stack Tecnológico

## Backend

- Python
- FastAPI
- Pydantic
- APIRouter

## Seguridad

- JWT
- OAuth2 Password Bearer
- Argon2 (`pwdlib`)
- python-jose

## Base de Datos

- MongoDB
- PyMongo

## Herramientas

- Git
- GitHub
- Visual Studio Code
- Postman
- Thunder Client
- MongoDB Compass

---

# 📂 Estructura del Proyecto

```
TaskFlow-API/
│
├── database/
├── models/
├── routers/
├── services/
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# 📌 Funcionalidades

## Usuarios

- Registro de usuarios.
- Inicio de sesión.
- Obtención del usuario autenticado.
- Actualización de información del usuario.
- Cambio seguro de contraseña.

## Tareas

- Crear tarea.
- Obtener todas las tareas.
- Buscar tareas por distintos criterios.
- Actualizar tareas.
- Eliminar tareas.
- Validaciones de negocio.

## Estadísticas

- Total de tareas.
- Tareas completadas.
- Tareas pendientes.
- Tareas en progreso.
- Tareas de alta prioridad.
- Porcentaje de tareas completadas.

---

# 🔒 Seguridad

La API implementa un flujo de autenticación basado en estándares ampliamente utilizados:

- Contraseñas protegidas mediante **Argon2**.
- Generación de tokens **JWT**.
- Protección de endpoints con **OAuth2 Password Bearer**.
- Variables sensibles almacenadas mediante archivos **.env**.

---

# 🧩 Conceptos Aplicados

- Desarrollo de APIs REST.
- Arquitectura Modular.
- Separación por capas.
- CRUD.
- Validaciones de negocio.
- Manejo de excepciones HTTP.
- Autenticación y autorización.
- Inyección de dependencias.
- Serialización de datos.
- Variables de entorno.

---

# ▶️ Instalación

Clonar el repositorio

```bash
git clone https://github.com/ExequielDW/TaskFlow-API.git
```

Ingresar al proyecto

```bash
cd TaskFlow-API
```

Crear entorno virtual

```bash
python -m venv .venv
```

Activarlo

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Crear el archivo `.env` con las variables necesarias y ejecutar la aplicación.

```bash
uvicorn main:app --reload
```

---

# 📖 Documentación

Una vez iniciada la aplicación, la documentación interactiva estará disponible en:

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 👨‍💻 Autor

**Exequiel González**

Backend Python Developer

GitHub:
https://github.com/ExequielDW

LinkedIn:
https://www.linkedin.com/in/exequielgonzalez

---

# 📄 Licencia

Este proyecto fue desarrollado con fines educativos y de práctica profesional, aplicando buenas prácticas de desarrollo backend con Python y FastAPI.