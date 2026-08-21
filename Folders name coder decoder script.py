import pathlib # Manejo de rutas de archivos y directorios
import shutil # Copia de directorios

# VARIABLES GLOBALES
# Lista de caracteres en orden no secuencial
lista_caracteres = ['b','0','j','R','f','H','g','9','a','1','k','S','m','2','ñ','o','3','p','q','4','r','s','t','5','u','v','w','6','x','y','z','7','A','B','C','8','D','E','F','G','I','J','K','L','M','N','O','P','Q','U','V','W','X','Y','Z','á','é','í','ó','ú','Á','É','Í','Ó','Ú','.','-',' '] # Caracteres mezclados para codificación
diccionario_valores = {} # Diccionario estático: carácter → número
diccionario_equivalencias = {} # Diccionario instancia: carácter → equivalente

# FUNCIONES
# Construye los diccionarios base
def construir_diccionarios_base():
    diccionario_valores_temp = {} # Diccionario temporal para valores
    diccionario_equivalencias_temp = {} # Diccionario temporal para equivalencias
    
    # Asignar número secuencial a cada carácter (según el orden de la lista)
    for indice_val, caracter_iter in enumerate(lista_caracteres, 1):
        diccionario_valores_temp[caracter_iter] = indice_val
    
    # Crear equivalencias: cada carácter apunta al siguiente en la lista (cíclico)
    for indice_val in range(len(lista_caracteres)):
        caracter_actual = lista_caracteres[indice_val]
        caracter_siguiente = lista_caracteres[(indice_val + 1) % len(lista_caracteres)]
        diccionario_equivalencias_temp[caracter_actual] = caracter_siguiente
    
    return diccionario_valores_temp, diccionario_equivalencias_temp

# Desplaza el diccionario de equivalencias (instancia) sumando posiciones
def desplazar_equivalencias(diccionario_equivalencias_entrada, desplazamiento_val, valor_maximo, lista_caracteres_ref):
    diccionario_nuevo = {} # Diccionario con equivalencias desplazadas
    
    # Para cada carácter, encontrar su nuevo equivalente
    for indice_val, caracter_iter in enumerate(lista_caracteres_ref):
        # Obtener el equivalente actual
        if caracter_iter in diccionario_equivalencias_entrada:
            equivalente_actual = diccionario_equivalencias_entrada[caracter_iter]
            
            # Obtener el índice del equivalente actual
            indice_equivalente = lista_caracteres_ref.index(equivalente_actual)
            
            # Desplazar el índice
            nuevo_indice = (indice_equivalente + desplazamiento_val) % valor_maximo
            
            # Asignar nuevo equivalente
            diccionario_nuevo[caracter_iter] = lista_caracteres_ref[nuevo_indice]
    
    return diccionario_nuevo

# Codifica un nombre
def codificar_nombre(nombre_entrada, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref):
    # Crear instancia del diccionario de equivalencias para este nombre
    diccionario_instancia = diccionario_equivalencias_ref.copy()
    
    valor_maximo_val = len(lista_caracteres_ref) # Número total de caracteres disponibles
    nombre_generado = [] # Lista para construir nombre resultado
    
    # Recorrer cada carácter del nombre original
    for caracter_iter in nombre_entrada:
        # Verificar si el carácter existe en el diccionario
        if caracter_iter not in diccionario_valores_ref:
            # Carácter no soportado: mantenerlo sin cambios
            nombre_generado.append(caracter_iter)
            
            continue
        
        # Buscar el carácter en el diccionario instancia para obtener su equivalente
        if caracter_iter in diccionario_instancia:
            caracter_equivalente = diccionario_instancia[caracter_iter]
        else:
            caracter_equivalente = caracter_iter
        
        # Agregar el equivalente al nombre generado
        nombre_generado.append(caracter_equivalente)
        
        # Buscar el carácter original en el diccionario estático para obtener el desplazamiento
        desplazamiento_val = diccionario_valores_ref[caracter_iter]
        
        # Desplazar la instancia del diccionario según el valor obtenido
        diccionario_instancia = desplazar_equivalencias(
            diccionario_instancia, 
            desplazamiento_val, 
            valor_maximo_val, 
            lista_caracteres_ref
        )
    
    # Eliminar la instancia del diccionario al finalizar
    del diccionario_instancia
    
    return ''.join(nombre_generado)

