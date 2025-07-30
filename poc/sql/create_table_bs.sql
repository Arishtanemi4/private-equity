-- Table: financials.bs

-- DROP TABLE IF EXISTS financials.bs;

CREATE TABLE IF NOT EXISTS financials.bs
(
    company_name text COLLATE pg_catalog."default" NOT NULL,
    date date NOT NULL,
    quarter integer,
    year integer,
    fy character varying(6) COLLATE pg_catalog."default" NOT NULL,
    equity_capital numeric,
    reserves numeric,
    borrowings numeric,
    other_liabilities numeric,
    trade_payables numeric,
    other_liability_items numeric,
    total_liabilities numeric,
    fixed_assets numeric,
    building numeric,
    equipments numeric,
    computers numeric,
    furniture_n_fittings numeric,
    vehicles numeric,
    intangible_assets numeric,
    other_fixed_assets numeric,
    gross_block numeric,
    accumulated_depreciation numeric,
    cwip numeric,
    investments numeric,
    other_assets numeric,
    trade_receivables numeric,
    receivables_over_6m numeric,
    receivables_under_6m numeric,
    cash_equivalents numeric,
    loans_n_advances numeric,
    other_asset_items numeric,
    total_assets numeric,
    CONSTRAINT bs_pkey PRIMARY KEY (company_name, date, fy)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS financials.bs
    OWNER to postgres;
-- Index: idx_bs_company_name_fy

-- DROP INDEX IF EXISTS financials.idx_bs_company_name_fy;

CREATE INDEX IF NOT EXISTS idx_bs_company_name_fy
    ON financials.bs USING btree
    (company_name COLLATE pg_catalog."default" ASC NULLS LAST, fy COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_bs_fy_company_name

-- DROP INDEX IF EXISTS financials.idx_bs_fy_company_name;

CREATE INDEX IF NOT EXISTS idx_bs_fy_company_name
    ON financials.bs USING btree
    (fy COLLATE pg_catalog."default" ASC NULLS LAST, company_name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;