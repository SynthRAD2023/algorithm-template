#!/usr/bin/env bash

# Set a default value for algorithm_name
algorithm_name="synthrad_algorithm"
# Check if a command-line argument is specified, and use it as the algorithm_name
if [ ! -z "$1" ]; then
    algorithm_name="$1"
fi

./build.sh

docker save synthrad_algorithm | gzip -c > "${algorithm_name}.tar.gz"