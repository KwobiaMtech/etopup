FROM python
COPY . /topup
WORKDIR /topup
RUN pip install -r requirements.txt
EXPOSE 7030
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
