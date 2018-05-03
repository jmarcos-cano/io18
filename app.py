import  os, redis, time, platform
from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)

REDIS_HOST=os.getenv('REDIS_HOST', 'redis')
cache = redis.Redis(host=REDIS_HOST, port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    host=platform.node()
    DOCKER_SERVICE_NAME=os.getenv('DOCKER_SERVICE_NAME', host)
    return render_template('index.html',visit_counts=count, hostname=host, DOCKER_SERVICE_NAME=DOCKER_SERVICE_NAME)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
