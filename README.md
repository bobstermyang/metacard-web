# Deploying marqeta app

# Step 1
```
pip install -r requirements.txt
```

# Step 2
Go to
```
./sma/
```

# Step 3
Run migrations
```
python manage.py makemigrations auth
python manage.py makemigrations home
python manage.py migrate
python manage.py migrate home
```

# Step 4
Run server
```
python manage.py runserver host:port
```
