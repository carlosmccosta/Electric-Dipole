from __future__ import division  #Para não truncar a divisão de inteiros
from visual import *             #Módulo com as funções gráficas do VPython
import random                    #Módulo para a geração de números aleatórios


print """
#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############
 ########**********************************************************########
  ###>>>>>>>>>>     Simulacao das interaccoes de cargas      <<<<<<<<<<<###
   ###>>>>>>>>>>          com um dipolo eletrico           <<<<<<<<<<<###
   ###>>>>>>>>>>           Fisica 2 - MIEIC - 10/11        <<<<<<<<<<<###
  ###>>>>>>>>>>        Carlos Miguel Correia da Costa       <<<<<<<<<<<###
 ########**********************************************************########
#############{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}##############


Nota: pode alterar a posicao das particulas.
As particulas verdes tem carga positiva e as vermelhas carga negativa.
"""


#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$$$$$  Configuração da janela de visualização da simulação $$$$$$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######

scene.title = "Simulacao das interaccoes de cargas com um dipolo eletrico"

scene_range = 20

scene.width = 1920
scene.height = 1080
scene.fullscreen = True
scene.autoscale = False
scene.range = (scene_range, scene_range, scene_range)
scene.center = (0,0,0)
scene.forward = (-1,-0.7,-1)


#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$$$$$               Parametrizações do programa            $$$$$$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######

dt_emf = 10
dt_part = 10
rate_simulacao = 10000
numero_planos_linhas_campo = 18     #Haverá (numero_planos_linhas_campo)^2 linhas de campo
raio_part_emf = 0.05
mag_field_range = 10 * scene_range
carga_particula = 1
massa_part_neg = 10**-17
massa_part_pos = 10**-17
carga_polo_pos = 5*10**7
pos_polo_pos = vector(0,2,0)
carga_polo_neg = -5*10**7
pos_polo_neg = vector(0,-2,0)
numero_particulas = 100             #Número de partículas que vão interagir com o campo elétrico
particulas_range = 2*scene_range
carga_min_part = -1*10**2
carga_max_part = 1*10**2
raio_max_part = 0.25


#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$$$$$                Pólos positivo e negativo             $$$$$$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######

polo_pos = sphere(pos=pos_polo_pos, radius=1, material=materials.rough, color=color.green, opacity=0.5)
polo_neg = sphere(pos=pos_polo_neg, radius=1, material=materials.rough, color=color.red, opacity=0.5)


#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$$$$$   Criação das particulas que vão interagir com o campo elétrico   $$$$$$$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######

lista_particulas = []
lista_carga_particulas = []
lista_velocidades_particulas = []
lista_trajectos_particulas = []

random.seed()
for i in range(numero_particulas):
    x = random.randint(-scene_range, scene_range)
    y = random.randint(-scene_range, scene_range)
    z = random.randint(-scene_range, scene_range)
    carga = random.randint(carga_min_part, carga_max_part)
    raio = abs((carga / carga_max_part) * raio_max_part)

    #Particulas com velocidade a apontar para perto do centro da cena (0,0,0)
    velocidade = -norm(vector(x,y,z))
    inicial_vel_offset = 10**-3
    velocidade.x *= (0.7 + random.random()*0.25) * inicial_vel_offset
    velocidade.y *= (0.7 + random.random()*0.25) * inicial_vel_offset
    velocidade.z *= (0.7 + random.random()*0.25) * inicial_vel_offset
    
    cor = color.green
    if (carga < 0):
        cor = color.red

    trajecto_particula = curve(pos=(x,y,z), color=cor)

    particula = sphere(pos=(x,y,z), radius = raio, material = materials.rough, color = cor, opacity = 0.5)
    lista_particulas.append(particula)
    lista_carga_particulas.append(carga)
    lista_velocidades_particulas.append(velocidade)
    lista_trajectos_particulas.append(trajecto_particula)

