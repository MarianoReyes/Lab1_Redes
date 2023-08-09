import random
import matplotlib.pyplot as plt
import socketio


def generar_cadena(tamano):
    return ''.join([str(random.randint(0, 1)) for _ in range(tamano)])


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


def aplicar_ruido(trama, probabilidad_error):
    trama_con_ruido = ""
    for bit in trama:
        if random.random() < probabilidad_error:
            bit = "1" if bit == "0" else "0"
        trama_con_ruido += bit
    return trama_con_ruido

# Tus funciones generar_cadena, hamming_codificar, aplicar_ruido ...


sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print("Conectado al receptor")


trama_decodificada = None


@sio.on('trama_decodificada')
def on_trama_decodificada(data):
    # Aquí puedes manejar la trama decodificada
    trama_decodificada = data['trama']
    error_count = sum(1 for a, b in zip(trama, trama_decodificada) if a != b)
    error_rate = error_count / len(trama)
    resultados.append((tamano, probabilidad, error_rate))
    print("Trama decodificada:", trama_decodificada)


sio.connect('http://localhost:4000')
# ...

# Lista para almacenar los resultados
resultados = []

# Parámetros de prueba
tamanos_cadena = [100, 1000, 10000]
probabilidades_error = [0, 0.01, 0.05, 0.1]

# Bucle para ejecutar pruebas
for tamano in tamanos_cadena:
    for probabilidad in probabilidades_error:
        # Generar una cadena aleatoria
        cadena = generar_cadena(tamano)
        
        # Aplicar algoritmo de Hamming
        trama = hamming_codificar(cadena)
        trama_con_ruido = aplicar_ruido(trama, probabilidad)
        
        # Enviar trama con ruido al receptor
        sio.emit('trama_con_ruido', {'trama': trama_con_ruido})
        # esperar 2 segudnos
        sio.sleep(2)
        # Aquí puedes incluir la lógica para procesar la trama decodificada
        # trama_decodificada = trama # Esto debería ser reemplazado por la trama decodificada que recibes del servidor


# Crear gráficos con matplotlib
for probabilidad in probabilidades_error:
    x = [res[0] for res in resultados if res[1] == probabilidad]
    y = [res[2] for res in resultados if res[1] == probabilidad]
    plt.plot(x, y, label=f'Probabilidad: {probabilidad}')

plt.xlabel('Tamaño de Cadena')
plt.ylabel('Tasa de Error')
plt.legend()
plt.show()
