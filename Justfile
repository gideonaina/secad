
prod:
    docker compose -f secad.docker-compose.yml up

prod-build:
    docker compose -f secad.docker-compose.yml up --build

prod-down:
    docker compose -f secad.docker-compose.yml down

prod-nuke:
    docker compose -f secad.docker-compose.yml down -v
    docker volume rm $(docker volume ls -q)