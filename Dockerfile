FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Streamlit
EXPOSE 8501

# Define o comando para rodar o Streamlit
CMD ["streamlit", "run", "Cadastro.py", "--server.port=8501", "--server.address=0.0.0.0"]