import crcmod.predefined


def crc_encode(message):
    crc32 = crcmod.predefined.Crc('crc-32')
    crc_value = crc32.new(message.encode()).digest()

    # Convertir el valor CRC en un número entero
    crc_int = int.from_bytes(crc_value, byteorder='big')

    # Obtener los 3 bits menos significativos del valor CRC
    crc_bits = bin(crc_int & 0b111).replace('0b', '').zfill(3)

    encoded_message = message + crc_bits
    return encoded_message


def main():
    binary_message = input("Ingrese una trama en binario (p.ej. 110101): ")
    encoded_message = crc_encode(binary_message)

    # Guardar la respuesta en un archivo de texto
    with open("respuesta.txt", "w") as file:
        file.write(encoded_message)

    print("Mensaje codificado guardado en 'respuesta.txt'.")


if __name__ == "__main__":
    main()
