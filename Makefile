run:
	python manage.py runserver

tests:
	python manage.py test

migrations:
	cd backend ; \
	python manage.py makemigrations ; \
	python manage.py makemigrations api_core ; \
	python manage.py makemigrations data_parsing; \
	python manage.py migrate	


deploy:
	cd backend ; \
	. venv/bin/activate ; \
	pip install -r requirements.txt ; \
	python manage.py migrate ; \
	python manage.py collectstatic --no-input
#	rm -rf schedulator_frontend/build
#	npm install --prefix schedulator_frontend
#	npm run-script build --prefix schedulator_frontend
	systemctl restart gunicorn_statistic_vorbind_covid19.socket
	systemctl restart gunicorn_statistic_vorbind_covid19.service
	systemctl restart nginx


today:
	cd backend ; \
	. venv/bin/activate ; \
	python manage.py collect_sources 3 ; \
	python manage.py analyze_raw_data --today ; \
	python manage.py analyze_each_case --today 
