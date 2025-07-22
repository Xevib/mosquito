FROM python:3.12-slim

WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh



RUN apt-get update && apt-get install -y \
    build-essential \
    binutils \
    libpq-dev \
    gcc \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install pipenv


COPY Pipfile Pipfile.lock* /app/


RUN pipenv install --deploy --system


COPY . .


EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]