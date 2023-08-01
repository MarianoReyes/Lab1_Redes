import crcmod.predefined


def crc_encode(message):
    # Creamos un generador de CRC-32 con el polinomio estándar (0x04C11DB7)
    crc32 = crcmod.predefined.Crc('crc-32')
    crc_value = crc32.new(message.encode()).hexdigest()
    encoded_message = message + crc_value
    return encoded_message


def main():
    binary_message = input("Ingrese una trama en binario (p.ej. 110101): ")
    encoded_message = crc_encode(binary_message)

    # Separar la trama original y el valor CRC-32
    original_message = encoded_message[:-8]
    crc_value = encoded_message[-8:]

    # Guardar solo la trama modificada en un archivo de texto
    with open("trama_modificada.txt", "w") as file:
        file.write("Trama modificada: " + encoded_message + "\n")
        file.write("Trama original: " + original_message + "\n")
        file.write("Valor CRC-32: " + crc_value + "\n")

    print("Trama modificada guardada en 'trama_modificada.txt'.")


if __name__ == "__main__":
    main()
