FROM python:3.11.4-slim-buster as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . . 

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# ENTRYPOINT ["sh", "entrypoint.sh"]



# ###########
# # BUILDER #
# ###########

# # pull official base image
# FROM python:3.11.4-slim-buster as builder

# # set work directory
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install system dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc

# # lint
# RUN pip install --upgrade pip
# COPY . /usr/src/app/

# # install python dependencies
# COPY ./requirements.txt .
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# #########
# # FINAL #
# #########

# # pull official base image
# FROM python:3.11.4-slim-buster

# # create directory for the app user
# RUN mkdir -p /home/app

# # create the app user
# RUN addgroup --system app && adduser --system --group app

# # create the appropriate directories
# ENV HOME=/home
# ENV APP_HOME=/home/web
# RUN mkdir $APP_HOME
# RUN mkdir $APP_HOME/staticfiles
# RUN mkdir $APP_HOME/mediafiles
# WORKDIR $APP_HOME

# # install dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends netcat
# COPY --from=builder /usr/src/app/wheels /wheels
# COPY --from=builder /usr/src/app/requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --no-cache /wheels/*

# # copy entrypoint.prod.sh
# COPY ./entrypoint.prod.sh .
# RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
# RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# # copy project
# COPY . $APP_HOME

# # chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# # change to the app user
# USER app

# # run entrypoint.prod.sh
# ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]