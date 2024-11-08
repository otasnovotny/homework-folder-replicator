# Folder replicator
This is an input test task for a software developer position.

## Assignment
Please implement a program that synchronizes two folders: source and replica. 
The program should maintain a full, identical copy of source folder at replica folder.
Solve the test task by writing a program in one of these programming languages:
- Python
- C/C++
- C#

Synchronization must be one-way: after the synchronization content of the
replica folder should be modified to exactly match content of the source
folder

Synchronization should be performed periodically.

File creation/copying/removal operations should be logged to a file and to the
console output

Folder paths, synchronization interval and log file path should be provided
using the command line arguments

It is undesirable to use third-party libraries that implement folder
synchronization

It is allowed (and recommended) to use external libraries implementing other
well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is
perfectly acceptable to use a third-party (or built-in) library.


## Solution

This app replicates folder `source` into folder `replica`.

### On the local machine

#### Clone repo
```
git clone git@github.com:otasnovotny/folder_replicator.git
cd ./folder_replicator
```

#### Prepare virtual env
```
# Install python:3.12.1
sudo apt install python3.12-venv
python3.12 -m venv ./.venv
source ./.venv/bin/activate
pip3 install --upgrade pip
pip3 install -r ./.docker/cron/requirements.txt
```

#### Run tests
```
python -m unittest discover -s tests
```

#### Run the job
Running locally every <interval_seconds>. 
Folder `replica` is mirrored from the `source` folder automatically.
```
# python main.py <source_dir> <replica_dir> <interval_seconds> <log_filename>
python main.py ./source ./replica 5 ./replicator_local.log
```

### In a Docker container
The same in a docker container
```
docker compose up -d
docker compose exec -it cron /usr/local/bin/python3 /app/cron/main.py /app/cron/source /app/cron/replica 5 /app/cron/replicator_docker.log
```
