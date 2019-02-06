from google.cloud import bigquery
import logging
import requests
import os

def get_divisas(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    '''
    https://api.sbif.cl/documentacion/Dolar.html
    '''
    bigquery_client = bigquery.Client()
    
    dataset_ref = bigquery_client.dataset('misc')
    table_ref = dataset_ref.table('Dolar')
    table = bigquery_client.get_table(table_ref)

    url_api = os.environ.get("url_api")
    key = os.environ.get("key_api")
    output_format = "json"

    url = url_api.format(key, output_format)
    r = requests.get(url)
    
    for item in r.json()["Dolares"]:
        rows_to_insert = [(u"{0}".format(item["Fecha"]), item["Valor"].replace(",","."))]
        errors = bigquery_client.insert_rows(table, rows_to_insert)
        assert errors == []
        msg='Fecha :' + item["Fecha"] + ' Valor :' + item["Valor"] + ' Inserted !!!'
        logging.warn(msg)
    return msg 