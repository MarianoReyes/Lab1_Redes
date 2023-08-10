import socketio
import random


def solicitar_mensaje():
    mensaje = input("Ingrese el mensaje a enviar: ")
    return mensaje


def string_to_bits(s):
    result = ''
    for char in s:
        binary = bin(ord(char))[2:]
        result += binary.zfill(8)
    return result


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


# def enviar_informacion(trama_con_ruido):
#     HOST = 'localhost'
#     PORT = 4000
#     print("Enviando trama codificada: ", trama_con_ruido)
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.sendall(trama_con_ruido)


mensaje = solicitar_mensaje()
mensaje_codificado = string_to_bits(mensaje)
trama = hamming_codificar(mensaje_codificado)
print(trama)
trama_con_ruido = aplicar_ruido(trama)
sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('Conectado al receptor')
    sio.emit('end', trama_con_ruido)
    print('Trama enviada')
    sio.disconnect()


sio.connect('http://localhost:4000')
