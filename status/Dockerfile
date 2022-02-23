FROM python:3.7-alpine
WORKDIR /code
COPY . .
ADD ../core /core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  status/requirements.txt
EXPOSE 5030
CMD [ "python", "status/status_server.py"]