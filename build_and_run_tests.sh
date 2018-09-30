#!/bin/sh
docker-compose --file docker-compose-tests.yml up
docker-compose --file docker-compose-tests.yml down
