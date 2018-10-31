[![Build Status](https://travis-ci.com/Codebiosys/django-audit-trail.svg?token=QV3wJRfpprDN5XdYRpuT&branch=master)](https://travis-ci.com/Codebiosys/django-audit-trail)

# Django Audit Trail

Audit Trail is a simple Django app to enable database-level audit tracking. It
accomplishes this by exposing an API to use in migrations to install
triggers that performs audit record diff inserts into a central
`audit.log` table.


## Requirements

* PostgreSQL 9.6+
* pg-audit-json extension install for postgres
* Django 1.11+
* Python 3.6+


## Quick start

1. Add "audit" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        ...
        'audit_trail',
    ]
    ```

1. Run `python manage.py migrate` to create the polls models.


1. In your migrations:

    ```python
    from audit_trail.migrating import AddAuditToModel
    ...

    class Migration(migrations.Migration):
        ...
        dependencies = [
            ('audit_trail', '0001_initial'),   # Only add this in the first migration
        ]
        operations = [
            ...
            AddAuditToModel(name='MyModel', app_label="myapp')
        ]
    ```

## Running tests

It is highly encouraged you run the tests using the included docker stack.


1. Clone the application:

    ```
    > git clone https://github.com/CodeBiosys/django-audit-trail
    > cd django-audit-trail
    ```

1. Provision a new Docker machine called `django-audit-trail`:

    ```
    > docker-machine create -d virtualbox django-audit-trail
    > eval $(docker-machine env django-audit-trail)
    > docker-machine ls
		NAME                      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER        ERRORS
		django-audit-trail        *        virtualbox   Running   tcp://192.168.99.100:2376           v18.06.1-ce
    ```

    **Note the asterisk in the "ACTIVE" column.**


1. Build the application stack and start the services:

    ```
    > docker-compose build
		> docker-compose up -d
    ```

1. Run the tests

		```
		docker-compose run --rm app py.test
		```


## Considerations

When using this app, it is recommended you exclude tracking BLOB changes as these
can dramatically bloat your `audit.log table`.

