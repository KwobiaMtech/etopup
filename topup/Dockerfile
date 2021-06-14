FROM python
COPY . /topup
WORKDIR /topup
RUN pip install \
  --extra-index-url http://host.docker.internal:8000 \
  -r requirements.txt
EXPOSE 7030
EXPOSE 54320
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
