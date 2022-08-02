#!/bin/bash
./mc config host add minio ${URL} ${USER} ${PASSWORD}
./mc share download --json --expire 1h minio/${BUCKET_NAME}/${TASK_NAME} |jq '.url' | xargs wget -P /cache-jmx