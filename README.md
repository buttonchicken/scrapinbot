# scrapinbot
Python django based microservice that can scrape product urls from sites like ajio

sample urls - https://www.ajio.com/s/boys-tshirts,https://www.ajio.com/men-shirts/c/830216013

Steps to run the application:

Install dependencies using pip3 install -r req.txt

Install redis using the link https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/

Run the commands:

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver

Command to run celery:

celery -A scrapinbot worker --concurrency=3 -l info

Full documenatation:

https://docs.google.com/document/d/1kpuFrGU08Ymg2O5acWtcsCBkRiCHA7q8tM1PWHei_h8/edit?usp=sharing
