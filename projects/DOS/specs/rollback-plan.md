# Plan de Rollback (Rollback Plan - TaskLiteJota)

En caso de fallo crítico de datos o corrupción en la base de datos local:
1. Apagar el servidor Uvicorn (`Ctrl + C`).
2. Copiar la base de datos de respaldo `db.sqlite3.bak` (si existiese) de vuelta a `db.sqlite3`.
3. Reiniciar el servidor FastAPI.