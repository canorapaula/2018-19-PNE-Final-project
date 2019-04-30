# FINAL PROJECT BY PAULA CANORA RHODES

import http.client
import json
import http.server
import socketserver
import termcolor

PORT = 8000


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # -- printing the request line
        termcolor.cprint(self.requestline, 'green')

        termcolor.cprint(self.requestline, 'green')
        # print(self.path)
        pathlist = self.path.split('?')
        print('pathlist: ', pathlist)
        resource = pathlist[0]
        print('resource: ', resource)

        # Getting the List of species:
        HOSTNAME = "rest.ensembl.org"
        ENDPOINT = "/info/"
        ENDPOINT2 = "species?content-type=application/json"
        METHOD = "GET"

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPConnection(HOSTNAME)
        conn.request(METHOD, ENDPOINT + ENDPOINT2, None, headers)
        r1 = conn.getresponse()

        text_json = r1.read().decode("utf-8")
        conn.close()
        user = json.loads(text_json)
        variable_lspec = ''
        list_of_species = []
        for element in user['species']:
            names = element['name']
            list_of_species.append(names)
            # print(list_of_species)
            variable_lspec = variable_lspec + '<li>{}</li>'.format(names)

        # Home Link...
        if resource == '/':
            f = open("form-final.html", 'r')
            contents = f.read()

        # When choosing an option
        # When option chosen is List of Species:
        elif len(pathlist) == 1 and resource == '/listSpecies':
            contents = """<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>List of Species</title>
                      </head>
                      <body style="background-color: white;">
                        <h1>LIST OF SPECIES</h1>
                        <a href="/">Home Link</a>
                        <br><br>
                        <l>{}</l>
                      </body>
                    </html>
                    """.format(variable_lspec)
        elif len(pathlist) == 2 and resource == '/listSpecies':
            lim = pathlist[1].split('=')
            limit = lim[1]
            print('limit:', limit)
            limit = int(limit)
            limited = list_of_species[:limit]
            limit_list = ''
            for element in limited:
                limit_list = limit_list + '<li>{}</li>'.format(element)
            contents = """<!DOCTYPE html>
                                <html lang="en" dir="ltr">
                                  <head>
                                    <meta charset="utf-8">
                                    <title>List of Species</title>
                                  </head>
                                  <body style="background-color: white;">
                                    <h1>LIST OF SPECIES</h1>
                                    <a href="/">Home Link</a>
                                    <br><br>
                                    <l>{}</l>
                                  </body>
                                </html>
                                """.format(limit_list)

        # When option chosen is Karyotype:
        elif resource == '/karyotype':
            life = pathlist[1].split('=')
            specie = life[1]
            print('specie', specie)

            LINK = 'http://rest.ensembl.org/info/assembly/homo_sapiens?content-type=application/json'
            HOSTNAME = "rest.ensembl.org"
            ENDPOINT = "/info/"
            ENDPOINT2 = "assembly/"

            ENDPOINT3 = "?content-type=application/json"
            METHOD = "GET"

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT + ENDPOINT2 + specie + ENDPOINT3, None, headers)
            r1 = conn.getresponse()
            print('r1', r1.status)

            total = HOSTNAME + ENDPOINT + ENDPOINT2 + specie + ENDPOINT3
            print('total', total)
            text_json = r1.read().decode("utf-8")
            print('txtjason', text_json)
            conn.close()

            user = json.loads(text_json)
            termcolor.cprint('LINK {}'.format(HOSTNAME + ENDPOINT + ENDPOINT2 + specie + ENDPOINT3), 'green')

            karyotype = ''
            for k in user['karyotype']:
                print(k)
                karyotype = karyotype + '<li>{}</li>'.format(k)
                contents = """<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>KARYOTYPE</title>
                      </head>
                      <body style="background-color: white;">
                        <h1>Karyotype of {}</h1>
                        <l>{}</l>
                        <br>
                        <a href="/">Home Link</a>
                      </body>
                    </html>
                    """.format(specie, karyotype)

        # When option chosen is Chromosome length:
        elif resource == '/chromosomeLength':
            parametres = pathlist[1].split('&')
            print('parametres', parametres)
            spec = parametres[0].split('=')
            print('spec', spec)
            specie = spec[1]
            print('specie', specie)
            chrom = parametres[1].split('=')
            chromosome = chrom[1]
            print('chromosome', chromosome)

            LINK = 'http://rest.ensembl.org/info/assembly/homo_sapiens?content-type=application/json'
            HOSTNAME = "rest.ensembl.org"
            ENDPOINT = "/info/"
            ENDPOINT2 = "assembly/"

            ENDPOINT3 = "?content-type=application/json"
            METHOD = "GET"

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT + ENDPOINT2 + specie + ENDPOINT3, None, headers)
            r1 = conn.getresponse()
            # print('r1', r1.status)

            # total = HOSTNAME + ENDPOINT + ENDPOINT2 + specie + ENDPOINT3
            # print('total', total)
            text_json = r1.read().decode("utf-8")
            # print('txtjason', text_json)
            conn.close()

            user = json.loads(text_json)
            termcolor.cprint('LINK {}'.format(HOSTNAME + ENDPOINT + ENDPOINT2 + specie + ENDPOINT3), 'green')

            for q in user['top_level_region']:
                if chromosome == q['name']:
                    length = q['length']
                    contents = """<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>CHROMOSOME LENGTH</title>
                      </head>
                      <body style="background-color: white;">
                        <h1>Length of chromosome {} of specie {}</h1>
                        <l>The length is: {}</l>
                        <br><br>
                        <a href="/">Home Link</a>
                      </body>
                    </html>
                    """.format(chromosome, specie, length)


        # When option chosen is Human Gene Sequence:
        elif resource == '/geneSeq':

            # Get the Human Gene id
            genee = pathlist[1].split('=')
            print('genee', genee)
            gene_name = genee[1]

            LINK = 'http://rest.ensembl.org/homology/symbol/human/BRCA2?content-type=application/json'
            HOSTNAME = "rest.ensembl.org"
            ENDPOINT = "/homology/symbol/human/" + gene_name + "?content-type=application/json"
            METHOD = "GET"

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)
            r1 = conn.getresponse()
            # print('r1', r1.status)

            text_json = r1.read().decode("utf-8")
            print('txtjason', text_json)
            conn.close()

            user = json.loads(text_json)
            termcolor.cprint('LINK {}'.format(HOSTNAME + ENDPOINT), 'green')

            # Get the id for the gene sequence
            for x in user['data']:
                id = x['id']
                print('id', id)

            # Get the sequence:

            LINK = 'http://rest.ensembl.org/sequence/id/ENSG00000139618?content-type=application/json'
            HOSTNAME = "rest.ensembl.org"
            ENDPOINT = "/sequence/id/" + id + "?content-type=application/json"
            METHOD = "GET"


            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)
            r1 = conn.getresponse()
            print('r1', r1.status)

            text_json = r1.read().decode("utf-8")
            print('txtjason', text_json)
            conn.close()

            user = json.loads(text_json)
            termcolor.cprint('user {}'.format(user), 'cyan')
            termcolor.cprint('LINK {}'.format(HOSTNAME + ENDPOINT), 'green')

            sequence = user['seq']

            step = 100
            seqlist = [sequence[i:i + step] for i in range(0, len(sequence), step)]
            Sequence = ''
            for x in seqlist:
                Sequence += x + '<br>'

            contents = """<!DOCTYPE html>
                                <html lang="en" dir="ltr">
                                  <head>
                                    <meta charset="utf-8">
                                    <title>HUMAN GENE</title>
                                  </head>
                                  <body style="background-color: white;">
                                    <h1>Human Gene Sequence</h1>
                                    <l>The Sequence of the gene {} is: {}</l>
                                    <br><br>
                                    <a href="/">Home Link</a>
                                  </body>
                                </html>
                                """.format(gene_name, Sequence)


        # When option chosen is Human Gene Sequence Info:
        elif resource == '/geneInfo':
            # length = (end - start) + 1

            LINK = 'http://rest.ensembl.org/overlap/id/ENSG00000157764?feature=gene;content-type=application/json'
            HOSTNAME = "rest.ensembl.org"
            ENDPOINT = "/overlap/id/" + id + "?feature=gene;content-type=application/json"
            METHOD = "GET"

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)
            r1 = conn.getresponse()
            print('r1', r1.status)

            text_json = r1.read().decode("utf-8")
            print('txtjason', text_json)
            conn.close()

            user = json.loads(text_json)
            termcolor.cprint('user {}'.format(user), 'cyan')
            termcolor.cprint('LINK {}'.format(HOSTNAME + ENDPOINT), 'green')

            for x in user['0']:
                start = x['start']
                print('start', start)
                end = x['end']
                print('end', end)


            contents = """<!DOCTYPE html>
                                <html lang="en" dir="ltr">
                                  <head>
                                    <meta charset="utf-8">
                                    <title>HUMAN GENE INFO</title>
                                  </head>
                                  <body style="background-color: white;">
                                    <h1>Human Gene Sequence Info</h1>
                                    <l>The Info of the gene is:</l>
                                    <br><br>
                                    Start: {}
                                    <a href="/">Home Link</a>
                                  </body>
                                </html>
                                """.format(start)














        # When an error occurs...
        else:
            f = open("error.html", 'r')
            contents = f.read()

        # Generate response message with html server
        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()

        # -- Sending the body response message
        self.wfile.write(str.encode(contents))

        termcolor.cprint('Text received FINISHED', 'cyan')


socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT: {}".format(PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

print("The server is stopped.")
