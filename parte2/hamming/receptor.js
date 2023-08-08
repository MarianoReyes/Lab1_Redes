const net = require('net')

const detectError = (arr,nr) =>{
    let n = arr.length
    let res = 0

    for(let i = 0; i < nr; i++) {
        let paridad = 0
        for(let j = 1; j <= n; j++) {
            // Verificamos los bits que deben ser verificados por este bit de paridad
            if((j & (1 << i)) === (1 << i)) {
                paridad += parseInt(arr[j-1])
            }
        }
        // Si la suma es par, la paridad es 0, si es impar es 1
        res = res << 1
        res += paridad % 2
    }

    return res
}

const obtenerParidad = (arr) => {
    let m = arr.length
    let r = 0

    // Calcular la paridad
    while(Math.pow(2, r) < m + r + 1) {
        r++
    }
    if (arr.length <=7) {
        r--
    }
    return r
}

const server = net.createServer((socket) => {
    let receivedData = ""

    socket.on('data', (data) => {
        receivedData += data.toString()
    })

    socket.on('end', () => {
        const r = obtenerParidad(receivedData)
        const errorPosition = detectError(receivedData, r)
        if(errorPosition === 0) {
            let originalData = ""
            for(let i = 0; i < receivedData.length; i++) {
                if(i !== Math.pow(2, 0) - 1 && i !== Math.pow(2, 1) - 1 && i !== Math.pow(2, 2) - 1) {
                    originalData += receivedData[i]
                }
            }
            mostrarMensaje(originalData)
        } else {
            console.log("Error is found at position: " + errorPosition)
            // Si hay un error, corregir el error
            const CorrectedBit = receivedData[errorPosition - 1] === "0" ? "1" : "0"
            const CorrectedData = receivedData.substr(0, errorPosition - 1) + CorrectedBit + receivedData.substr(errorPosition)
    
            console.log("Corrected data: " +CorrectedData)
            // Extraer los bits de datos corregidos (omitir los bits de paridad)
            let correctedData = ""
            const Lis_position_pariedad = [1,2,4,8,16,32,64,128,256,512,1024,2048]
            for(let i = 0; i < CorrectedData.length; i++) {
                if(!Lis_position_pariedad.includes(i+1)) {
                    correctedData += CorrectedData[i]
                }
            }
            console.log("Extracted data bits: " + correctedData)
        }
    })
})


function mostrarMensaje(mensaje) {
    console.log("Mensaje recibido y verificado:", mensaje)
}

server.listen(4000, 'localhost', () => {
    console.log('Receptor escuchando en el puerto 4000')
})
