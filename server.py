# Creating a server for the html files with forms, using form1.html and form2.html
import http.client
import json
import http.server
import socketserver
import termcolor

PORT = 8009

# Objects inherit properties from BaseHTTPRequestHandler


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # -- printing the request line
        termcolor.cprint(self.requestline, 'green')

        f = open("form-final.html", 'r')
        contents = f.read()


        termcolor.cprint(self.requestline, 'green')
        print(self.path)
        pathlist = self.path.split('?')
        print(pathlist)
        resource = pathlist[1]
        print('resource', resource)
        parametres = resource.split('&')
        print('parametres', parametres)
        if parametres[0] == 'l_spec=on':
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

            for x in user['species']:
                print('\t\t', end='')
                print(x['name'])

        if resource == "/":
            file = open('form-final.html', 'r')
            contents = file.read()
        elif resource == "/echo":
            params = pathlist[1]
            user_message = params.split("=")
            message = user_message[1]
            contents = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>     
                        <meta charset="UTF-8">     
                        <title>Echo server</title>     
                    </head>     
                    <body>     
                    <h1>Echo of the received message</h1>     
                    <p>{}<p>                                  
                    <a href="/">Home Page</a>     
                    </body>     
                    </html>""".format(message)
        else:
            file = open('error.html', 'r')
            contents = file.read()



        # Generate response message with html server
        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))
        self.end_headers()

        # -- Sending the body response message
        self.wfile.write(str.encode(contents))

        print()
        termcolor.cprint('Text received', 'cyan')
        mes_dict = self.requestline.split('msg=')
        mes_dict_1 = mes_dict[1].split('&')
        mes_dict_2 = mes_dict_1[0].split('+')
        print(mes_dict_2[0])

        termcolor.cprint('Text received FINISHED', 'cyan')


# -- Main Program
# The "" with nothing in them means use the local IP adress
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT: {}".format(PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

print("The server is stopped.")
