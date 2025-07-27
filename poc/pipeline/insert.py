import os
import psycopg2
import pandas as pd
import __init__ as ini
from dotenv import load_dotenv

# Load environment variables (like DB credentials) from a .env file
load_dotenv()

# Function to add a 'fy' (financial year and quarter) column to a DataFrame
def add_fy_quarter_column(df, date_col='date', new_col='fy'):
    dates = pd.to_datetime(df[date_col])  # Convert date column to datetime format
    quarters = pd.Series(index=dates.index, dtype="object")  # Create empty column for quarter
    fy_years = pd.Series(index=dates.index, dtype="int")  # Create empty column for financial year

    # Assign quarters and corresponding financial years based on month
    quarters[dates.dt.month.isin([4, 5, 6])] = 'Q1'
    fy_years[dates.dt.month.isin([4, 5, 6])] = dates.dt.year + 1

    quarters[dates.dt.month.isin([7, 8, 9])] = 'Q2'
    fy_years[dates.dt.month.isin([7, 8, 9])] = dates.dt.year + 1

    quarters[dates.dt.month.isin([10, 11, 12])] = 'Q3'
    fy_years[dates.dt.month.isin([10, 11, 12])] = dates.dt.year + 1

    quarters[dates.dt.month.isin([1, 2, 3])] = 'Q4'
    fy_years[dates.dt.month.isin([1, 2, 3])] = dates.dt.year

    # Combine quarter and FY year into a single string column
    fy_years = fy_years.astype('Int16')
    df[new_col] = quarters + 'FY' + fy_years.astype(str).str[-2:]
    return df

# Create schema in the database if it doesn't already exist
def create_schema_if_not_exists(conn, schema_name):
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")  # SQL to create schema
        conn.commit()  # Save changes

# Create table in the database if it doesn't already exist
def create_table_if_not_exists(conn, schema_name, table_name, df):
    # Map pandas dtypes to SQL types
    dtype_map = {
        'int64': 'NUMERIC',
        'float64': 'NUMERIC',
        'object': 'TEXT',
        'datetime64[ns]': 'DATE'
    }

    columns_sql = []
    for col, dtype in df.dtypes.items():
        sql_type = dtype_map.get(str(dtype), 'TEXT')  # Default to TEXT if not found
        columns_sql.append(f"{col} {sql_type}")  # Create column definition

    # Set primary key if required columns are present
    primary_key = "PRIMARY KEY (company_name, date, fy)" if {'company_name', 'date', 'fy'}.issubset(df.columns) else ""

    # Combine SQL and execute
    create_query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
            {', '.join(columns_sql)}
            {',' if primary_key else ''} {primary_key}
        );
    """

    with conn.cursor() as cursor:
        cursor.execute(create_query)
        conn.commit()

# Check if a specific record already exists in the database
def record_exists(conn, schema, table, company, date, fy):
    query = f"""
        SELECT 1 FROM {schema}.{table}
        WHERE company_name = %s AND date = %s AND fy = %s
        LIMIT 1
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (company, date, fy))
        return cursor.fetchone() is not None  # Return True if record exists

# Insert only new records from DataFrame into the database
def insert_df_if_new(df, schema, table, conn):
    new_rows = []
    for _, row in df.iterrows():
        if not record_exists(conn, schema, table, row['company_name'], row['date'], row['fy']):
            new_rows.append(tuple(row))  # Add new row to list

    if not new_rows:
        print(f"No new data to insert into {schema}.{table}.")
        return

    # Prepare insert SQL
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"""
        INSERT INTO {schema}.{table}
        ({columns}) VALUES ({placeholders})
    """

    # Execute insertion
    with conn.cursor() as cursor:
        cursor.executemany(insert_query, new_rows)
    conn.commit()
    print(f"{len(new_rows)} new rows inserted into {schema}.{table}.")

# Extract and transform Profit & Loss data from Excel
def extract_pnl(file_name):
    file_path = os.path.join(ini.raw_data_dir, file_name)  # Build file path
    df = pd.read_excel(file_path, sheet_name="profit_loss")  # Read sheet
    df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)  # Rename first column
    df_t = df.transpose()  # Transpose rows/columns
    df_t.columns = df_t.iloc[0]  # First row becomes header
    df_t = df_t.iloc[1:].reset_index().rename(columns={"index": "date"})  # Reset index

    df_t['date'] = df_t['date'] + pd.offsets.MonthEnd(0)  # Set date to month-end

    # Clean column names
    df_t.columns = (
        df_t.columns
        .str.replace('-', '', regex=False)
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('%', 'percent')
        .str.lower()
    )

    # Add FY column and company name
    df_t = add_fy_quarter_column(df_t)
    df_t['company_name'] = file_name.split('.')[0]
    return df_t

# Extract and transform Balance Sheet data from Excel
def extract_bs(file_name):
    file_path = os.path.join(ini.raw_data_dir, file_name)
    df = pd.read_excel(file_path, sheet_name="balance_sheet")  # Read BS sheet
    df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
    df_t = df.transpose()
    df_t.columns = df_t.iloc[0]  # Set first row as header
    df_t = df_t.iloc[1:].reset_index().rename(columns={"index": "date"})

    df_t['date'] = pd.to_datetime(df_t['date'], format='%b-%y') + pd.offsets.MonthEnd(0)  # Convert to datetime

    # Clean and standardize column names
    df_t.columns = (
        df_t.columns
        .str.replace(r'[^\x00-\x7F]+', '', regex=True)  # Remove non-ASCII
        .str.replace('-', '', regex=False)
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('%', 'percent')
        .str.lower()
    )

    df_t = add_fy_quarter_column(df_t)  # Add financial year info
    df_t['company_name'] = file_name.split('.')[0]
    return df_t

# Main function to run the ETL process
def main():
    file_name = 'hdfcamc.xlsx'  # Name of the Excel file
    schema_name = 'financials'  # Target schema in database

    # Connect to PostgreSQL DB
    conn = psycopg2.connect(ini.dsn)

    # Create schema if not exists
    create_schema_if_not_exists(conn, schema_name)

    # Process Profit & Loss data
    pnl_df = extract_pnl(file_name)
    create_table_if_not_exists(conn, schema_name, 'pnl', pnl_df)
    insert_df_if_new(pnl_df, schema_name, 'pnl', conn)

    # Process Balance Sheet data
    bs_df = extract_bs(file_name)
    create_table_if_not_exists(conn, schema_name, 'bs', bs_df)
    insert_df_if_new(bs_df, schema_name, 'bs', conn)

    # Close DB connection
    conn.close()

    #Committing this

# Entry point for script
if __name__ == "__main__":
    main()