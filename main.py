import matplotlib.pyplot as plt
import numpy as np 
import math
import matplotlib.animation as animation
import os.path
import imageio

def hacer_video(cant_fotos, step_frames):
    dir_name = "output"
    lista_fotos=[] #aca voy a ir guardando las fotos
    for i in range (0,cant_fotos,2):
        file_name = os.path.join(dir_name, "out{:05}.png".format(i))
        lista_fotos.append(imageio.imread(file_name))
        # print("{} de {} fotos leidas".format(i+1, cant_fotos)) #contador porque tarda un poco

    video_name = os.path.join(dir_name, "animation.mp4")
    imageio.mimsave(video_name, lista_fotos)
    # imageio.mimsave(video_name, lista_fotos, fps=20)
    print('Video Guardado')
    
def print_frame(array, array_len, dir_name, ii):
    n = int(math.sqrt(array_len))
    matrix = array.reshape(n,n)
    # figure = plt.gcf()
    # figure.set_size_inches(4, 6)
    # matrix = array.reshape(125,80) # <- para array_len=10000 solamente
    file_name = os.path.join(dir_name, "out{:05}.png".format(ii))
    plt.imshow(matrix)
    plt.savefig(file_name, dpi=600)




#VARIABLES
CANT_EJECUCIONES = 100
POBLACION = 717409
MIN_AMIGOS = 3
buscado = POBLACION - 1
SEED = None
PRINT_ANIMATION = False
STEP_FRAMES = 2

def simulacion(POBLACION, MIN_AMIGOS, buscado, SEED, PRINT_ANIMATION, STEP_FRAMES):
    np.random.seed(seed=SEED)

    personas = []
    # Seteo los valores amigos iniciales random
    for i in range(POBLACION):
        personas.append(list())
        for j in range(MIN_AMIGOS):
            while True:
                amigo_random = np.random.randint(0,POBLACION-1)
                if (amigo_random!=i and personas[i].count(amigo_random)==0):
                    break
            personas[i].append(amigo_random)

    # Corrijo la lista de amigos para que sea consistente
    for i in range(POBLACION):
        for j in range(MIN_AMIGOS):
            if i not in personas[personas[i][j]]:
                personas[personas[i][j]].append(i)

    # Obtengo el maximo de amigos
    max_amigos=0
    for i in range(POBLACION):
        if len(personas[i])>max_amigos:
            max_amigos = len(personas[i])
            
    promedio_amigos = 0
    for i in range(POBLACION):
        promedio_amigos += len(personas[i])

    promedio_amigos = promedio_amigos/POBLACION

    # print("El maximo de amigos es:", max_amigos)
    # print("El promedio de amigos es:", promedio_amigos)
    # print("\n")




    # AHORA QUE ya inicialize los grupos de amigos empiezo con la simulacion

    # Creo un nuevo arreglo de booleanos donde figurara si la persona ya fue preguntada
    preguntados = np.repeat(0 ,POBLACION)
    preguntados[0] = 1

    # Variables para la animacion:
    dir_name = "output"
    if not os.path.exists(dir_name):
            os.mkdir(dir_name)
    #lista_fotos=[] #aca voy a ir guardando las fotos
    plt.axis('off')


    #Variables para el loop
    encontrado = False
    stop = False
    raiz = 0
    amigos_preguntados = 0
    cont_frames = 0


    # ANIMACION (primer frame):
    if PRINT_ANIMATION:
        print_frame(preguntados, POBLACION, dir_name, amigos_preguntados)

    while not stop:
        # Actualizo la cantidad de amigos preguntados
        amigos_preguntados=amigos_preguntados+1
        
        # Esta el buscado en su grupo de amigos?
        if (personas[raiz].count(buscado)==1):
            encontrado = True
            stop = True
            preguntados[buscado] = 1
            break
        
        # Busco al amigo de confianza (que no este pintado)
        k = 0
        while True:
            amigo_de_confianza = personas[raiz][k]
            if (preguntados[amigo_de_confianza]==0):
                preguntados[amigo_de_confianza]=1
                raiz = amigo_de_confianza
                break
            k=k+1
            if (len(personas[raiz])==k):
                stop = True
                break
        
        #ANIMACION (frames intermedios):
        if PRINT_ANIMATION:
            cont_frames += 1
            if (cont_frames == STEP_FRAMES):
                print_frame(preguntados, POBLACION, dir_name, amigos_preguntados) 
                cont_frames = 0
        
        if (len(personas)==amigos_preguntados):
            stop = True

    if encontrado:
        preguntados[buscado] = 2

    if PRINT_ANIMATION:
        # ANIMACION (ultimo frame):
        print_frame(preguntados, POBLACION, dir_name, amigos_preguntados)
        # Rutina para hacer el video
        hacer_video(amigos_preguntados+1, STEP_FRAMES)
    return max_amigos, promedio_amigos, encontrado, amigos_preguntados


maximos_array = []
promedios_array = []
cant_veces_encontrado = 0
cant_pasos_requeridos_array = []

for i in range(CANT_EJECUCIONES):
    resultado = simulacion(POBLACION,MIN_AMIGOS,buscado,SEED,PRINT_ANIMATION,STEP_FRAMES)
    print("Ejecucion numero: ",i , flush=True)
    max_amigos = resultado[0]
    promedio_amigos = resultado[1]
    encontrado = resultado[2]
    amigos_preguntados = resultado[3]
    
    maximos_array.append(max_amigos)
    promedios_array.append(promedio_amigos)
    
    print("Se encontro al buscado?: ", encontrado)
    if encontrado:
        cant_veces_encontrado += 1
        cant_pasos_requeridos_array.append(amigos_preguntados)
        print("Cuantos amigos se requirio?: ", amigos_preguntados)
        
print("El maximo de los maximos es: ", np.amax(maximos_array))
print("El promedio de los maximos es: ", np.mean(maximos_array))
print("El promedio de los promedios es: ", np.mean(promedios_array))
print("Veces que se encontro al buscado: ", cant_veces_encontrado)
if cant_veces_encontrado>0:
    print("Promedio de pasos requeridos al encontrar al buscado: ", np.mean(cant_pasos_requeridos_array))
    