#codigo de lalo
import random

def generar_laberinto(filas, columnas, semilla=None, incluir_portales=True):
    """Genera un laberinto perfecto (sin ciclos) y ubica 3 portales aleatorios."""
    if filas < 5:
        filas = 5
    if columnas < 5:
        columnas = 5

    if semilla is not None and str(semilla).strip() != "":
        try:
            sem_int = int(semilla)
            random.seed(sem_int)
        except ValueError:
            random.seed(hash(semilla))
        semilla_usada = semilla
    else:
        semilla_usada = random.randint(1, 1000000)
        random.seed(semilla_usada)

    if filas % 2 == 0:
        filas += 1
    if columnas % 2 == 0:
        columnas += 1

    laberinto = [[1 for _ in range(columnas)] for _ in range(filas)]


   def _tallar(r, c):
        laberinto[r][c] = 0
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        dir_lista = list(direcciones)
        random.shuffle(dir_lista)

        def _iterar_dirs(idx):
            if idx >= len(dir_lista):
                return
            dr, dc = dir_lista[idx]
            nr, nc = r + dr, c + dc
            if 0 < nr < filas - 1 and 0 < nc < columnas - 1 and laberinto[nr][nc] == 1:
                laberinto[r + dr // 2][c + dc // 2] = 0
                _tallar(nr, nc)
            _iterar_dirs(idx + 1)

        _iterar_dirs(0)

    _tallar(1, 1)

    inicio = (1, 1)
    final = (filas - 2, columnas - 2)

    laberinto[inicio[0]][inicio[1]] = 'I'
    laberinto[final[0]][final[1]] = 'F'

    portales = []
    estados_portales = []  # Para registrar si sirven o no

    if incluir_portales:
        caminos_disponibles = []
        for r in range(filas):
            for c in range(columnas):
                if laberinto[r][c] == 0:
                    caminos_disponibles.append((r, c))

        random.shuffle(caminos_disponibles)

        def _colocar_portales(index):
            if index >= len(caminos_disponibles) or len(portales) >= 3:
                return
            pos_portal = caminos_disponibles[index]
            dx = random.choice([-2, -1, 1, 2])
            dy = random.choice([-2, -1, 1, 2])
            
            dest_r = pos_portal[0] + dx
            dest_c = pos_portal[1] + dy

            if pos_portal != inicio and pos_portal != final:
                laberinto[pos_portal[0]][pos_portal[1]] = 'P'
                portales.append((pos_portal, (dx, dy)))
                
                # Validar si sirve o no de inmediato para reportarlo
                if (0 <= dest_r < filas and 0 <= dest_c < columnas and laberinto[dest_r][dest_c] != 1):
                    estados_portales.append("Activo")
                else:
                    estados_portales.append("Sin efecto (Cae en pared/fuera)")

            _colocar_portales(index + 1)

        _colocar_portales(0)

    return laberinto, inicio, final, portales, estados_portales, semilla_usada
