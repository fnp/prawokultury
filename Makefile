.PHONY: deploy


deploy: prawokultury/settings.d/local.py
	pip install -r requirements.txt
	./manage.py migrate --noinput
	./manage.py collectstatic --noinput

