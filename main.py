import uvicorn
from dev_db_server import dev_db_app

uvicorn.run(
    dev_db_app,
    use_colors=True,
    host="127.0.0.1",
    port=8000,
    reload=0,
)
