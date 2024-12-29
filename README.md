# tron-wallet-search

## Тестовое задание
Написать микросервис, который будет выводить информацию по адресу в сети трон, 
его bandwidth, energy, и баланс trx, ендпоинт должен принимать входные данные - адрес.
Каждый запрос писать в базу данных, с полями о том какой кошелек запрашивался.

Написать юнит/интеграционные тесты
У сервиса 2 ендпоинта
- POST
- GET для получения списка последних записей из БД, включая пагинацию,
2 теста
- интеграционный на ендпоинт
- юнит на запись в бд
Примечания: использовать FastAPI, аннотацию(typing), SQLAlchemy ORM, для удобства с взаимодействию с 
троном можно использовать tronpy, для тестов Pytest


## Development

Backend docs: [backend/README.md](./backend/README.md).


General development docs: [development.md](./development.md).

This includes using Docker Compose, `.env` configurations, etc.

## Quick start

### Configure

Create `.env` file from  `.env.example`.

Before starting it, make sure you change at least the values for:

- `TRONGRID_API_KEY`

### Run tests
```bash
bash ./scripts/test-local.sh

```

### Just start

```bash
docker compose up --build

```
