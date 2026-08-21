# logica.py
from datos import G

def insertar_bst(raiz, codigo):
    if raiz is None:
        return {"codigo": codigo, "izq": None, "der": None}

    # Extraemos los últimos 3 caracteres y los pasamos a entero para ordenar numéricamente
    num_actual = int(codigo[3:])
    num_raiz   = int(raiz["codigo"][3:])

    if num_actual < num_raiz:
        raiz["izq"] = insertar_bst(raiz["izq"], codigo)
    elif num_actual > num_raiz:
        raiz["der"] = insertar_bst(raiz["der"], codigo)
    else:
        # Desempate alfabético por si dos materias comparten el mismo número
        if codigo < raiz["codigo"]:
            raiz["izq"] = insertar_bst(raiz["izq"], codigo)
        elif codigo > raiz["codigo"]:
            raiz["der"] = insertar_bst(raiz["der"], codigo)
    return raiz

def buscar_bst(raiz, codigo, ruta=None):
    if ruta is None:
        ruta = []
    if raiz is None:
        return None, ruta

    ruta.append(raiz["codigo"])
    if codigo == raiz["codigo"]:
        return raiz, ruta

    num_actual = int(codigo[3:])
    num_raiz   = int(raiz["codigo"][3:])

    if num_actual < num_raiz:
        return buscar_bst(raiz["izq"], codigo, ruta)
    elif num_actual > num_raiz:
        return buscar_bst(raiz["der"], codigo, ruta)
    else:
        # Desempate alfabético para la búsqueda
        if codigo < raiz["codigo"]:
            return buscar_bst(raiz["izq"], codigo, ruta)
        else:
            return buscar_bst(raiz["der"], codigo, ruta)

def inorden_bst(raiz, resultado):
    if raiz is not None:
        inorden_bst(raiz["izq"], resultado)
        resultado.append(raiz["codigo"])
        inorden_bst(raiz["der"], resultado)

# --- CONSTRUCCIÓN GRAFO INVERTIDO (Para prerrequisitos) ---
plan = {curso: [] for curso in G.keys()}
for curso, desbloqueos in G.items():
    for desb in desbloqueos:
        if desb in plan:
            plan[desb].append(curso)
        else:
            plan[desb] = [curso]
