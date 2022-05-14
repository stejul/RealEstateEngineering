TODO
- implement correct marquez.yml configuration
  - didn't work because credentials were wrong for marquez-db

`docker system prune --all && docker-compose -f docker-compose.yml -f docker-compose.seed.yml up -V --force-recreate --remove-orphans`
Sites to scrape:
* [LaendleImmo](https://www.laendleimmo.at/)
* [ImmobilienScout](https://www.immobilienscout24.at/)
* [ImmoWelt](https://immowelt.at)
* [Immobilien](https://immobilien.net)

scripts to run:

`docker-compose up -f docker-compose.yml -f docker-compose.airflow.yml up --build --force-recreate --remove-orphans`

seed marquez db
`docker-compose up -f docker-compose.yml -f docker-compose.seed.yml -f docker-compose.airflow.yml up --build --force-recreate --remove-orphans`

- localhost:3000 -> marquez
- localhost:8080 -> airflow
- localhost:9090 -> spark-master
- localhost:9091 -> spark-worker-a
- localhost:9092 -> spark-worker-b
