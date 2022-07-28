#!/bin/bash
./mc config host add minio ${URL} ${USER} ${PASSWORD}
./mc share download --json --expire 1h minio/${BUCKET_NAME}/${JOB_NAME} |jq '.url' | xargs wget -P /cache-jmx