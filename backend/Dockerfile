FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]