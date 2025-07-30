import psycopg2
import pandas as pd
from fastapi import Query, Depends
import __init__ as ini


def query_params(
        company_name: str = Query(..., description="Company name"),
        fy: str = Query(..., description="Fiscal Year (e.g., Q4FY23)")
):
    return {
        "company_name": company_name,
        "fy": fy
        }


def get_pnl(event: dict = Depends(query_params)):
    conn = psycopg2.connect(ini.dsn)
    query = f"""
        SELECT * FROM financials.pnl
        WHERE company_name = %s AND fy = %s
    """

    df = pd.read_sql(query, conn, params=(event['company_name'], event['fy']))
    conn.close()

    if df.empty:
        return {"message": "No data found for the given company and FY."}

    return df.to_dict(orient="records")


def get_bs(event: dict = Depends(query_params)):
    conn = psycopg2.connect(ini.dsn)
    query = f"""
        SELECT * FROM financials.bs
        WHERE company_name = %s AND fy = %s
    """

    df = pd.read_sql(query, conn, params=(event['company_name'], event['fy']))
    conn.close()

    if df.empty:
        return {"message": "No data found for the given company and FY."}

    return df.to_dict(orient="records")


def get_cf(event: dict = Depends(query_params)):
    conn = psycopg2.connect(ini.dsn)
    query = f"""
        SELECT * FROM financials.cf
        WHERE company_name = %s AND fy = %s
    """

    df = pd.read_sql(query, conn, params=(event['company_name'], event['fy']))
    conn.close()

    if df.empty:
        return {"message": "No data found for the given company and FY."}

    return df.to_dict(orient="records")