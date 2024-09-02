<div align="center">
    <br/>
    <img src=".github/readme/etsii-claro.png#gh-light-mode-only" height=100 alt="ETSII logo (claro)"/>
    <img src=".github/readme/etsii-oscuro.png#gh-dark-mode-only" height=100 alt="ETSII logo (oscuro)"/>
    <br/>
</div>

# TFG - Quantum-Proxy

Este repositorio contiene la aplicación desarrollada como TFG, una plataforma para elegir y gestionar proveedores de computación cuántica heterogéneos.

> [!NOTE] 
> Este proyecto se encuentra desplegado en la nube, accesible a través del siguiente [enlace web](https://quantum-proxy.vercel.app). Aun así, si se desea ejecutar la aplicación de forma local, se puede hacer siguiendo las instrucciones del [manual de instalación](manual-instalacion.pdf).

## Información del repositorio

Junto con el código fuente de la aplicación, este repositorio contiene toda la documentación referente al proyecto, incluyendo la [memoria](memoria.pdf) del TFG y el [manual de uso](manual-uso.pdf).

### Estructura del repositorio

**`backend/`**  
- Código fuente de la API REST desarrollada en FastAPI para manejar proveedores, sistemas, y cuentas de usuario.
- Toda la lógica de negocio junto con los módulos que conforman la aplicación.
- Modelos y configuración referente a la conexión con la base de datos MongoDB.

**`frontend/`**  
- Código fuente de la aplicación web desarrollada en Angular.
- Componentes y servicios que conforman la interfaz de usuario.
- Estilos y configuración de la aplicación.

**`docker-compose.yml`**  
- Archivo de configuración de Docker Compose para desplegar la aplicación en local.

**`manual-instalación.pdf`**
- Manual de instalación para un despliegue local.

**`manual-uso.pdf`**
- Manual de uso de la plataforma.

**`memoria.pdf`**
- Memoria del proyecto TFG.
