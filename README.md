# The SQL CLI

## Description 

This is a cli utility build on python. This helps you to save your frequently used query with name and run them over a particular window at various granularity. Currently it only support daily granularity. It also let you specify some extra filter like category to run your analysis. The application is extendable. Curently it support MySQL source to run your query but other DB support can be easily added. The project is built in python. It use poetry to build the project. 




## Installation and Run Guide


### installation guide ::

python requirment >3.7 <3.10.

install poetry in your system `pip install poetry`.

run `poetry install`. It will install the dependencies for the project and create a venv for the project. 

run `poetry shell` to login in the venv.

run `poetry build` to create fresh wheel artefact


### Run guide ::

Build the docker file under `db/mysql/Dockerfile`

Start the mysql container `docker run --env-file=./db/mysql/.env -p 3306:3306 mysql:0.1`

Run the `load_data.py` under `db` to load the data. It should run inside the venv created. This will help to load the data into the mysql container. Place the `data.csv` inside the `db` dir. 

Run the cli application by running `python cli.py demand daily 2010-12-01 2010-12-10 T-Shirt`. It should use the venv python


