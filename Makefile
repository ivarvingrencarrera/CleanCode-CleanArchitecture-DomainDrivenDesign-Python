SHELL := /bin/bash -O globstar

linting:
	@echo
	isort . 
	@echo
	#ruff .
	#@echo
	blue --check --diff --color . 
	#@echo
	#mypy . 
	@echo
	pip-audit


formating:
	ruff --silent --exit-zero --fix .
	blue .

testing:
	pytest --cov-report term-missing --cov-report html --cov-branch --cov src/

testing_only:
	pytest -s -x -vv

install_hooks:
	@ scripts/install_hooks.sh

run:
	@ docker-compose up -d
	@ hypercorn src.api_currency:app --bind 0.0.0.0:3001 --reload

psql:
	@ docker compose exec -it postgres bash -c "psql -U root -d root"
