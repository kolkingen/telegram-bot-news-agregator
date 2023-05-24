FROM python:3.11

WORKDIR /code
COPY ./news_agregator/requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./table_models.py /code/table_models.py
COPY ./news_agregator/*.py /code/
CMD ["python", "main.py"]
