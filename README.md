# Folder replicator

This app replicates folder `source` into folder `replica`.

## On the local machine

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
pip3 install --upgrade pip
pip3 install -r ./.docker/cron/requirements.txt
```

### Run tests
```
python -m unittest discover -s tests
```

### Run the job
Running locally every <interval_seconds>. 
Folder `replica` is mirrored from the `source` folder automatically.
```
# python main.py <source_dir> <replica_dir> <interval_seconds> <log_filename>
python main.py ./source ./replica 5 ./replicator1.log
```

## In a Docker container
The same in a docker container
```
docker compose up -d
docker compose exec -it cron /usr/local/bin/python3 /app/cron/main.py /app/cron/source /app/cron/replica 5 /app/cron/replicator.log
```
