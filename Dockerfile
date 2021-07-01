FROM vichuhari100/care-production-base:latest

RUN apt-get install -y \
  --no-install-recommends \
  libmagic-dev \
  && rm -rf /var/lib/apt/lists/* \
  &&:

RUN addgroup --system django \
  && adduser --system --ingroup django django

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
  && rm -rf /requirements

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

COPY --chown=django:django . /app

USER django

WORKDIR /app

EXPOSE 9000
