

# Palabras reservadas de Python
palabras_reservadas = [
    'False', 'class', 'finally', 'is', 'return', 'None', 'continue', 'for', 'lambda',
    'try', 'True', 'def', 'from', 'nonlocal', 'while', 'and', 'del', 'global', 'not',
    'with', 'as', 'elif', 'if', 'or', 'yield', 'assert', 'else', 'import', 'pass',
    'break', 'except', 'in', 'raise'
]

# Operadores y símbolos
simbolos = {
    '(': 'tk_par_izq', ')': 'tk_par_der', '{': 'tk_llave_izq', '}': 'tk_llave_der',
    '=': 'tk_asig', '+': 'tk_suma', '-': 'tk_resta', '*': 'tk_mult', '/': 'tk_div',
    '.': 'tk_punto', ':': 'tk_dos_puntos', '!=': 'tk_distinto', '==': 'tk_igual'
}


# Función para verificar si un string representa un número entero
def es_entero(cadena):
    for char in cadena:
        if not char.isdigit():
            return False
    return True


# Función para verificar si un string es un identificador o palabra reservada
def es_identificador(lexema):
    if lexema[0].isalpha() or lexema[0] == '_':
        for char in lexema[1:]:
            if not (char.isalnum() or char == '_'):
                return False
        return True
    return False


# Función para analizar una línea de código y generar tokens
def analizar_linea(linea, numero_linea):
    tokens_encontrados = []
    posicion = 0

    while posicion < len(linea):
        char = linea[posicion]

        if char.isspace():  # Ignorar espacios
            posicion += 1
            continue

        # Verificar si es un comentario
        if char == '#':
            comentario = linea[posicion:]
            tokens_encontrados.append(f"<tk_comentario,{comentario.strip()},{numero_linea},{posicion + 1}>")
            break  # Salir del ciclo, ya que el resto de la línea es un comentario

        # Verificar si es una cadena de texto
        if char == '"' or char == "'":
            inicio = posicion
            posicion += 1
            while posicion < len(linea) and linea[posicion] != char:
                posicion += 1
            if posicion < len(linea):  # Encontró el final de la cadena
                posicion += 1
                tokens_encontrados.append(f"<tk_cadena,{linea[inicio:posicion]},{numero_linea},{inicio + 1}>")
            else:
                print(f">>> Error léxico(linea:{numero_linea},posicion:{inicio + 1})")
                return tokens_encontrados  # Devolver tokens antes del error

        # Verificar si es un número
        elif char.isdigit():
            inicio = posicion
            while posicion < len(linea) and linea[posicion].isdigit():
                posicion += 1
            tokens_encontrados.append(f"<tk_entero,{linea[inicio:posicion]},{numero_linea},{inicio + 1}>")

        # Verificar si es un símbolo
        elif char in simbolos:
            tokens_encontrados.append(f"<{simbolos[char]},{numero_linea},{posicion + 1}>")
            posicion += 1

        # Verificar si es un identificador o palabra reservada
        elif char.isalpha() or char == '_':
            inicio = posicion
            while posicion < len(linea) and (linea[posicion].isalnum() or linea[posicion] == '_'):
                posicion += 1
            lexema = linea[inicio:posicion]
            if lexema in palabras_reservadas:
                tokens_encontrados.append(f"<{lexema},{numero_linea},{inicio + 1}>")
            else:
                tokens_encontrados.append(f"<id,{lexema},{numero_linea},{inicio + 1}>")

        # Si no es ninguno de los anteriores, error léxico
        else:
            print(f">>> Error léxico(linea:{numero_linea},posicion:{posicion + 1})")
            return tokens_encontrados  # Devolver tokens antes del error

    return tokens_encontrados


# Función principal para leer el archivo de entrada y generar el archivo de salida
def analizar_archivo(entrada, salida):
    try:
        with open(entrada, 'r') as archivo:
            lineas = archivo.readlines()

        with open(salida, 'w') as archivo_salida:
            for i, linea in enumerate(lineas):
                tokens = analizar_linea(linea, i + 1)
                for token in tokens:
                    archivo_salida.write(token + '\n')

        print(f"Análisis léxico completado. Revisa el archivo de salida: {salida}")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {entrada}")


# Ejemplo de cómo ejecutar el programa
if __name__ == "__main__":
    archivo_entrada = 'ejemplo_prueba_1.txt'  # Nombre del archivo de entrada
    archivo_salida = 'salida.txt'  # Nombre del archivo de salida
    analizar_archivo(archivo_entrada, archivo_salida)
