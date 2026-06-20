from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import users, owners

app = FastAPI(
    title='Apartment Management System',
    version='1.0.0',
)

app.include_router(users.router)
app.include_router(owners.router)

app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'detail': 'An unexpected error occurred'}
    )

@app.get('/health')
def health_check():
    return {'status': 'ok'}