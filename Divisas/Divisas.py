from google.cloud import bigquery
import logging
import requests
import os
import datetime

def get_divisas(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    
    logging.warn(" recibe divisa: "+request_json["divisa"])
    
    # Global Variables:
    now = datetime.datetime.now()
    
    array = request_json["array"]
    divisa = request_json["divisa"]
    bq_project = request_json["bq_project"]
    bq_dataset = request_json["bq_dataset"]
    bq_table = request_json["bq_table"]
    
    bigquery_client = bigquery.Client()
    
    # Get BD MAX DATE
    qry_max_date = ("SELECT DISTINCT MAX(Fecha) AS fecha FROM `{0}.{1}.{2}`".format(bq_project, bq_dataset, bq_table))
    qry_job = bigquery_client.query(qry_max_date)

    for row in qry_job:
        max_fecha = str(row.fecha)
    logging.warn("BQ MAX Date : "+max_fecha)
    
    # Clean
    qry_clean = ("DELETE FROM `{0}.{1}` WHERE Fecha = '{2}' AND 1=1".format(bq_dataset, bq_table, max_fecha))
    query_job = bigquery_client.query(qry_clean)  
    query_job.result() 
    
    logging.warn("Cleaned : "+max_fecha)
    
    url_api = os.environ.get("url_api")
    key = os.environ.get("key_api")
    
    # SBIF Api GET Request
    url = url_api.format(divisa, max_fecha[0:4] , max_fecha[5:7], max_fecha[8:10], str(now.year), str(now.month), str(now.day), key)
    logging.warn("url api : " +url)
    r = requests.get(url) 
    
    logging.warn("Insert2BQ")
    
    for item in r.json()[array]:
         # Insert Data  
        fecha = u"{0}".format(item["Fecha"])
        valor = item["Valor"].replace(".","").replace(",",".")
        qry_insert = ("INSERT INTO `{0}.{1}.{2}` (Fecha,Valor) VALUES ('{3}',{4})".format(bq_project, bq_dataset, bq_table,fecha,valor))
        query_job = bigquery_client.query(qry_insert)  
        query_job.result()

        logging.warn('Divisa :'+ divisa+' Fecha :' + item["Fecha"] + ' Valor :' + item["Valor"] + ' Inserted !!!')
    
    return 'OK'