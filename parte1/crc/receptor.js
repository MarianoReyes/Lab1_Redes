const fs = require('fs');

function readInputMessageFromFile(filePath) {
  try {
    const inputMessage = fs.readFileSync(filePath, 'utf8');
    return inputMessage.trim(); // Eliminar espacios en blanco al principio o al final, si los hay
  } catch (error) {
    console.error("Error al leer el archivo:", error);
    return null;
  }
}

function crc_simplified(data) {
    const polynomial = [1, 1, 0, 1]; // Polinomio generador: x^3 + x^2 + 1 (grado 3)
  
    // Convertir la cadena de entrada en un array de bits
    const bits = data.split('').map(bit => parseInt(bit));
  
    // Realizar el cálculo de CRC
    for (let i = 0; i < bits.length - 3; i++) {
      if (bits[i] === 1) {
        for (let j = 0; j < 4; j++) {
          bits[i + j] ^= polynomial[j];
        }
      }
    }
  
    // Verificar si se detectaron errores
    const crc_result = bits.slice(-3);
    const errorsDetected = crc_result.some(bit => bit === 1);
  
    if (!errorsDetected) {
      // Caso: No se detectaron errores
      return { valid: true, message: data };
    } else {
      // Caso: Se detectaron errores
      // Descartar la trama
      return { valid: false, message: "Trama descartada por detectar errores." };
    }
  }
  
  function decodeMessage(encodedMessage) {
    const data = encodedMessage.slice(0, -3); // Eliminar los 3 bits de paridad del final
    const crc = encodedMessage.slice(-3); // Obtener los 3 bits de paridad del final
  
    const result = crc_simplified(encodedMessage);
  
    if (result.valid) {
      // Caso: No se detectaron errores
      return `Trama recibida: ${data}`;
    } else {
      // Caso: Se detectaron errores
      // Intentar corregir errores invirtiendo el bit que está en la posición de los bits de paridad (crc)
      const errorPosition = encodedMessage.length - 3;
      if (errorPosition >= 0 && errorPosition < encodedMessage.length) {
        const correctedMessage = encodedMessage.slice(0, errorPosition) + (1 - parseInt(encodedMessage[errorPosition])) + encodedMessage.slice(errorPosition + 1);
  
        // Calcular el nuevo CRC del mensaje corregido
        const correctedResult = crc_simplified(correctedMessage);
        if (correctedResult.valid) {
          return `Trama corregida: ${correctedMessage}`;
        } else {
          return `Trama descartada por detectar errores.`;
        }
      } else {
        return result.message; // Si la posición de error está fuera del rango, simplemente se descarta la trama.
      }
    }
  }
  
  
  
 // Obtener el mensaje desde el archivo
const filePath = 'crc/trama_codificada.txt';
const inputMessageFromFile = readInputMessageFromFile(filePath);

if (inputMessageFromFile) {
  // Decodificar el mensaje
  const decodedResult = decodeMessage(inputMessageFromFile);
  console.log(decodedResult);
}