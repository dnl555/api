FROM python:3.8

USER root

EXPOSE 8181

COPY . /app

WORKDIR /app

RUN pip install pipenv==2022.7.4
RUN pipenv install

CMD ["pipenv", "run", "gunicorn", "-w", "4", "--timeout", "240", "-k", "uvicorn.workers.UvicornWorker", "api.main:app", "--bind", "0.0.0.0:8181"]
