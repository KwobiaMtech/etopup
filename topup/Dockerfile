FROM python
COPY . /topup
WORKDIR /topup
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app","--reload"]