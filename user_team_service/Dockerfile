FROM python:3.12-slim

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY  . .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn


RUN chmod +x entrypoint.sh

CMD ["/bin/sh", "entrypoint.sh"]