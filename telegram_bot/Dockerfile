FROM python:3.11

WORKDIR /code
COPY ./telegram_bot/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./table_models.py /code/table_models.py
COPY ./telegram_bot/*.py /code/
CMD ["python", "main.py"]
