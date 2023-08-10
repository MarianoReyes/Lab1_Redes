import socket
import random
import zlib


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


def calcular_integridad(mensaje_binario):
    crc32 = zlib.crc32(mensaje_binario.encode()) & 0xFFFFFFFF
    crc32_binary = bin(crc32)[2:].zfill(32)
    return crc32_binary


def aplicar_ruido(trama, probabilidad):
    trama_con_ruido = ""
    for bit in trama:
        if random.random() < probabilidad:  # Probabilidad de error del 1%
            bit = "1" if bit == "0" else "0"
        trama_con_ruido += bit
    return trama_con_ruido


def enviar_informacion(trama_con_ruido):
    HOST = 'localhost'
    PORT = 8081

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(trama_con_ruido.encode())


mensaje = solicitar_mensaje()
mensaje_codificado = codificar_mensaje(mensaje)
integridad = calcular_integridad(mensaje_codificado)
trama = mensaje_codificado + integridad
trama_con_ruido = aplicar_ruido(trama, 0.01)
enviar_informacion(trama)
