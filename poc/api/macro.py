import psycopg2
import pandas as pd
from fastapi import Query, Depends
import __init__ as ini

def query_params(
    company_name: str = Query(..., description="Company name"),
    fy: str = Query(..., description="Fiscal Year (e.g., Q4FY23)")
):
    return {"company_name": company_name, "fy": fy}

def get_pnl(event: dict = Depends(query_params)):
    conn = psycopg2.connect(ini.dsn)
    sql = """
        SELECT *
        FROM financials.pnl
        WHERE company_name = %s AND fy = %s
    """
    df = pd.read_sql(sql, conn, params=(event["company_name"], event["fy"]))
    conn.close()

    if df.empty:
        return []

    # Optional: consistent, JSON-friendly types
    df = df.convert_dtypes()
    return df.to_dict(orient="records")
