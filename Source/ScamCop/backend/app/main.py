from fastapi import FastAPI
from app.api.analyze import router

app = FastAPI(title='ScamCop')
app.include_router(router)

@app.get('/health')
async def health(): 
    return {'status':'ok'}
