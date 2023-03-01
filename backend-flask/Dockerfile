# Stage 1: Base stage
FROM python:3.10-slim-buster as base
WORKDIR /backend-flask
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Stage 2: Development stage
FROM base as development
COPY . .
ENV FLASK_ENV=development
EXPOSE ${PORT}
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]

# Stage 3: Production stage
FROM base as production
COPY . .
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]
