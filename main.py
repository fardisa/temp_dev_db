import uvicorn
from dev_db_server import dev_db_app

uvicorn.run(dev_db_app, use_colors=True)

# uvicorn.run("dev_b_server:app", reload=True, workers=2)
