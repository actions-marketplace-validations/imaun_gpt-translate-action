FROM python:3.9

WORKDIR /github/workspace

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "translate.py" ]