def crc_simplified(data):
    polynomial = [1, 1, 0, 1]  # Polinomio generador: x^3 + x^2 + 1 (grado 3)

    # Convertir la cadena de entrada en una lista de bits
    bits = [int(bit) for bit in data]

    # Agregar tres bits de paridad al final
    for _ in range(3):
        bits.append(0)

    # Realizar el cálculo de CRC
    for i in range(len(bits) - 3):
        if bits[i] == 1:
            for j in range(4):
                bits[i + j] ^= polynomial[j]

    # Convertir los bits a una cadena binaria
    crc_result = ''.join(str(bit) for bit in bits[-3:])

    # Devolver el mensaje en binario concatenado con la información adicional (CRC)
    return data + crc_result

# Ejemplo de uso:
input_data = input("Ingresa una trama ej: 11010011101100\n>> ")
output_data = crc_simplified(input_data)

# Guardar el resultado en un archivo
with open("crc/trama_codificada.txt", "w") as file:
    file.write(output_data)

print("Mensaje original + CRC:", output_data)
print("El resultado se ha guardado en el archivo trama_codificada.txt")

