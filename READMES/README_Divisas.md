## Funcionalidad
Esta función tiene como objetivo recopilar datos de divisas desde la API de la SBIF mediante Google Cloud Function calendarizada con Cloud Scheduled, consulta por la fecha máxima registrada y trae los registros,hasta la fecha actual.

## Proceso

1. Recibe por una petición POST:

	{"array":"`Nodo Padre`",
"divisa":"`tipo_divisa`", -> (dolar,euro,uf)
"bq_project":"`project_id`",
"bq_dataset":`bigquery_dataset`,
"bq_table":`bgquery_table`}
	
3. Obtiene la fecha máxima de la última carga en `misc.Dolar`  , `misc.Euro` y `misc.UF`
Por motivos de requerimiento de negocio los registros fueron almacenados en BigQuery.
4. Consulta datos de dolar, uf y euros a través de la api de sbif, en el intervalo de Fecha de última carga en BigQuery y Fecha Actual(GET DATE).
5. Carga en tabla de Bigquery.

## Global Configurations

### Create Cron Tab

Before create the cron tab, define the body post request for example see `dolar_body.json` and use `create_cron.sh` script

EX Usage : `bash create_cron.sh "get_uf" "0 8 * * *" "https://localization-project.cloudfunctions.net/get_divisas" "uf_body.json"`

### Set to requeriments.txt

Before to execute `create_cron.sh` and scheduler cloud function, add **google-cloud-bigquery>=1.9.0** library into the  **requirements.txt** file.

Set your api_key enviroment variable with your personal api_key in Cloud Function enviroment variables, more information in [sbif_api](https://api.sbif.cl/documentacion/index.html)


gcloud beta scheduler jobs create http get_dolar --schedule="0 8 * * *" --uri="https://localization-project.cloudfunctions.net/get_divisas"--headers="application/json" --http-method POST  --time-zone="America/Santiago" --message-body-from-file="dolar_body.json" 


