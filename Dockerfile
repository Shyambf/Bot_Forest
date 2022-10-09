FROM python:3.10.7-slim-buster
RUN mkdir /Bot_forest
WORKDIR /Bot_forest
RUN pip install pipenv
COPY Pipfile /Bot_forest
COPY Pipfile.lock /Bot_forest
RUN pipenv install --deploy --system --ignore-pipfile
COPY . /Bot_forest
ENTRYPOINT [ "python", "bot.py" ]