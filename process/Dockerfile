FROM python:3.7-alpine
WORKDIR /code
COPY . .
COPY ../core /core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  requirements.txt
EXPOSE 5020
CMD [ "python", "process_server.py"]