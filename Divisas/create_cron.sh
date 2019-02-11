#!/bin/bash

if [ $# -ne 4 ]; then
  echo "Incorrect parameters number"
  echo'"EX: bash create_cron.sh "get_euro" "0 8 * * *" "https://region-project.cloudfunctions.net/get_divisas" "euro_body.json"'
  exit 1
fi

NAME=$1
SCHEDULE=$2
URL=$3
BODY_FILE=$4

echo "CREANDO CRON NAME : ${NAME} SCHEDULE : ${SCHEDULE} URL : ${URL} BODY_FILE : ${BODY_FILE}"

gcloud beta scheduler jobs create http ${NAME} --schedule="${SCHEDULE}" --uri="${URL}" --headers content-type="application/json" \
--http-method POST  --time-zone="America/Santiago" --message-body-from-file="${BODY_FILE}"

echo "CRON CREATED!!!"
