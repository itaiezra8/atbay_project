FROM python:3.7-alpine
WORKDIR /code
COPY . .
ADD ../core /core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  process/requirements.txt
EXPOSE 5020
CMD [ "python", "process/process_server.py"]