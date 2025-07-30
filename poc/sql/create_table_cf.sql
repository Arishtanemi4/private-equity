-- Table: financials.cf

-- DROP TABLE IF EXISTS financials.cf;

CREATE TABLE IF NOT EXISTS financials.cf
(
    company_name text COLLATE pg_catalog."default" NOT NULL,
    date date NOT NULL,
    quarter integer,
    year integer,
    fy character varying(6) COLLATE pg_catalog."default" NOT NULL,
    cash_from_operating_activity numeric,
    profit_from_operations numeric,
    receivables numeric,
    payables numeric,
    loans_advances numeric,
    other_wc_items numeric,
    working_capital_changes numeric,
    direct_taxes numeric,
    cash_from_investing_activity numeric,
    fixed_assets_purchased numeric,
    fixed_assets_sold numeric,
    investments_purchased numeric,
    investments_sold numeric,
    interest_received numeric,
    dividends_received numeric,
    invest_in_subsidiaries numeric,
    other_investing_items numeric,
    cash_from_financing_activity numeric,
    proceeds_from_shares numeric,
    interest_paid_fin numeric,
    dividends_paid numeric,
    financial_liabilities numeric,
    share_application_money numeric,
    application_money_refund numeric,
    other_financing_items numeric,
    net_cash_flow numeric,
    CONSTRAINT cf_pkey PRIMARY KEY (company_name, date, fy)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS financials.cf
    OWNER to postgres;
-- Index: idx_cf_company_name_fy

-- DROP INDEX IF EXISTS financials.idx_cf_company_name_fy;

CREATE INDEX IF NOT EXISTS idx_cf_company_name_fy
    ON financials.cf USING btree
    (company_name COLLATE pg_catalog."default" ASC NULLS LAST, fy COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_cf_fy_company_name

-- DROP INDEX IF EXISTS financials.idx_cf_fy_company_name;

CREATE INDEX IF NOT EXISTS idx_cf_fy_company_name
    ON financials.cf USING btree
    (fy COLLATE pg_catalog."default" ASC NULLS LAST, company_name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;