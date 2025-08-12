import macro
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # must be a list
    allow_credentials=False,      # True only if you need cookies/auth
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/macro/pnl")
def get_pnl(event: dict = Depends(macro.query_params)):
    try:
        return macro.get_pnl(event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
