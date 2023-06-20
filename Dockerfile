FROM python:3.9 
# Or any preferred Python version.

ADD ./requirements.txt .
RUN pip install -r ./requirements.txt
ADD . .
RUN export KAGGLE_CONFIG_DIR=./config 
RUN kaggle datasets download dannielr/marvel-superheroes/v/3 -p ./data --force
RUN python setup.py
RUN alembic upgrade heads > logs/etl.log
CMD ["python", "app.py"] 