# Decodifica un nombre
def decodificar_nombre(nombre_entrada, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref):
    # Crear instancia del diccionario de equivalencias para este nombre
    diccionario_instancia = diccionario_equivalencias_ref.copy()
    
    valor_maximo_val = len(lista_caracteres_ref) # Número total de caracteres disponibles
    nombre_generado = [] # Lista para construir nombre resultado
    
    # Recorrer cada carácter del nombre codificado
    for caracter_iter in nombre_entrada:
        # Verificar si el carácter existe en el diccionario
        if caracter_iter not in diccionario_valores_ref:
            # Carácter no soportado: mantenerlo sin cambios
            nombre_generado.append(caracter_iter)
            
            continue
        
        # Para decodificar: buscar qué carácter en la instancia tiene como equivalente el carácter actual
        caracter_original = None
        
        for clave_val, valor_val in diccionario_instancia.items():
            if valor_val == caracter_iter:
                caracter_original = clave_val
                
                break
        
        # Si no se encontró, usar el mismo carácter
        if caracter_original is None:
            caracter_original = caracter_iter
        
        # Agregar el carácter original al nombre generado
        nombre_generado.append(caracter_original)
        
        # Buscar el carácter original en el diccionario estático para obtener el desplazamiento
        desplazamiento_val = diccionario_valores_ref[caracter_original]
        
        # Desplazar la instancia del diccionario según el valor obtenido (igual que en codificación)
        diccionario_instancia = desplazar_equivalencias(
            diccionario_instancia, 
            desplazamiento_val, 
            valor_maximo_val, 
            lista_caracteres_ref
        )
    
    # Eliminar la instancia del diccionario al finalizar
    del diccionario_instancia
    
    return ''.join(nombre_generado)

# Copia recursivamente una carpeta renombrando las carpetas en el destino
def copiar_y_renombrar(origen_actual, destino_actual, modo_operacion, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref, carpetas_procesadas):
    # Obtener el nombre codificado/decodificado de la carpeta actual
    nombre_original = origen_actual.name
    
    # Aplicar codificación o decodificación según modo
    if modo_operacion == 1:
        nombre_nuevo = codificar_nombre(nombre_original, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref)
    else:
        nombre_nuevo = decodificar_nombre(nombre_original, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref)
    
    # Crear la ruta destino con el nuevo nombre
    destino_carpeta = destino_actual / nombre_nuevo
    
    # Crear la carpeta destino
    destino_carpeta.mkdir(exist_ok = True)
    
    # Procesar todos los elementos dentro de la carpeta origen
    for elemento_iter in origen_actual.iterdir():
        if elemento_iter.is_dir():
            # Es una subcarpeta: procesar recursivamente
            copiar_y_renombrar(elemento_iter, destino_carpeta, modo_operacion, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref, carpetas_procesadas)
        else:
            # Es un archivo: copiar directamente al destino
            shutil.copy2(elemento_iter, destino_carpeta)
    
    # Marcar carpeta como procesada
    carpetas_procesadas.append(destino_carpeta)
    
    return destino_carpeta

# Procesa el directorio completo creando una nueva estructura con nombres codificados
def procesar_directorio(directorio_entrada, modo_operacion, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref):
    # Convertir a objeto Path
    ruta_origen = pathlib.Path(directorio_entrada)
    
    # Crear el directorio destino con el nombre codificado/decodificado
    nombre_raiz_original = ruta_origen.name
    
    # Aplicar codificación o decodificación a la raíz
    if modo_operacion == 1:
        nombre_raiz_nuevo = codificar_nombre(nombre_raiz_original, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref)
    else:
        nombre_raiz_nuevo = decodificar_nombre(nombre_raiz_original, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref)
    
    # Ruta destino (mismo directorio padre)
    ruta_destino = ruta_origen.parent / nombre_raiz_nuevo
    
    # Verificar si la carpeta destino ya existe
    if ruta_destino.exists():
        # Eliminar la carpeta destino existente para evitar conflictos
        shutil.rmtree(ruta_destino)
    
    # Lista para rastrear carpetas procesadas
    carpetas_procesadas = []
    
    # Copiar y renombrar recursivamente
    copiar_y_renombrar(ruta_origen, ruta_origen.parent, modo_operacion, diccionario_valores_ref, diccionario_equivalencias_ref, lista_caracteres_ref, carpetas_procesadas)
    
    return True

# PUNTO DE PARTIDA
# Construir diccionarios base al inicio
diccionario_valores, diccionario_equivalencias = construir_diccionarios_base()

# Bucle principal del programa
while True:
    # Solicitar directorio de entrada
    while True:
        directorio_entrada = input("Enter directory: ").strip('"\'')
        
        # Verificar que el directorio exista
        if not pathlib.Path(directorio_entrada).exists():
            print("Wrong directory\n")
        else:
            break
    
    # Solicitar modo de operación
    while True:
        opcion_val = input("Select option (Encode: 1 , Decode: 2): ").strip()
        
        # Validar opción ingresada
        if opcion_val in ['1', '2']:
            opcion_val = int(opcion_val)
            
            break
        else:
            print("Invalid option\n")
    
    # Crear instancias de los diccionarios para este proceso
    diccionario_valores_proceso = diccionario_valores.copy()
    diccionario_equivalencias_proceso = diccionario_equivalencias.copy()
    
    procesar_directorio(directorio_entrada, opcion_val, diccionario_valores_proceso, diccionario_equivalencias_proceso, lista_caracteres)
    
    print("Directories processed")
    print("-" * 36)
    print("")
    
    # Liberar los diccionarios del proceso
    del diccionario_valores_proceso
    del diccionario_equivalencias_proceso
