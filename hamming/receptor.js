
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
})

const calcularParidad = (bits, pos) =>{
    let paridad = 0 
    let j = pos - 1
    while (j < bits.length) {
        for(let i = 0; i < pos; i++) {
            if (j + i < bits.length) {
                paridad ^= parseInt(bits.charAt(j + i))
            }
        }
        j += 2 * pos
    }
    return paridad
}

const hammingDecodificar=(datos) =>{
    let n = datos.length
    let r = 0
    let error_pos = 0
    for(let i = 0; i < n; i++) {
        if (Math.pow(2, r) === (i + 1)) {
            let val = calcularParidad(datos, i + 1)
            if (val != parseInt(datos.charAt(i))) {
                error_pos += i + 1
            }
            r++
        }
    }

    let result
    if (error_pos >= 0) {
        let corrected_data = datos.split('')
        corrected_data[error_pos - 1] = corrected_data[error_pos - 1] === '0' ? '1' : '0'
        result = "Se detectó un error en la trama en la posición: " + error_pos + ". Trama corregida: " + corrected_data.join('')
    } else {
        result = "No se detectaron errores. La trama recibida es: " + datos
    }
    return result
}

readline.question("Introduzca una trama en binario: ", function(datos) {
    console.log(hammingDecodificar(datos))
    readline.close()
})