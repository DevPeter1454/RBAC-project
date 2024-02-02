import os
from app.core.config import settings
from app.api import router
from app.core.setup import create_application

from fastapi import Request


app = create_application(router=router, settings=settings)


# static_dir =os.path.join(os.getcwd(), "my-react-app", "dist", "static")

# app.mount("/static", StaticFiles(directory=static_dir), name="static")


# @app.get("/")
# def root(request: Request):
#     return templates.TemplateResponse("email_templates.html", {"request": Request})

# from fastapi import FastAPI


# app = FastAPI()

# @app.get("/")
# def root():
#         return {
#             "message": "Server running"
#         }
