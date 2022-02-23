FROM python:3.7-alpine
WORKDIR /code
COPY . .
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  requirements.txt
EXPOSE 5030
CMD [ "python", "status_server.py"]