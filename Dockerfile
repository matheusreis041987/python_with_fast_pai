FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

#contruir a imagem: docker build -t contas-api .
#rodar passando as variáveis de ambiente: docker run --env-file .env  -p 80:80 contas-api