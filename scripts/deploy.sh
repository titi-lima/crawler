#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

cd ../app/
~/.local/bin/pipenv requirements > requirements.txt
pip install -r requirements.txt --no-deps -t output
cd output
zip -r ../../deployment/lambda_function_payload.zip ./
cd ..
zip -g -r ../deployment/lambda_function_payload.zip ./* -x output/\*
cd ../deployment
terraform apply