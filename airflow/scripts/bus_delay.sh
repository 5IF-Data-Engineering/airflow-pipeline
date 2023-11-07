#!/bin/bash

# Assign the first parameter to a variable
host="$1"

# Assign the second parameter to a variable
port="$2"
year="$3"
city="$4"

# Run the curl command and capture the status code in a variable
response_code=$(curl -s -o /dev/null -w "%{http_code}" "$host:$port/ingestion_bus_delay/?year=$year&city=$city")
response=$(curl -s "$host:$port/ingestion_bus_delay/?year=$year&city=$city")

# Check the value of the response_code
if [ "$response_code" -eq 200 ]; then
  echo "HTTP Status Code: 200 OK"
  echo "Response: $response"
  exit 0
else
  echo "HTTP Status Code: $response_code"
  exit 1
fi
