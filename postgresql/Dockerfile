FROM python:3.9-alpine
WORKDIR /code
COPY postgresql /code/postgresql
ADD core /code/core
RUN apk add --no-cache libpq-dev gcc musl-dev linux-headers
RUN pip install -r postgresql/requirements.txt
EXPOSE 5050
ENV PYTHONPATH "${PYTHONPATH}:/code"
CMD [ "python", "postgresql/app.py"]