const fs = require('fs');
const crc = require('crc');

function crcDecode(encodedMessage) {
    // Obtener los últimos 3 bits que representan el CRC
    const crcBits = encodedMessage.slice(-3);
    const message = encodedMessage.slice(0, -3);

    // Calcular el CRC del mensaje recibido
    const crc32 = crc.crc32(message).toString(2);

    // Asegurar que el valor CRC tenga 3 bits
    return crc32.slice(-3).padStart(3, '0');
}

function crc32Encoder(message) {
    const crc32 = require('crc-32');

    // Calcular el valor CRC del mensaje
    const crcInt = crc32.str(message).toString(2);

    // Asegurar que el valor CRC tenga 3 bits
    return crcInt.slice(-3).padStart(3, '0');
}

function correctBit(message, expectedCRC) {
    // Iterar sobre cada bit del mensaje y cambiarlo para obtener un CRC coincidente
    for (let i = 0; i < message.length; i++) {
        const bitToChange = message[i];
        // Invertir el bit
        const newBit = bitToChange === '0' ? '1' : '0';
        const correctedMessage = message.slice(0, i) + newBit + message.slice(i + 1);

        // Calcular el nuevo CRC para el mensaje corregido
        const newCRC = crc32Encoder(correctedMessage);
        if (parseInt(newCRC, 2) === expectedCRC) {
            return correctedMessage;
        }
    }

    return null;
}

// Función para leer el archivo con la trama codificada
function readEncodedMessageFromFile(filePath) {
    try {
        const encodedMessage = fs.readFileSync(filePath, 'utf8').trim();
        return encodedMessage;
    } catch (error) {
        console.error('Error al leer el archivo:', error);
        return null;
    }
}

// Función principal del receptor
function main() {
    const filePath = 'respuesta.txt'; // Ruta del archivo con la trama codificada
    const encodedMessage = readEncodedMessageFromFile(filePath);

    if (encodedMessage !== null) {
        const result = crcDecode(encodedMessage);
        console.log('Resultado:');
        console.log('Tipo:', result.type);
        if (result.data !== null) {
            console.log('Trama:', result.data);
        }
    }
}

if (require.main === module) {
    main();
}
