import socket
import random
import string
import zlib
import matplotlib.pyplot as plt
import time

# Importar las funciones del archivo emisor.py
from emisor import codificar_mensaje, calcular_integridad, aplicar_ruido, enviar_informacion


def generar_palabra_aleatoria(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def realizar_prueba(probabilidad_error, mensaje):
    mensaje_codificado = codificar_mensaje(mensaje)
    integridad = calcular_integridad(mensaje_codificado)
    trama = mensaje_codificado + integridad
    trama_con_ruido = aplicar_ruido(trama, probabilidad_error)
    enviar_informacion(trama_con_ruido)


def main():
    probabilidad_error_list = [0.01, 0.02, 0.03]
    resultados = []

    batch_size = 100  # Número de conexiones simultáneas en cada iteración
    total_iterations = 10000

    for probabilidad_error in probabilidad_error_list:
        resultados_prob = []
        for i in range(0, total_iterations, batch_size):
            batch_results = []
            for _ in range(batch_size):
                mensaje_aleatorio = generar_palabra_aleatoria(
                    random.randint(10, 30))
                realizar_prueba(probabilidad_error, mensaje_aleatorio)
                batch_results.append(len(mensaje_aleatorio))
                time.sleep(0.01)  # Retardo de 10 ms entre conexiones

            resultados_prob.extend(batch_results)

        resultados.append(resultados_prob)

    # Generar gráficas
    for i, probabilidad_error in enumerate(probabilidad_error_list):
        plt.hist(resultados[i], bins=20, alpha=0.5,
                 label=f'Probabilidad de error: {probabilidad_error}')

    plt.xlabel('Longitud del mensaje recibido')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.title('Distribución de longitudes de mensajes recibidos')
    plt.show()


if __name__ == "__main__":
    main()
