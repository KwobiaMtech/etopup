FROM python
ENV http_proxy http://proxy-chain.xxx.com:911/
ENV https_proxy http://proxy-chain.xxx.com:912/
COPY . /topup
WORKDIR /topup
RUN pip install -r requirements.txt
EXPOSE 7030
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
