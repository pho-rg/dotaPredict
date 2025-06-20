## Backend

### Prerequises

> Dockerfile interpretation: make sure separator line for file `backend/dotaPredictBackEnd/django.sh` is set to LF (not CRLF)

> Backend .env file filled based on .template `backend/dotaPredictBackEnd/.template` (ask for value)

> Frontend .env file filled based on .template `frontend/dota-predict-frontend/.template` (ask for value)

### Launch dotapredict API

Folder
```
cd \backend\dotaPredictBackEnd\
```

Start container
````
docker compose up --build
````

Stop container
````
docker compose down
````

Stop container deleting volume and datas
```
docker compose down -v
```

PORT
> API reachable on http://localhost:8000/

CORS allowed only for PORT 3000 (frontend side)

## Frontend

### Prerequises

Folder
```
cd \frontend\dota-predict-frontend\
```

Install packages
```
npm install
```

### Start server

Folder
```
cd \frontend\dota-predict-frontend\
```

Start server
```
docker-compose up --build
docker compose ups
```

PORT
> website host on http://localhost:3000/

Make sure it's exposed to PORT 3000 to pass CORS API restriction (backend side)

### Register to login

From a webbrowser, hit http://localhost:3000/. Click on **create an account** to register. Once register you are redirected to login.