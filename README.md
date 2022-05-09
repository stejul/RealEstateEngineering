TODO
- implement correct marquez.yml configuration
  - didn't work because credentials were wrong for marquez-db

`docker system prune --all && docker-compose -f docker-compose.yml -f docker-compose.seed.yml up -V --force-recreate --remove-orphans`
Sites to scrape:
* [LaendleImmo](https://www.laendleimmo.at/)
* [ImmobilienScout](https://www.immobilienscout24.at/)
* [ImmoWelt](https://immowelt.at)
* [Immobilien](https://immobilien.net)
