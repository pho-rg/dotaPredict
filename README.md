## Backend

### Prerequises

> Dockerfile interpretation: make sure separator line for file `backend/dotaPredictBackEnd/django.sh` is set to LF (not CRLF)

### Database container

Folder
```
cd \backend\dotaPredictBackEnd\
```

Start container
````
docker compose up -d db
````

Stop container
````
docker compose down
````

Stop container deleting volume and datas
```
docker compose down -v
```

### Djangoapps container

Folder
```
cd \backend\dotaPredictBackEnd\
```

Build project
```
docker compose build djangoapp
```

Start container
```
docker compose up djangoapp
```

Stop container
````
docker compose down
````

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
npm run dev
```

PORT
> website host on http://localhost:3000/

Make sure it's exposed to PORT 3000 to pass CORS API restriction (backend side)

### Register to login

From a webbrowser, hit http://localhost:3000/login. Click on **create an account** to register. Once register you are redirected to login.