array_particulas = array(lista_particulas)
array_carga_particulas = array(lista_carga_particulas)
array_velocidades_particulas = array(lista_velocidades_particulas)
array_trajectos_particulas = array(lista_trajectos_particulas)


#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$ Função  que faz o update das linhas de campo e velocidades das partículas $$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######

def simulacao_emf():
    global pos_polo_pos
    global pos_polo_neg

    #######==================================================#######
     ##>>   Criacao do referencial dentro da esfera positiva   <<##
    #######==================================================#######

    #(sendo o vec_y_polo_pos paralelo ao vector que une os dois centros das esferas)
    #os vectores serão usados nas rotações (eixos), usados para a computação das posições das particulas que irão seguir o campo elétrico
    norm_vec_conect_center_spheres = norm(polo_pos.pos - polo_neg.pos)
    vec_norm_polo_pos = vector(norm_vec_conect_center_spheres.y, norm_vec_conect_center_spheres.x, 0)

    vec_x_polo_pos = arrow(pos=polo_pos.pos, axis=vec_norm_polo_pos, opacity=0.25, color = color.red)
    vec_y_polo_pos = arrow(pos=polo_pos.pos, axis=norm_vec_conect_center_spheres, opacity=0.25, color = color.green)
    vec_z_polo_pos = arrow(pos=polo_pos.pos, axis=cross(vec_y_polo_pos.axis, vec_x_polo_pos.axis), opacity=0.25, color = color.cyan)


    #######==================================================#######
     ##>> Criação das esferas que irão seguir o campo elétrico <<##
    #######==================================================#######

    #listas com os dados
    lista_cargas_emf = []
    lista_trajectos_emf = []

    #ângulos de rotação
    latitude = 0
    longitude = 0
    
    while (longitude < 180):
        dir_longitude = vec_x_polo_pos.axis.rotate(angle=radians(longitude), axis=vec_y_polo_pos.axis)
        latitude_axis = vec_z_polo_pos.axis.rotate(angle=radians(longitude), axis=vec_y_polo_pos.axis)

        while (latitude < 360):
            dir_particula = dir_longitude.rotate(angle=radians(latitude), axis=latitude_axis)
            pos_particula = polo_pos.pos + dir_particula

            particula = sphere(pos=pos_particula, radius=raio_part_emf, opacity=0.25)
            trajecto = curve(pos=pos_particula, color=color.yellow)

            lista_cargas_emf.append(particula)
            lista_trajectos_emf.append(trajecto)

            latitude += 360 / numero_planos_linhas_campo
        
        latitude = 0
        longitude += 360 / numero_planos_linhas_campo


    #criação de arrays a partir das listas
    array_cargas_emf = array(lista_cargas_emf)
    array_trajectos_emf = array(lista_trajectos_emf)


    continuar = True
    picked_pole = None
    
    while continuar:
        rate(rate_simulacao)

        #######===================================================#######
         ##>>       Computação das deslocações das partículas       <<##
        #######===================================================#######

        #Caso o utilizador altere a posição de um dos pólos, reconstroi as linhas de campo
        if scene.mouse.events:
            m = scene.mouse.getevent()

            if m.drag:
                if (m.pick == polo_pos or m.pick == polo_neg):
                    picked_pole = m.pick
            elif m.drop:
                if picked_pole:
                    continuar = False

                    pos_polo_pos = polo_pos.pos
                    pos_polo_neg = polo_neg.pos

                    #Limpa as cargas e linhas do campo elétrico actual
                    vec_x_polo_pos.visible = False
                    vec_y_polo_pos.visible = False
                    vec_z_polo_pos.visible = False

                    for i in range(array_cargas_emf.size):
                        array_cargas_emf[i].visible = False
                        array_trajectos_emf[i].visible = False

        if picked_pole:
            current_pos = scene.mouse.pos
            offset = current_pos - picked_pole.pos

            if (offset != 0):
                picked_pole.pos += offset



        #######===================================================#######
         ##>>        Actualização das linhas do campo elétrico      <<##
        #######===================================================#######
                    
        #Update das linhas de campo
        for i in range(array_cargas_emf.size):
            #Se as particulas se afastarem consideravelmento do centro dos polos ou quando entrarem dentro do polo neg, são imobilizadas
            if ((mag(array_cargas_emf[i].pos) < mag_field_range) and (mag(array_cargas_emf[i].pos - polo_neg.pos) > polo_neg.radius)):
                #cálculo dos dados
             
                #Fe = k |q1|*|q1| / K r^2   -> Lei de Coulomb
                #E = Fe / q
                #E = k * q1 / K r^2
                         
                dist_cargas_polo_pos = array_cargas_emf[i].pos - polo_pos.pos
                dist_cargas_polo_neg = array_cargas_emf[i].pos - polo_neg.pos
                
                Eqp = ((9*10**9 * carga_polo_pos * 1.602*10**-19) / mag(dist_cargas_polo_pos)**2) * norm(dist_cargas_polo_pos)
                Eqn = ((9*10**9 * carga_polo_neg * 1.602*10**-19) / mag(dist_cargas_polo_neg)**2) * norm(dist_cargas_polo_neg)

                E = Eqp + Eqn

                #x = x0 + v*t
                #Como se está a desenhar as linhas de campo, está-se a percorrer o espaço usando E como vector director (análogo à velocidade de uma partícula)
                pos = array_cargas_emf[i].pos + E * dt_emf

                #update dos dados
                #array_campo_mag_emf[i] = E
                array_cargas_emf[i].pos = pos
                array_trajectos_emf[i].append(pos)


        #######===========================================================================#######
         ##>>     Actualização das particulas que estão a interagir com o dipolo elétrico   <<##
        #######===========================================================================#######

        for k in range(array_particulas.size):
            #Caso a partícula saia do espaço de visualização desejado, inverte-se a direcção da sua velocidade, para voltar novamente para dentro da cena
            if (mag(array_particulas[k].pos) > particulas_range):
                array_velocidades_particulas[k] = -norm(array_particulas[k].pos) * inicial_vel_offset

            #Fe = k |q1|*|q1| / K r^2   -> Lei de Coulomb

            dist_particulas_polo_pos = array_particulas[k].pos - polo_pos.pos
            dist_particulas_polo_neg = array_particulas[k].pos - polo_neg.pos

            carga_particula = array_carga_particulas[k]
            
            Fqp = (9*10**9 * carga_particula * 1.602*10**-19 * carga_polo_pos * 1.602*10**-19) * norm(dist_particulas_polo_pos) / (mag(dist_particulas_polo_pos))**2
            Fqn = (9*10**9 * carga_particula * 1.602*10**-19 * carga_polo_neg * 1.602*10**-19) * norm(dist_particulas_polo_neg) / (mag(dist_particulas_polo_neg))**2

            Fe = Fqp + Fqn
            
            massa_particula = abs(carga_particula * massa_part_pos)
            if (carga_particula < 0):
                massa_particula = abs(carga_particula * massa_part_neg)

            if (massa_particula == 0):
                if (carga_particula < 0):
                    massa_particula = massa_part_neg
                else:
                    massa_particula = massa_part_pos

            #dv / dt = a
            #v = v0 + a*t
            #F = m * a
            V = array_velocidades_particulas[k] + (Fe / massa_particula) * dt_part

            #x = x0 + v*t
            pos = array_particulas[k].pos + V * dt_part

            #update dos dados
            array_velocidades_particulas[k] = V
            array_particulas[k].pos = pos
            array_trajectos_particulas[k].append(pos)
               


#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
 ##  $$ Reconstrução das linhas do campo elétrico sempre que há deslocação de um dos pólos $$  ##
#####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#######
                
while True:
    try:
        simulacao_emf()
    except Exception as e:
        print "Apanhada excepcao: ", e
