FROM python:3.9 
# Or any preferred Python version.

ADD . .
RUN pip install -r ./requirements.txt
# change path 
COPY ./config/kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json
RUN kaggle datasets download dannielr/marvel-superheroes/v/3 -p ./data --force
# RUN alembic upgrade heads >> logs/etl.log
ENTRYPOINT python app.py