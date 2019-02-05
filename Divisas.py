from google.cloud import bigquery
import logging
import requests


def get_divisas(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    '''
    https://api.sbif.cl/documentacion/Dolar.html

    '''
    if started == 'begin':
        bigquery_client = bigquery.Client()
        # Get Dolar Price
        dataset_ref = bigquery_client.dataset('misc')
        table_ref = dataset_ref.table('Dolar')
        table = bigquery_client.get_table(table_ref)

        url_api = os.environ.get("url_api")
        key = os.environ.get("key_api")
        output_format = "json"

        url = url.api.format(url_api, output_format)

        r = requests.get(url)
        for item in r.json()["Dolares"]:
            rows_to_insert = [(item["Fecha"], item["Valor"])]
            bigquery_client.insert_rows(table, rows_to_insert)

            logging.warn('Fecha :' + item["Fecha"] + ' Valor :' + item["Valor"] + ' Inserted !!!')

