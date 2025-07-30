import macro
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials='*',
    allow_methods='*',
    allow_headers='*'
)


@app.get("/macro/profit-and-loss")
def get_pnl(event: dict = Depends(macro.query_params)):
    try:
        response = macro.get_pnl(event)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/macro/balance-sheet")
def get_bs(event: dict = Depends(macro.query_params)):
    try:
        response = macro.get_bs(event)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/macro/cash-flow")
def get_cf(event: dict = Depends(macro.query_params)):
    try:
        response = macro.get_cf(event)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))