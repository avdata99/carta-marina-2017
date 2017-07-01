#!/usr/bin/env python3
import sys
import csv

path='carta-marina-cordoba-2017.txt'

f = open(path, 'r')
raw=f.read()

""" 
archivo extraido con pdftotext ya que el PDF esta mal armado y Tabula 
  no ve que haya tablas armadas correctamente) 
"""

lines = raw.split('\n')

# valores actuales que cambian cada x escuelas
seccion_nro = 0
seccion_name = ''
circuito_nro = '' # NO ES NUMERICO
circuito_name=''

imin = '' # en que estoy
cnt = 0
errores=0

escuelas = [] # resultados finales
secciones = {} # secciones electorales (una por departamentpos de Córdoba)
circuitos = {} # subdivision de las secciones, en la práctica es una por cada municpio, salvo la Capital

last_mesa= 0 # controlar que todos los numeros de mesa esten incluidos

for r in lines:
    cnt += 1
    
    if r.find('                      Página') > -1:
        print('NO - PAGE')
        continue

    if r.strip() == 'DISTRITO CORDOBA' or r.startswith(''):
        print('NO - DIST')
        continue

    if r.find('              ELECCIONES 2017') > -1:
        print('NO - ELEC')
        continue

    if r.find('      Informe de Establecimientos') > -1:
        print('NO - INFO')
        continue
        
    if r.find('Sección ') == 0: # es la seccion
        p = r.replace('Sección ', '').strip().split('-')
        seccion_nro = int(p[0].strip())
        seccion_name = p[1].strip()
        print("Empezando seccion %d %s" % (seccion_nro, seccion_name))
        prev_line = r
        imin = ''
        continue

    if r.find(' Circuito') == 0: # es la seccion
        p = r.replace(' Circuito', '').strip().split('-')
        circuito_nro = p[0].strip()
        p2 = p[1].split('       ') # en la misma linea hay titulos de otros campos mas abajo
        circuito_name = p2[0].strip()
        print("Empezando circuito %s %s" % (circuito_nro, circuito_name))
        prev_line = r
        imin = 'escuelas' # marco que estoy en las escuelas
        continue

    if r.find('Resúmen del Circuito') == 0:
        imin = ''
        continue
    
    if imin == 'escuelas':
        if r == '':
            continue

        p = r.split('    ')
        p2 = [x for x in p if x.strip() != ''] # tomar solo los datos reales
        if len(p2) < 4:
            print('linea muy corta {}'.format(r))
            continue
        # print('ESCUELA PELADA: {}'.format(r))
        escuela = p2[0]
        p3 = escuela.split(' - ')
        direccion = ''
        barrio = ''
        if len(p3) == 2:
            escuela = p3[0]
            direccion = p3[1]
        elif len(p3) == 3:
            escuela = p3[0]
            direccion = p3[1]
            barrio = p3[2]
        elif len(p3) > 3:
            print('Linea {} no comprendida, corregir: {}'.format(cnt, r))
            sys.exit(1)
        
        if not p2[1].strip().isnumeric(): # viene el barrio algunas veces
            escuela = '{} - {}'.format(p2[0], p2[1])
            del p2[1]

        cant_mesas = int(p2[1])
        mesa_desde = int(p2[2].split(' a ')[0])
        # LA MESA 6000 esta cambiada de lugar (?)
        if mesa_desde == 6000:
            mesa_desde = 6339
        if mesa_desde != 6001 and mesa_desde != last_mesa + 1:
            print("Mesa invalida %d %d" % (mesa_desde, last_mesa))
            sys.exit(1)
        mesa_hasta = int(p2[2].split(' a ')[1])
        last_mesa = mesa_hasta
        cant_electores = int(p2[3].replace('.', ''))
        # print("Escuela %s. %d mesas. Desde %d a %d. %d electores" % (escuela, cant_mesas, mesa_desde, mesa_hasta, cant_electores))
        elem = {'seccion_nro': seccion_nro,
                'seccion_name': seccion_name,
                'circuito_nro': circuito_nro,
                'circuito_name': circuito_name,
                'escuela': escuela.replace(',', '.'),
                'direccion': direccion,
                'barrio': barrio,
                'cant_mesas': cant_mesas,
                'desde': mesa_desde, 'hasta': mesa_hasta,
                'electores': cant_electores}
        # print(elem)
        escuelas.append(elem)
        
print("Escuelas: %d" % len(escuelas))


with open('escuelas-elecciones-2017-cordoba.csv', 'w') as csvfile:
    fieldnames = ['escuela', 'direccion', 'barrio', 'seccion_nro', 'seccion_name', 'circuito_nro',
                    'circuito_name', 'cant_mesas', 'desde', 'hasta',
                    'electores']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in escuelas:
        writer.writerow(data)


print("END")
