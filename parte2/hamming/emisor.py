import socket
import random


def solicitar_mensaje():
    mensaje = input("Ingrese el mensaje a enviar: ")
    return mensaje


def codificar_mensaje(mensaje):
    mensaje_codificado = ""
    for char in mensaje:
        ascii_code = ord(char)
        binary_code = bin(ascii_code)[2:].zfill(8)
        mensaje_codificado += binary_code
    return mensaje_codificado


def hamming_codificar(datos):
    n = len(datos)
    r = 1
    while (n + r + 1) > pow(2, r):
        r += 1
    arr = ['0'] * (n + r)
    # print("DATA: ", n, " PARIDAD: ", r, " TOTAL: ", n + r)
    # print("ARRAY", arr)

    j = 0
    k = 1
    for i in range(0, n + r):
        if i == (pow(2, j) - 1):
            arr[i] = 'P'
            j += 1
        else:
            arr[i] = datos[k - 1]
            k += 1
    # print("ARRAY", arr)
    # Calcular los bits de paridad
    for i in range(0, r):
        paridad = 0
        for j in range(0, n + r):
            if arr[j] == 'P':
                continue
            elif (j + 1) & (1 << i):
                if arr[j] == '1':
                    paridad = paridad ^ 1
        for paridades in range(r):
            if paridad == paridades + 1:
                arr[pow(2, i) - 1] = '1'
                break
            else:
                arr[pow(2, i) - 1] = '0'
    # print("ARRAY", arr)
    return ''.join(arr)


def aplicar_ruido(trama):
    trama_con_ruido = ""
    for bit in trama:
        if random.random() < 0.01:  # Probabilidad de error del 1%
            bit = "1" if bit == "0" else "0"
        trama_con_ruido += bit
    return trama_con_ruido


def enviar_informacion(trama_con_ruido):
    HOST = 'localhost'
    PORT = 8080
    print("Enviando trama codificada: ", trama_con_ruido)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(trama_con_ruido.encode())


mensaje = solicitar_mensaje()
mensaje_codificado = codificar_mensaje(mensaje)
print(mensaje_codificado)
trama = hamming_codificar(mensaje_codificado)
trama_con_ruido = aplicar_ruido(trama)
enviar_informacion(trama_con_ruido)
