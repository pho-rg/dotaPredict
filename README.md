## Backend

### Prerequises

> Dockerfile interpretation: make sure separator line for file `backend/dotaPredictBackEnd/django.sh` is set to LF (not CRLF)

> Backend .env file filled based on .template `backend/dotaPredictBackEnd/.template` (ask for value)

> Frontend .env file filled based on .template `frontend/dota-predict-frontend/.template` (ask for value)

### Launch via docker swarm 

Initiate the swarm (in root path) :
```
docker swarm init
```
Build frontend image **(needed every time the code is updated)** :
```
docker build -t dota-predict-frontend:latest ./frontend/dota-predict-frontend
(only for updates) docker service update --force dota-predict_frontend
```
Build backend image **(needed every time the code is updated)** :
```
docker build -t dotapredict-api:latest ./backend/dotaPredictBackEnd
(only for updates) docker service update --force dota-predict_dotapredict-api
```
Deploy stack with built images :
```
docker stack deploy -c docker-compose.yml dota-predict
```
Remove stack:
```
docker stack rm dota-predict
```

### Set a user's role to 'analyst'

> Open the terminal of the "db" docker
> psql -U <username> -d <dbname> (check the .env file)
> find the user to edit with ```SELECT * FROM "userapp_user";```
> execute ```UPDATE "userapp_user" SET role = 'analyst' WHERE id = <id>;```

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