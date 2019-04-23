import http.client
import json

HOSTNAME = "rest.ensembl.org"
ENDPOINT = "/info/"
ENDPOINT2 = "species?content-type=application/json"
METHOD = "GET"

headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection(HOSTNAME)

conn.request(METHOD,  ENDPOINT + ENDPOINT2, None, headers)
r1 = conn.getresponse()

text_json = r1.read().decode("utf-8")
conn.close()
user = json.loads(text_json)

for x in user['species']:
    # print('\t\t', end='')
    # termcolor.cprint(x['name'], 'grey')
    carrot = 'whaevs'

def listspecies1():
    listspecies = ''
    for x in user['species']:
        listspecies = listspecies + ',' +  x['name']

    return listspecies

listspecies1()

mes = pathlist[1]
# print('MES: ', mes)
message = mes.split('&')
print('MESSAGE:', message)












# Getting the karyotype:

elif message[0] == 'kary=on' and message[1] == 'spec_kary=':

animal = message[2].split('=')
LINK = 'http://rest.ensembl.org/info/assembly/homo_sapiens?content-type=application/json'
HOSTNAME = "rest.ensembl.org"
ENDPOINT = "/info/"
ENDPOINT2 = "assembly/"
SPECIE = animal[1]
ENDPOINT3 = "?content-type=application/json"
METHOD = "GET"

conn.request(METHOD, HOSTNAME + ENDPOINT + ENDPOINT2 + SPECIE + ENDPOINT3, None, headers)
r1 = conn.getresponse()
text_json = r1.read().decode("utf-8")
conn.close()
user = json.loads(text_json)
termcolor.cprint('LINK {}'.format(HOSTNAME + ENDPOINT + ENDPOINT2 + SPECIE + ENDPOINT3), 'green')
karyotype = ''
for k in user['karyotype']:
    karyotype = + k

contents = """<!DOCTYPE html>
        <html lang="en" dir="ltr">
          <head>
            <meta charset="utf-8">
            <title>Karyotype</title>
          </head>
          <body style="background-color: white;">
            <h1>KARYOTYPE</h1>
            <p>Here's the list of Species:</p>
            <l>{}</l>
            <a href="/">Home Link</a>
          </body>
        </html>
        """.format(karyotype)
