
build: .env
	docker-compose build

run: .env
	docker-compose up

dev: .env
	docker-compose -f devel-compose.yml up --build

init-npm:
	cd frontend && npm install 

init-pip:
	python3 -m pip install --upgrade -r requirements.txt

init: init-pip init-npm

init-db: .env
	python3 db_init.py

.env:
	python3 create_env.py

stop:
	docker-compose down

firstrun: .env build init-db
	echo "\033[31mRun 'make run' to start MakerAdmin\033[0m"

frontend-dev-server:
	mkdir -p frontend/node_modules
	docker-compose -f frontend/dev-server-compose.yaml rm -f
	docker volume rm makeradmin_node_modules
	docker-compose -f frontend/dev-server-compose.yaml up --build

.PHONY: build init-db
