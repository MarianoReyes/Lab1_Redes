import crcmod.predefined


def crc_encode(message):
    # Creamos un generador de CRC-32 con el algoritmo específico
    crc32 = crcmod.predefined.Crc('crc-32')

    # Calculamos el valor CRC del mensaje
    crc_value = crc32.new(message.encode()).hexdigest()

    # Combinamos el mensaje original con el valor CRC
    encoded_message = message + crc_value

    return encoded_message


def main():
    # Paso 1: Solicitar una trama en binario
    binary_message = input("Ingrese una trama en binario (p.ej. 110101): ")

    # Paso 2: Calcular el CRC-32
    encoded_message = crc_encode(binary_message)

    # Paso 3: Devolver el mensaje en binario concatenado con el CRC-32
    print("Mensaje codificado:", encoded_message)


if __name__ == "__main__":
    main()
