import os
import psycopg2
import pandas as pd
import __init__ as ini


def add_fy_quarter_column(df: pd.Series, date_col='date', new_col='fy'):
    dates = pd.to_datetime(df[date_col])
    
    quarters = pd.Series(index=dates.index, dtype="object")
    fy_years = pd.Series(index=dates.index, dtype="int")

    quarters[dates.dt.month.isin([4, 5, 6])] = '1'
    fy_years[dates.dt.month.isin([4, 5, 6])] = dates.dt.year + 1     # Add 1 year for Indian FY

    quarters[dates.dt.month.isin([7, 8, 9])] = '2'
    fy_years[dates.dt.month.isin([7, 8, 9])] = dates.dt.year + 1     # Add 1 year for Indian FY

    quarters[dates.dt.month.isin([10, 11, 12])] = '3'
    fy_years[dates.dt.month.isin([10, 11, 12])] = dates.dt.year + 1  # Add 1 year for Indian FY

    quarters[dates.dt.month.isin([1, 2, 3])] = '4'
    fy_years[dates.dt.month.isin([1, 2, 3])] = dates.dt.year         # Last Quarter stays in same year

    fy_years = fy_years.astype('Int16')                              # Changing datatype from float to int for easier extraction of year

    df[new_col] = 'Q' + quarters + 'FY' + fy_years.astype(str).str[-2:]    # Extracting last 2 digits from year
    df['quarter'] = quarters
    df['year'] = fy_years

    return df


def extract_financials(file_name: str, financials: str):
    '''
        Extract Data from excel file and convert into a celan DataFrame.
    '''
    file_financials = os.path.join(ini.raw_data_dir, file_name)
    df = pd.read_excel(file_financials, sheet_name=financials)
    df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)

    dft = df.transpose()                                    # Transpose the Table for horizontal format
    dft.columns = dft.iloc[0]                               # The column name i.e. the mertices are in the first row
    dft = dft.iloc[1:]                                      # Dropping the first row
    dft = dft.reset_index()                                 # Date is in the index
    dft.rename(columns={"index": "Date"}, inplace=True)     # renaming the new columna as Date

    # The date is converted incorrectly from the excel sheet as start of the month instead of end of the month
    # The format of dates in Excel is Mar-14
    dft['Date'] = dft['Date'] + pd.offsets.MonthEnd(0)      # Setting 0 as parameter ensures that the date does not move to next month incase the date already is end of month

    dft.columns = (
        dft.columns
        .str.replace('-', '', regex=False)                  # 1. Remove all hyphens
        .str.strip()                                        # 2. Strip trailing/leading spaces
        .str.replace(' ', '_')                              # 3. Replace spaces with underscores
        .str.replace('%', 'percent')                        # 4. Replace % with percent
        .str.lower()                                        # 5. Lower the column names
    )

    dft = add_fy_quarter_column(dft)                        # Adding fy column

    company_name = file_name.split('.')[0]                  # Fetching company_name from file_name
    dft['company_name'] = company_name                      # Assigning company_name to all rows of dataframe

    return dft


def insert_df_with_executemany(df: pd.Series, schema_name: str, table_name: str, conn_params: str):
    '''
        DataFrame and SQL Table should contain the same columns
        Dynamic sql insertion function
    '''
    conn = psycopg2.connect(conn_params)
    cursor = conn.cursor()

    columns = ', '.join(df.columns)                         # Comma seperated columns for SQL insertion
    placeholders = ', '.join(['%s'] * len(df.columns))      # Placeholder (%s) matching number of columns
    insert_query = f"""
        INSERT INTO {schema_name}.{table_name}
        ({columns}) VALUES ({placeholders})
        ON CONFLICT (company_name, date, fy) DO NOTHING
    """                                                     # Dynamic SQL insert query

    print("Insert query generated")
    print(insert_query)

    data = [tuple(row) for row in df.to_numpy()]
    cursor.executemany(insert_query, data)

    conn.commit()
    cursor.close()
    conn.close()

    return print("Data inserted using executemany.")


def main():
    file_name = 'hdfcamc.xlsx'

    pnl = extract_financials(file_name, financials='profit_loss')
    insert_df_with_executemany(pnl, schema_name='financials', table_name='pnl', conn_params=ini.dsn)

    bs = extract_financials(file_name, financials='balance_sheet')
    insert_df_with_executemany(bs, schema_name='financials', table_name='bs', conn_params=ini.dsn)

    cf = extract_financials(file_name, financials='cash_flow')
    insert_df_with_executemany(cf, schema_name='financials', table_name='cf', conn_params=ini.dsn)


if __name__ == "__main__":
    main()