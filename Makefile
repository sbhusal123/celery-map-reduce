runserver:
	cd src && python manage.py runserver
start_pdf_to_text_worker:
	cd src && celery -A src worker -l info --queues=pdf_to_text
start_worker:
	cd src && celery -A src worker -l info
make_migrations:
	cd src && python manage.py makemigrations
migrate:
	cd src && python manage.py migrate
createsuperuser:
	cd src && python manage.py createsuperuser
shell:
	cd src && python manage.py shell
start_ner_worker:
	cd src && celery -A src worker -l info --queues=named_entity_extraction
createsuperuser:
	cd src && python manage.py createsuperuser
