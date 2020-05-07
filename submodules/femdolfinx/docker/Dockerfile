FROM dolfinx/real

# set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip3 install --upgrade pip -r ../requirements.txt

COPY ./femdolfinx /app/submodules/femdolfinx/femdolfinx
COPY ./ /app/submodules/femdolfinx

WORKDIR /app/submodules/femdolfinx

# CMD export FLASK_APP=app.py && flask run --host=0.0.0.0 --port=5555
CMD gunicorn --bind 0.0.0.0:5555 wsgi:app