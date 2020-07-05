# Database


## ER-диаграмма

[PDF](./docs/er.pdf)

## Плагины

* [uuid-ossp](https://postgrespro.ru/docs/postgrespro/11/uuid-ossp)
* [pg_similarity](https://github.com/eulerto/pg_similarity)

## Миграции

Создание миграции

```bash
export PG_CONNECTION=postgresql://login:password@host:port/database_name
alembic revision --autogenerate
```

Накатывание миграции

```bash
export PG_CONNECTION=postgresql://login:password@host:port/database_name
alembic upgrade head
```

    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
