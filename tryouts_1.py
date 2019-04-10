
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
