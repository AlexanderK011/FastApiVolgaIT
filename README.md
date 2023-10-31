# FastApiVolgaIT

1. pip install -r requirements.txt
2. python uvicorn main:app --reload

#URL: http://127.0.0.1:8000/docs/  - swagger

Для того чтобы базы данных работали необходимо в .env ввести данные базы данных.
Для создания миграций необходимо:
1. alembic init migrations (уже создано)
2. alembic revision --autogenerate -m 'name commit'
3. alembic upgrade head

4. Для авторизации используется OAuth2, поэтому авторизация через login не сработает. Чтобы авторизоваться необходимо нажать на замочек либо сверху справа зеленую кнопочку Authorize. 
