FROM python:3.9-alpine
WORKDIR /code
COPY process /code/process
ADD core /code/core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  process/requirements.txt
EXPOSE 5020
ENV PYTHONPATH "${PYTHONPATH}:/code"
CMD [ "python", "process/process_server.py"]