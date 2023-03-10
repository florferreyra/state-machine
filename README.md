# state-machine

### Start up project

```commandline
$ docker-compose up
```

### Django Admin
- Create a superuser
  - Go inside app container: `$ docker-compose exec app bash  `
  - Apply migrations: `/app/app# python manage.py migrate`
  - Create superuser: `/app/app# python manage.py createsuperuser`

- Access to site: http://0.0.0.0:8080/admin/
