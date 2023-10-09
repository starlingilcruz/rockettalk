# Rockettalk

## Real-time chat application

Rapid real-time chat application using django-channels and redis for caching

### Run development: 

```
  docker-compose up --build
```

### Run tests

Run and access the docker container:

```
  docker exec -ti rockettalk bash
```

And run the test suite with the following command: 

```
  python manage.py test
```