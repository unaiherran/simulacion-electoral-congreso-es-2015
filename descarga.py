#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, requests

import util

# Descarga los datos de la página oficial del ministerio del interior y los formatea en JSON


#bajar lista de provincias y escaños por circuscripcion

nombre_provincias = requests.get('http://resultadosgenerales2015.interior.es/congreso/config/ES201512-CON-ES/provincia.json')
seat_alocation = requests.get('http://resultadosgenerales2015.interior.es/congreso/assets/seats/CONGRESO.json')

prov = json.loads(nombre_provincias.text)
seat = json.loads (seat_alocation.text)


#Ir a cada página de datos de provincia, bajarlos datos y masajearlos un poco para obtener un formato de salida

# La dirección de descarga es :
# http://resultadosgenerales2015.interior.es/congreso/results/ES201512-CON-ES/ES/...
# .../COMUNIDAD/PROVINCIA/info.json

base = 'http://resultadosgenerales2015.interior.es/congreso/results/ES201512-CON-ES/ES/'

output = []

for p in prov:
    nombre = p[1]
    comunidad = p[2]
    numero_prov = p[0]

    origen = '/' + comunidad + '/' + numero_prov
    url = base + origen + '/info.json'

    dato_prov_json = requests.get(url)

    out = {}

    prov_data = json.loads(dato_prov_json.text)

    out["province"] = nombre
    out["province_number"] = numero_prov
    out["community"] = comunidad
    out["census"] = prov_data["results"]["census"]
    out["voters"] = prov_data["results"]["voters"]
    out["absent"] = prov_data["results"]["abstention"]
    out["blank"] = prov_data["results"]["blank"]
    out ["null"] = prov_data["results"]["null"]
    out ["totalseats"] = seat["2015"]["ES201512-CON-ES/ES"+origen]

    parties = []

    for p in prov_data["results"]["parties"]:
        party = {}
        party["name"] = p["name"]
        party["acronym"] = p["acronym"]
        party["code"] = util.code(p["acronym"])
        party["seats"] = p["seats"]
        party["votes"] = p["votes"]["presential"]

        parties.append(party)

    out ["parties"] = parties

    output.append(out)

#formatearlo en formato json
jstring = json.dumps(output)

#escribir un archivo con los datos
f = open('output.json', 'w')
f.write(jstring)
f.close()

