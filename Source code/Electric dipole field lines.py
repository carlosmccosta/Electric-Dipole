from __future__ import division  #Para não truncar a divisão de inteiros
from visual import *             #Módulo com as funções gráficas do VPython
from math import *

scene_range = 15

scene.width = 1920
scene.height = 1080
scene.fullscreen = True
scene.autoscale = False
scene.range = (scene_range, scene_range, scene_range)
scene.center = (0,0,0)
scene.forward = (-1,-0.7,-1)

dt = 10
rate_emf = 1000
numero_planos_linhas_campo = 24
carga_particula = 1
massa_particula = 1.673*10**-27
carga_polo_pos = 5*10**7
pos_polo_pos = vector(0,2,0)
carga_polo_neg = -5*10**7
pos_polo_neg = vector(0,-2,0)


def criacao_emf():
    #polos pos e neg
    global pos_polo_pos
    global pos_polo_neg
    polo_pos = sphere(pos=pos_polo_pos, radius=1, material = materials.marble, opacity=0.25)
    polo_neg = sphere(pos=pos_polo_neg, radius=1, material = materials.marble, opacity=0.25)
    
    #criacao do referencial dentro da esfera positiva (sendo o vec_y_polo_pos paralelo ao vector que une os dois centros das esferas)
    #os vectores serão usados nas rotações (eixos)
    norm_vec_conect_center_spheres = norm(polo_pos.pos - polo_neg.pos)
    vec_norm_polo_pos = vector(norm_vec_conect_center_spheres.y, norm_vec_conect_center_spheres.x, 0)

    vec_x_polo_pos = arrow(pos=polo_pos.pos, axis=vec_norm_polo_pos, opacity=0.25, color = color.red)
    vec_y_polo_pos = arrow(pos=polo_pos.pos, axis=norm_vec_conect_center_spheres, opacity=0.25, color = color.green)
    vec_z_polo_pos = arrow(pos=polo_pos.pos, axis=cross(vec_y_polo_pos.axis, vec_x_polo_pos.axis), opacity=0.25, color = color.cyan)

        
    #listas com os dados
    lista_particulas_emf = []
    lista_trajectos = []

    #ângulos de rotação
    latitude = 0
    longitude = 0

    #criação das particulas
    while (longitude < 180):
        dir_longitude = vec_x_polo_pos.axis.rotate(angle=radians(longitude), axis=vec_y_polo_pos.axis)
        latitude_axis = vec_z_polo_pos.axis.rotate(angle=radians(longitude), axis=vec_y_polo_pos.axis)

        while (latitude < 360):
            dir_particula = dir_longitude.rotate(angle=radians(latitude), axis=latitude_axis)
            pos_particula = polo_pos.pos + dir_particula

            particula = sphere(pos=pos_particula, radius=0.05, opacity=0.25)
            trajecto = curve(pos=pos_particula, color=color.yellow)

            lista_particulas_emf.append(particula)
            lista_trajectos.append(trajecto)

            latitude += 360 / numero_planos_linhas_campo
        
        latitude = 0
        longitude += 360 / numero_planos_linhas_campo


    #criação de arrays a partir das listas
    array_particulas_emf = array(lista_particulas_emf)
    array_trajectos = array(lista_trajectos)


    #cálculo das linhas do campo magnético
    continuar = True

    picked_pole = None

    while continuar:
        rate(rate_emf)

        #Caso o utilizador altere a posição de uma das partículas, reconstroi as linhas de campo
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

                    #Limpa os objectos e linhas de campo actuais
                    while(len(scene.objects) > 0):
                        scene.objects[0].visible = False

        if picked_pole:
            current_pos = scene.mouse.pos
            offset = current_pos - picked_pole.pos

            if (offset != 0):
                picked_pole.pos += offset



        for i in range(array_particulas_emf.size):
            #Se as particulas se afastarem consideravelmento do centro dos polos ou quando entrarem dentro do polo neg, são imobilizadas
            if ((mag(array_particulas_emf[i].pos) < scene_range) and (mag(array_particulas_emf[i].pos - polo_neg.pos) > polo_neg.radius)):
                #cálculo dos dados
             
                #Fe = k |q1|*|q1| / K r^2   -> Lei de Coulomb
                #E = Fe / q
                #E = k * q1 / K r^2
                         
                dist_particulas_pos = array_particulas_emf[i].pos - polo_pos.pos
                dist_particulas_neg = array_particulas_emf[i].pos - polo_neg.pos
                
                Eqp = ((9*10**9 * carga_polo_pos * 1.602*10**-19) / mag(dist_particulas_pos)**2) * norm(dist_particulas_pos)
                Eqn = ((9*10**9 * carga_polo_neg * 1.602*10**-19) / mag(dist_particulas_neg)**2) * norm(dist_particulas_neg)

                E = Eqp + Eqn

                #x = x0 + v*t
                #Como se está a desenhar as linhas de campo, está-se a percorrer o espaço usando E como vector director (análogo à velocidade de uma partícula)
                pos = array_particulas_emf[i].pos + E * dt

                #update dos dados
                #array_campo_mag_emf[i] = E
                array_particulas_emf[i].pos = pos
                array_trajectos[i].append(pos)
               



while True:
    criacao_emf()
