from typing import Union


from app_factory import create_app
from core.config import settings
from database import connect_to_mongo

app = create_app()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn

    if settings.ENV.lower() == "development":
        uvicorn.run(app, host="0.0.0.0", port=443)
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=443,
            # ssl_keyfile=settings.SSL_KEY_PATH,  # Path to the private key
            # ssl_certfile=settings.SSL_CERT_PATH,  # Path to the certificate
        )
