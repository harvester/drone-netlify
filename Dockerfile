FROM registry.suse.com/bci/python:3.10

COPY requirements.txt run.py /usr/src/app/

RUN pip3 install -r /usr/src/app/requirements.txt

ENTRYPOINT python3 /usr/src/app/run.py
