# datos.py

# Grafo de la carrera (prerequisitos → desbloqueos)
G = {
    'EIF200': ['EIF201', 'EIF202', 'EIF203'],
    'MAT030': ['EIF201', 'MAT002', 'EIF203'],
    'LIX410': ['LIX411'],
    'EIF201': ['EIF204', 'EIF205', 'EIF404'],
    'MAT002': ['MAT005', 'MAT006', 'EIF206'],
    'LIX411': ['LIX412'],
    'EIF202': ['EIF205'],
    'EIF203': ['EIF207', 'MAT006'],
    'EIF204': ['EIF206', 'EIF207'],
    'MAT005': [],
    'LIX412': [],
    'EIF205': [], 'EIF206': [], 'EIF207': [],
    'EIF404': [], 'MAT006': [],
}

# Nombre oficial de cada asignatura
NOMBRES = {
    'EIF200': 'Fundamentos de Informática',
    'MAT030': 'Matemática para Informática',
    'LIX410': 'Inglés Integrado I',
    'EIF201': 'Programación I',
    'MAT002': 'Cálculo I',
    'LIX411': 'Inglés Integrado II',
    'EIF202': 'Soporte Técnico',
    'EIF203': 'Estructuras Discretas para Informática',
    'EIF204': 'Programación II',
    'MAT005': 'Álgebra Lineal',
    'LIX412': 'Inglés Integrado III',
    'EIF205': 'Arquitectura de Computadoras',
    'EIF206': 'Programación III',
    'EIF207': 'Estructuras de Datos',
    'EIF404': 'La Organización y su Entorno',
    'MAT006': 'Probabilidad y Estadística para Informática',
}
