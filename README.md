# BasketBallManagementSystem

## Python Version  -
`Python 3.9.9`

## Requirement setup

### Localhost setup
```
python -m venv venv
```
```source venv/bin/activate``` or for windows ```venv\Scripts\activate```

```
pip install -r requirements.txt
```

### Create DB tables
```
 python manage.py makemigrations
```

### apply changes to the DB
```
  python manage.py migrate 
```

### Run the Application
```
 python manage.py runserver  
```

### POSTMAN
```
 http://127.0.0.1:8000/health (Content-Type: application/json) (GET)
```
