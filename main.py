from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from database import SessionLocal
from routers import users, transports, rents, payments, admin

db = SessionLocal()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
app.include_router(users.authusers)
app.include_router(transports.transportrout)
app.include_router(rents.rentscontr)
app.include_router(payments.paymrout)
app.include_router(admin.adminaccounts)
app.include_router(admin.admintransp)
app.include_router(admin.adminrent)



