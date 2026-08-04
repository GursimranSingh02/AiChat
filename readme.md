## Migrations using alembic

- To apply the migrations run: `alembic upgrade head`

- To create a new migration run: `alembic revision -m "your_migration_message"`


## Run the server 
`uvicorn app.main:app --port=8000 --reload`