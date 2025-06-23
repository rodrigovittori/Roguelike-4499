#pgzero

"""
Pack Kodland: https://kenney.nl/assets/roguelike-caves-dungeons (NO VIENE PRECORTADO)
packs de assets: https://kenney.nl/assets/series:Tiny?sort=update (LO TIENEN QUE ESCALAR)

pack escalado (drive del profe): https://drive.google.com/drive/folders/19obh4TK0RIBWlXOsaOq9uJ287jUHuLTn?usp=drive_link

> Página para redimensionar assets https://imageresizer.com/bulk-resize/

> Link del repositorio en GitHub: https://github.com/rodrigovittori/Roguelike-4499/
============================================================================================================================
Version actual: [M9.L1] - Actividad #9 (Adicional): "Nueva fila"
Objetivo: Implementar nuestro sistema de movimiento (por casillas/por turnos)

NOTA: Borrar update(dt)

PASOS:

1º) Implementar el despalzamiento entre celdas por turnos con on_key_down(key)

NOTA: Revisar restricciones
"""

# Ventana de juego hecha de celdas
celda = Actor('border') # Celda que voy a utilizar como referencia para mi mapa
""" ******************************************************************* """
paleta_terrenos = [] # Paleta de terrenos
pared = Actor("border") # 0: Pared de bloques
paleta_terrenos.append(pared) 

piso = Actor("floor")   # 1: Suelo liso (sin decoración)
paleta_terrenos.append(piso)

crack =  Actor("crack") # 2: Suelo resquebrajado/quebradizo
paleta_terrenos.append(crack)

huesos = Actor("bones") # 3: Suelo con una pilita de huesos
paleta_terrenos.append(huesos)
""" ******************************************************************* """

# NOTA: El cambio de tamaño de las actividades Nº 9 y 10 se hace aquí

cant_celdas_ancho = 7 # Ancho del mapa (en celdas)
cant_celdas_alto =  8 # Altura del mapa (en celdas)

WIDTH  = celda.width  * cant_celdas_ancho # Ancho de la ventana (en píxeles)
HEIGHT = celda.height * cant_celdas_alto  # Alto de la ventana (en píxeles)

TITLE = "Rogue-like: Mazmorra Maldita" # Título de la ventana de juego
FPS = 60 # Número de fotogramas por segundo

# Personaje:
personaje = Actor("stand", size=(50, 50))

# Nota: si quieren llevar control de la vida, pueden crear dos atributos: "salud_max" y "salud_actual"
# personaje.salud = 100
personaje.salud_max = 100
personaje.salud_act = personaje.salud_max # El PJ empieza con la vida llena

# Nota: si quieren hacer más interesante el combate pueden agregar atributos para el valor mínimo de ataque y el máximo
# (también pueden implementar un sistema de miss y critical hits) Por ejemplo ataque de 2-5 de daño y crítico 2xMAX = 10
personaje.ataque = 5

################## MAPAS ##################

mapa = [ [0, 0, 0, 0, 0, 0, 0],
         [0, 1, 2, 1, 3, 1, 0],
         [0, 1, 1, 2, 1, 1, 0],
         [0, 3, 2, 1, 1, 3, 0],
         [0, 1, 1, 1, 3, 1, 0],
         [0, 1, 3, 1, 1, 2, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [-1, -1, -1, -1, -1, -1, -1]]

mapa_2 = [ [0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 3, 1, 3, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 3, 1, 1, 1, 3, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [-1, -1, -1, -1, -1, -1, -1] ]

##########################################

mapa_actual = mapa # mapa a dibujar // cambiar valor si cambiamos de habitación

"""   #####################
     # FUNCIONES PROPIAS #
    #####################   """

def dibujar_mapa(mapa, mostrar_texto):

  for fila in range(len(mapa)):
    for columna in range(len(mapa[fila])):

      """
      Lista códigos terrenos
      
      0: pared
      1: piso (sin nada)
      2: piso (roto/resquebrajado)
      3: piso (c/ huesitos)
      """

      # https://pygame-zero.readthedocs.io/en/stable/builtins.html?highlight=anchor#positioning-actors

      """ NOTA: Yo podría multiplicar SIEMPRE por el tamaño de celda, PERO si hacemos eso,
                ¿Cómo me daría cuenta si alguna casilla me quedó mal escalada? """
      if (mapa[fila][columna] != -1):
          paleta_terrenos[mapa[fila][columna]].left =  pared.width * columna
          paleta_terrenos[mapa[fila][columna]].top  = pared.height * fila
          paleta_terrenos[mapa[fila][columna]].draw()
        
      if (mostrar_texto):
          screen.draw.text( str(mapa_actual[fila][columna]),
                            center=( ( (celda.width * columna) + int(celda.width/2) ), ( (celda.height * fila) + int(celda.height/2)) ),
                            color="black", fontsize=32 )

"""   #####################
     # FUNCIONES PG-ZERO #
    #####################   """

def draw():
    screen.fill((200,200,200))
    dibujar_mapa(mapa = mapa_actual, mostrar_texto = False)
    personaje.draw()

    # Mostramos valores personaje:
    #screen.draw.text(("❤️: " + str(personaje.salud)), midright=((WIDTH - 15), 14), color = 'white', fontsize = 16)
    screen.draw.text(("❤️: " + str(personaje.salud_act) + "/" + str(personaje.salud_max)), midright=((WIDTH - 15), 14), color = 'white', fontsize = 16)
    screen.draw.text(("🗡️: " + str(personaje.ataque)), midright=((WIDTH - 15), 36), color = 'white', fontsize = 16)

def on_key_down(key):
    if ((keyboard.right or keyboard.d) and (personaje.x < (WIDTH - celda.width * 2))):
        # ¿Xq 2?: Una (a la que me voy a desplazar) y otra (por la pared, que NO puedo atravesar)
        personaje.x += celda.width
        personaje.image = "stand" # xq stand mira a la dcha
    
    elif ((keyboard.left or keyboard.a) and (personaje.x > (celda.width * 2))):
        personaje.x -= celda.width
        personaje.image = "left" # xq mira a la izq
        
    elif ((keyboard.down or keyboard.s) and (personaje.y < HEIGHT - celda.height * 3)):
        # A partir de la próxima actividad (9) deberían ser 3 celdas: a la que me muevo, la pared y el espacio para datos
        personaje.y += celda.height
    
    elif ((keyboard.up or keyboard.w) and (personaje.y > (celda.height * 2))):
        personaje.y -= celda.height