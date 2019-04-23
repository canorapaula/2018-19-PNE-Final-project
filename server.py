# FINAL PROJECT BY PAULA CANORA RHODES
import http.client
import json
import http.server
import socketserver
import termcolor

PORT = 8009

class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # -- printing the request line
        termcolor.cprint(self.requestline, 'green')

        termcolor.cprint(self.requestline, 'green')
        # print(self.path)
        pathlist = self.path.split('?')
        print('pathlist: ', pathlist)
        resource = pathlist[0]
        print('Resources: ', resource)

        # Getting the List of species:
        HOSTNAME = "rest.ensembl.org"
        ENDPOINT = "/info/"
        ENDPOINT2 = "species?content-type=application/json"
        METHOD = "GET"

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection(HOSTNAME)
        conn.request(METHOD, ENDPOINT + ENDPOINT2, None, headers)
        r1 = conn.getresponse()

        text_json = r1.read().decode("utf-8")
        conn.close()
        user = json.loads(text_json)
        variable_lspec = ''
        list_of_species = []
        for element in user['species']:
            Names = element['name']
            list_of_species.append(Names)
            # print(list_of_species)
            variable_lspec = variable_lspec + '<li>{}</li>'.format(Names)
        # Getting the karyotype:

        # Home Link...
        if resource == '/':
            f = open("form-final.html", 'r')
            contents = f.read()
        # When choosing an option
        # When option chosen is List of Species:
        elif resource == '/listSpecies':
            contents = """<!DOCTYPE html>
                    <html lang="en" dir="ltr">
                      <head>
                        <meta charset="utf-8">
                        <title>List of Species</title>
                      </head>
                      <body style="background-color: white;">
                        <h1>LIST OF SPECIES</h1>
                        <a href="/">Home Link</a>
                        <l>{}</l>
                      </body>
                    </html>
                    """.format(variable_lspec)

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

            conn.request(METHOD, HOSTNAME + ENDPOINT + ENDPOINT2 + specie + ENDPOINT3, None, headers)
            r1 = conn.getresponse()
            text_json = r1.read().decode("utf-8")
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
                        <title>Karyotype</title>
                      </head>
                      <body style="background-color: white;">
                        <h1>KARYOTYPE</h1>
                        <a href="/">Home Link</a>
                        <l>{}</l>
                      </body>
                    </html>
                    """.format(karyotype)
        # When option chosen is Chromosome length:
        elif resource == 'chromosomeLength':
            parametres = pathlist[1].split('&')
            print('parametres', parametres)
            spec = parametres[0].split('=')
            print('spec', spec)
            specie = spec[1]
            chrom = parametres[1].split('=')
            chromosome = chrom[1]
            print('chromosome', chromosome)

            for q in user['top_level_region']:
                q = chromosome
                print(chromosome['length'])
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
