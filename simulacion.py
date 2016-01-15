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


def simula_provincia (provincia, derecha =0.0, izquierda = 0.0, confluencias =0.0):

    dic_partidos = {}

    dic_partidos["others"]=provincia["blank"]

    partidos_en_provincia = provincia["parties"]

    for partido in partidos_en_provincia:
        dic_partidos[partido["code"]]=partido["votes"]

    dic_partidos = ajusta_simulacion(dic_partidos, derecha, izquierda, confluencias)

    nseats = provincia["totalseats"]

    reparto = dhondt.dhondt(nseats,3.0,dic_partidos)

    return reparto.repre

def define_header (derecha, izquierda, confluencias, circuscripcion = 'p'):

    if circuscripcion == 'p': c='Provincial'
    if circuscripcion == 'a': c=u'Autonómica'
    if circuscripcion == 'e': c=u'Única'

    if derecha>0: td="\tEl %s%% de los votos de C's van al PP\n" %(derecha*100)
    if derecha<0: td="\tEl %s%% de los votos del PP van a C's\n" %(-derecha*100)

    if izquierda<0: ti="\tEl %s%% de los votos del PSOE van a PODEMOS\n" %(-izquierda*100)
    if izquierda>0: ti="\tEl %s%% de los votos de PODEMOS van al PSOE\n" %(izquierda*100)

    if confluencias<0: tc="\tEl %s%% de los votos de PODEMOS van a UP\n" %(-confluencias*100)
    if confluencias>0: tc="\tEl %s%% de los votos de UP van a PODEMOS\n" %(confluencias*100)


    h= u"""
SIMULACIÓN DE REPARTO DE ESCAÑOS CON TRASVASE DE VOTOS
======================================================
Parámetros
----------
Circuscripción: %s
Trasvase de votos:
%s%s%s""" %(c,td,ti,tc)

    return h

def format_result(resultado):

    res =u"Resultados\n----------\n"
    lista_ordenada= (sorted(resultado.items(), key=lambda p: p[1], reverse=True))
    for e in lista_ordenada:
        res=res + "\t%s:%s\n" %(e[0],e[1])

    return res

def format_detail(p, res, detail=0):
#    print res
#    print p
    provincia = p['province']
    seats = {}

    #quitar los partidos sin escaño
    for partido, esc in res.iteritems():
        if esc <> 0:
            seats[partido]=esc

    output=""

    if detail == 0: #ningun detalle
        pass
    if detail == 1: #partidos y escaños por provincia


        output += "\t" + provincia + " -> "
        for partido,esc in seats.iteritems():
            output += partido+": "+ str(esc) + " "
        output += "\n"

    if detail == 2: #votos, escaños, censo, abstenciones por provincia
        output = u"Circuscripción: " + provincia + "\n------------------------\n"
        output += u"\tNúmero de escaños a repartir:" + str(p['totalseats']) + "\n"
        output += "\tReparto -> "
        for partido,esc in seats.iteritems():
            output += partido+": "+ str(esc) + " "

        output += "\n\n\tCenso: %s\n\tVotos: %s\n\tBlanco: %s\n\tNulo: %s\n\tAbstenciones: %s\n" %(p['census'],p['voters'],
                                                                                     p['blank'],p['null'],
                                                                                     p['absent'])


        output += "\n\tVotos por partido\n\t-----------------\n"

        votos = ""

        for v in p["parties"]:
            votos += "\t%s : %s\n" %(v["acronym"],v["votes"])

        output += votos

        output += "\n"



    return output


def realiza_simulacion (datos_provincia, derecha=0.0, izquierda=0.0, confluencias=0.0, nivel_detalle = 0):

    resultado = {}

    header = define_header (derecha, izquierda, confluencias)

    detailed_output =""

    for p in datos_provincia:
        res = simula_provincia(p, derecha=derecha, izquierda=izquierda, confluencias=confluencias)

        for key, value in res.iteritems():
            if value == 0: continue
            if key in resultado:
                resultado[key] = resultado[key] + value
            else:
                resultado[key] = value

        detalle=format_detail(p, res, nivel_detalle)

        if detalle:
            detailed_output += detalle


        #print p["province"],res

    result = format_result (resultado)

    if detailed_output:
        detailed_output = "Detalles\n--------\n" + detailed_output

    print header
    print result
    print detailed_output



f = open('output.json', 'r')
jstring = f.read()
f.close()

votos_por_provincia = json.loads(jstring)

realiza_simulacion(votos_por_provincia, derecha=0.25, izquierda = -0.1, confluencias = -.20, nivel_detalle=1)

