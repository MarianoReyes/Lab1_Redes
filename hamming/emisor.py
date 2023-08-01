def calcular_paridad(bits, pos):
    j = pos - 1
    longitud = len(bits)
    paridad = 0
    while j < longitud:
        for i in range(0, pos):
            if j + i < longitud:
                paridad ^= int(bits[j + i])
        j += 2 * pos
    return paridad


def hamming_codificar(datos):
    n = len(datos)
    r = 1
    while (n + r + 1) > pow(2, r):
        r += 1
    arr = ['0'] * (n + r)
    j = 0
    for i in range(1, n + r + 1):
        if i != pow(2, j):
            arr[i - 1] = datos[-1]
            datos = datos[:-1]
        else:
            j += 1
    for i in range(0, len(arr) // 2):
        arr[i] = str(calcular_paridad(arr, pow(2, i)))
    for i in range(len(arr) // 2, len(arr)):
        arr[i] = str(calcular_paridad(arr, pow(2, i - len(arr) // 2)))
    return ''.join(arr)


print("Introduzca una trama en binario: ")
datos = input()
dato = hamming_codificar(datos)
print("Mensaje codificado: ", dato)

# Guardar en un archivo de texto
with open("respuesta.txt", "w") as file:
    file.write(dato)
