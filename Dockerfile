FROM python:latest
# unpinned base image

ENV DB_PASSWORD=admin123
ARG API_TOKEN=d41d8cd98f00b204e9800998ecf8427e
# secrets baked into image layers

COPY . /app
# copies .env, .git and everything else; invalidates the dependency cache
WORKDIR /app

ADD http://example.com/tool.tar.gz /tmp/
# ADD from a URL, no checksum

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl sudo openssh-server
# no --no-install-recommends, no cache cleanup, unpinned packages

RUN curl -s http://example.com/setup.sh | sh
# unverified remote script over plain HTTP

RUN pip install flask requests pyyaml
# unpinned dependencies

RUN chmod -R 777 /app
# world-writable

EXPOSE 22 5000
# exposes SSH

CMD ["python", "app.py"]
CMD ["python", "other.py"]
# only the last CMD runs, and the container runs as root with no HEALTHCHECK
