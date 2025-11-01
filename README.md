## Flask Event


* docker compose exec api flask db init
* docker compose exec api flask db migrate -m "Added location field to Event"
* docker compose exec api flask db upgrade