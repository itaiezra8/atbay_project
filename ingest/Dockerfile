FROM python:3.7-alpine
WORKDIR /code
COPY . .
COPY ../core /core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  requirements.txt
EXPOSE 5010
CMD [ "python", "ingest_server.py"]