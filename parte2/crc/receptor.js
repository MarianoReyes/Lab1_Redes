const net = require('net');
const zlib = require('zlib');
const crc32 = require('crc').crc32;

const server = net.createServer((socket) => {
    let receivedData = "";

    socket.on('data', (data) => {
        receivedData += data.toString();
    });

    socket.on('end', () => {
        const [mensajeBinario, integridad] = obtenerMensajeEIntegridad(receivedData);
        const crc32_calculado = calcularCRC32(mensajeBinario);
        if (crc32_calculado === integridad) {
            const mensajeDecodificado = decodificarMensaje(mensajeBinario);
            mostrarMensaje(mensajeDecodificado);
        } else {
            console.log("Error de integridad/ruido detectado en la trama recibida.");
        }
    });
});

function obtenerMensajeEIntegridad(trama) {
    // La trama contiene el mensaje codificado + integridad
    const mensajeBinario = trama.substring(0, trama.length - 32);
    const integridad = trama.substring(trama.length - 32);
    return [mensajeBinario, integridad];
}

function calcularCRC32(mensaje) {
    const buffer = Buffer.from(mensaje, 'binary');
    const crc32Value = crc32(buffer).toString(2).padStart(32, '0');
    return crc32Value;
}

function decodificarMensaje(mensajeBinario) {
    let mensajeDecodificado = "";
    for (let i = 0; i < mensajeBinario.length; i += 8) {
        const byte = mensajeBinario.substr(i, 8);
        const asciiCode = parseInt(byte, 2);
        const char = String.fromCharCode(asciiCode);
        mensajeDecodificado += char;
    }
    return mensajeDecodificado;
}

function mostrarMensaje(mensaje) {
    console.log("Mensaje recibido y verificado:", mensaje);
}

server.listen(8081, 'localhost', () => {
    console.log('Receptor escuchando en el puerto 8081');
});
