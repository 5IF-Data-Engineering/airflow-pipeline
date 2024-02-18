#!/bin/bash

host="$1"

port="$2"
lat="$3"
lon="$4"
start_date="$5"
end_date="$6"
city="$7"

# Run the curl command and capture the status code in a variable
response_code=$(curl -w "%{http_code}\n" -o /tmp/response.json "$host:$port/ingestion_weather/?lat=$lat&lon=$lon&start_date=$start_date&end_date=$end_date&city=$city")

# Check the value of the response_code
if [ "$response_code" -eq 200 ]; then
  echo "HTTP Status Code: 200 OK"
  echo "Response Body:"
  cat /tmp/response.json
  exit 0
else
  echo "HTTP Status Code: $response_code"
  exit 1
fi
