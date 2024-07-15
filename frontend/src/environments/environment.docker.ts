export const environment = {
    production: false,
    // Como el código se ejecuta en el navegador, el contenedor con el backend no es visible
    // puesto que no se resuelve el nombre "backend", debería añadirse a la tabla de resolución de nombres
    // Solución sencilla: vincular el puerto 8000 del host al 80 del contenedor del backend
    apiUrl: 'http://localhost:8000'
};