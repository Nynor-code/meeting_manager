.PHONY:
	build up down logs seed

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

seed:
	docker-compose exec web python sample_data.py

test:
	docker-compose exec web pytest

report:
	@echo "Generating reports (open in browser or access API endpoints)"
	@echo "http://localhost:5000/meetings/1/report"
	@echo "http://localhost:5000/meetings/1/report.pdf"

shell:
	docker-compose exec web flask shell