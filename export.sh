#!/usr/bin/env bash

./build.sh

docker save synthrad_algorithm | gzip -c > synthrad_algorithm.tar.gz
