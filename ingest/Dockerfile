FROM python:3.7-alpine
WORKDIR /code
COPY . .
ADD ../core /core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  ingest/requirements.txt
EXPOSE 5010
CMD [ "python", "ingest/ingest_server.py"]