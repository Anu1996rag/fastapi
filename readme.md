## FastApi

This is a fastapi application backed by Postgresql database.

This application stored the posts created by multiple users and the votes/likes they have given to each of the posts.

The api in response provides a detailed information about the post contents, the owner/user who created the post and the votes/likes it has been given.

## Installation

Please follow the steps to run the application successfully.

1. Clone the repository using the below command.

```commandline
git clone https://github.com/Anu1996rag/fastapi.git
```

2. Create a virtual environment
```commandline
python3 -m venv <virtual_environment_name>
```
3. Activate the virtual environment
```commandline
source /<virtual_environment_name>/bin/activate
```
4. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```commandline
pip install -r requirements.txt
```
5. Run the server using the below command.
```commandline
uvicorn app.main:app
```
6. Make sure the postgresql service is installed in your system and it is running by running the following command.
```commandline
sudo /etc/init.d/postgresql status
```
7. To start it you can issue the command
```commandline
sudo /etc/init.d/postgresql start
```
8. To stop you can issue the command
```commandline
sudo /etc/init.d/postgresql-8.3 stop
```
9. If you are using poetry, follow the below set of commands.
```commandline
poetry shell
poetry install
poetry run uvicorn app.main:app
```
10. You should see the below response
```commandline
INFO     2022-11-16 11:30:28.782 | uvicorn.server:serve | Started server process [17055]
INFO     2022-11-16 11:30:28.783 | uvicorn.lifespan.on:startup | Waiting for application startup.
INFO     2022-11-16 11:30:28.783 | uvicorn.lifespan.on:startup | Application startup complete.
INFO     2022-11-16 11:30:28.784 | uvicorn.server:_log_started_message | Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## API Docs

To access the API documentation, use the URL
http://127.0.0.1:8000/docs#

## Using Docker 

You can also pull the docker image using the below command.

Make sure you have the docker installed in your system.

```commandline
docker pull anurag1996/fastapi-postgres
```

Check logs for the api using below command
```commandline
docker logs <container_id> --tail N
```