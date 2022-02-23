FROM python:3.7-alpine
WORKDIR /code
COPY . .
ADD ../core /core
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r  postgresql/requirements.txt
EXPOSE 5050
CMD [ "python", "postgresql/app.py"]