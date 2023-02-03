FROM python:3.9-slim-buster

# pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.
RUN mkdir ~/.pip && \
cd ~/.pip/  && \
echo "[global] \ntrusted-host =  pypi.douban.com \nindex-url = http://pypi.douban.com/simple" >  pip.conf

# Error: pg_config executable not found.
RUN apt-get update
RUN apt-get install -y libpq-dev python-dev libev-dev libevdev2 gcc
RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install uWSGI

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./create_superuser.py  /app/create_superuser.py
COPY ./entrypoint.sh        /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY ./src/django_project /app
RUN python  manage.py collectstatic  --noinput

ENV DJANGO_SETTINGS_MODULE=django_project.settings
ENV PYTHONUNBUFFERED=1


ENTRYPOINT ["sh", "/app/entrypoint.sh"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uwsgi", "--http", ":8000", "--module", "django_project.wsgi:application"]

