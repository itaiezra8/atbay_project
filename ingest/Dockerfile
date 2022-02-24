FROM python:3.9-alpine
WORKDIR /code
COPY ingest /code/ingest
ADD core /code/core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  ingest/requirements.txt
EXPOSE 5010
ENV PYTHONPATH "${PYTHONPATH}:/code"
CMD [ "python", "ingest/ingest_server.py"]