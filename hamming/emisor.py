
def hamming_codificar(datos):
    n = len(datos)
    r = 1
    while (n + r + 1) > pow(2, r):
        r += 1
    arr = ['0'] * (n + r)
    print("DATA: ", n, " PARIDAD: ", r, " TOTAL: ", n + r)
    print("ARRAY", arr)

    j = 0
    k = 1
    for i in range(0, n + r):
        if i == (pow(2, j) - 1):
            arr[i] = 'P'
            j += 1
        else:
            arr[i] = datos[k - 1]
            k += 1
    print("ARRAY", arr)
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
    print("ARRAY", arr)
    return ''.join(arr)


print("Introduzca una trama en binario: ")
datos = input()
dato = hamming_codificar(datos)
print("Mensaje codificado: ", dato)

# Guardar en un archivo de texto
with open("respuesta.txt", "w") as file:
    file.write(dato)
