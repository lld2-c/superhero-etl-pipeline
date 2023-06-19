FROM python:3.9 
# Or any preferred Python version.

ADD ./requirements.txt .
RUN pip install -r ./requirements.txt
ADD . .
CMD ["python3.9", "app.py"] 
# Or enter the name of your unique directory and parameter set.