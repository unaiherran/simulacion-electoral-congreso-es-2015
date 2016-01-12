#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dhondt, json

def ajusta_simulacion (dic, derecha, izquierda, confluencias):

    if derecha:
        if derecha > 0:
            cambio_votos = int(dic["C's"] * derecha)
            dic["C's"] = dic["C's"] - cambio_votos
            dic['PP'] = dic ['PP'] + cambio_votos
        if derecha < 0:
            cambio_votos = int(dic["PP"] * derecha)
            dic["C's"] = dic["C's"] + cambio_votos
            dic['PP'] = dic ['PP'] - cambio_votos
    if izquierda:
        if izquierda > 0:
            cambio_votos = int(dic["PODEMOS"] * izquierda)
            dic["PODEMOS"] = dic["PODEMOS"] - cambio_votos
            dic['PSOE'] = dic ['PSOE'] + cambio_votos
        if izquierda < 0:
            cambio_votos = int(dic["PSOE"] * derecha)
            dic["PODEMOS"] = dic["PODEMOS"] + cambio_votos
            dic['PSOE'] = dic ['PSOE'] - cambio_votos
    if confluencias:
        if "UP" in dic:
            if confluencias > 0:
                cambio_votos = int(dic["UP"] * confluencias)
                dic["UP"] = dic["UP"] - cambio_votos
                dic['PODEMOS'] = dic ['PODEMOS'] + cambio_votos
            if confluencias < 0:
                cambio_votos = int(dic["PODEMOS"] * confluencias)
                dic["UP"] = dic["UP"] + cambio_votos
                dic['PODEMOS'] = dic ['PODEMOS'] - cambio_votos

    return dic


def simula_provincia (provincia, derecha =0, izquierda = 0, confluencias =0):

    dic_partidos = {}

    dic_partidos["others"]=provincia["blank"]

    partidos_en_provincia = provincia["parties"]

    for partido in partidos_en_provincia:
        dic_partidos[partido["code"]]=partido["votes"]

    dic_partidos = ajusta_simulacion(dic_partidos, derecha, izquierda, confluencias)

    nseats = provincia["totalseats"]

    reparto = dhondt.dhondt(nseats,3.0,dic_partidos)

    return reparto.repre


f = open('output.json', 'r')
jstring = f.read()
f.close()

provincia = json.loads(jstring)

resultado = {}

for p in provincia:
    res = simula_provincia(p, derecha=1, izquierda=0, confluencias=1)

    print res

    for key, value in res.iteritems():
        if value == 0: continue
        if key in resultado:
            resultado[key] = resultado[key] + value
        else:
            resultado[key] = value

    print p["province"],res

print resultado
