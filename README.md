# Folder replicator

This app replicates folder `source` into folder `replica`.

## On local machine

### Clone repo
```
git clone git@github.com:otasnovotny/folder_replicator.git
cd ./folder_replicator
```

### Prepare virtual env
```
# Install python:3.12.1
sudo apt install python3.12-venv
python3.12 -m venv ./.venv
source ./.venv/bin/activate
```

### Run tests
```
python -m unittest discover -s tests
```

### Run locally (one time run)
```
python main.py ./source ./replica --logFilename=replicator1.log
```

## In a Docker container (periodically)

Running in docker container the sync process is triggered as a cron every <interval_seconds>. 
Folder `replica` is mirrored from the `source` folder automatically.

```
docker compose up -d
docker compose exec -it cron /usr/local/bin/python3 /app/cron/main.py /app/cron/source /app/cron/replica 5 /app/cron/replicator.log
```
