FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt 
RUN pip install --no-cache-dir --upgrade -r requirements.txt 
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]   


#questo file definisce l'immagine Docker per l'applicazione Flask
# - FROM python:3.10: utilizza l'immagine base di Python 3.10
# - EXPOSE 5000: espone la porta 5000 per l'applicazione Flask
# - WORKDIR /app: imposta la directory di lavoro all'interno del container
# - RUN pip install flask: installa il framework Flask
# - COPY . .: copia il contenuto della directory corrente nel container
# - CMD ["flask", "run", "--host", "0.0.0.0"]: avvia l'applicazione Flask
#docker run -d -p 5001:5000 rest-apis-flask-python
# - docker run -d -p 5001:5000 rest-apis-flask-python: esegue il container in modalità detached, mappando la porta 5001 del host alla porta 5000 del container, utilizzando l'immagine "rest-apis-flask-python"
# - Questo comando permette di eseguire l'applicazione Flask in un container Docker
# - La porta 5001 del host sarà accessibile per le richieste HTTP, mentre la porta 5000 del container sarà utilizzata dall'applicazione Flask
# - Assicurati di avere l'immagine "rest-apis-flask-python" costruita prima di eseguire questo comando
# - Puoi costruire l'immagine con il comando: docker build -t rest-apis-flask-python .
# - Dopo aver eseguito il container, puoi accedere all'applicazione Flask visitando http://localhost:5001 nel tuo browser
# - docker run -d -p 5001:5000 rest-apis-flask-python: esegue il container in modalità detached, mappando la porta 5001 del host alla porta 5000 del container, utilizzando l'immagine "rest-apis-flask-python"
# - Questo comando permette di eseguire l'applicazione Flask in un container Docker
# - La porta 5001 del host sarà accessibile per le richieste HTTP, mentre la porta 5000 del container sarà utilizzata dall'applicazione Flask
# - Assicurati di avere l'immagine "rest-apis-flask-python" costruita prima di eseguire questo comando
# - Puoi costruire l'immagine con il comando: docker build -t rest-apis-flask-python .
# - Dopo aver eseguito il container, puoi accedere all'applicazione Flask visitando http://localhost:5001 nel tuo browser