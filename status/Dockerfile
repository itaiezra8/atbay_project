FROM python:3.9-alpine
WORKDIR /code
COPY status /code/status
ADD core /code/core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  status/requirements.txt
EXPOSE 5030
ENV PYTHONPATH "${PYTHONPATH}:/code"
CMD [ "python", "status/status_server.py"]