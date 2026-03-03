Generic single-database configuration.

# Deploy a migration

```
alembic revision --autogenerate -m "Change note"
alembic upgrade head
```

# Audit versions

```
alembic history          # list all revisions (oldest → newest)
alembic history --verbose
alembic current          # see which revision the DB is at
alembic heads            # see latest revision(s)
```

# Common development workflows

Downgrade last migration:

`alembic downgrade -1`

Delete or fix the bad file in migrations/versions/.

```
alembic revision --autogenerate -m "better migration"
alembic upgrade head
```