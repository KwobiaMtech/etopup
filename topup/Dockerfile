FROM python
COPY . /topup
WORKDIR /topup
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "127.0.0.1", "--reload"]