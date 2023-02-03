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


COPY ./src/django_project /app

ENV DJANGO_SETTINGS_MODULE=django_project.settings
ENV PYTHONUNBUFFERED=1

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uwsgi", "--http", ":8000", "--module", "src.django_project.wsgi:application"]


