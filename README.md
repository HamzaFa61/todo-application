# TODO REST APIs with multiple users



## Setup the project

Add your PostgreSQL database's credentials in ```secrets.json``` file

### Install required packages
Create a virtual environment
```
python -m venv env
```
activate the virtual environment by using command:
```
. env/bin/activate
```
install the requirements
```
pip install -r requirements.txt
```
### Database migration
Run the following command to migrate the database
```
alembic upgrade head
```
## Run the application server
```
flask run
```
## Stop the application server
Press ctrl+C to stop the server