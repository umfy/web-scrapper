# web-scrapper
Simple web scrapper that records the office queue status.

The  *urllib.request* didn't work for that website because it required JavaScript to render its content.

Data format is:

**[timestamp, number of people waiting in queue, number of employees, number of open tickets remaining for today]**
## Create and activate virtual environment
```sh
python -m venv env

env/Scripts/activate
```

## Run script
```sh
python main.py
```