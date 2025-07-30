-- Table: financials.pnl

-- DROP TABLE IF EXISTS financials.pnl;

CREATE TABLE IF NOT EXISTS financials.pnl
(
    company_name text COLLATE pg_catalog."default" NOT NULL,
    date date NOT NULL,
    quarter integer,
    year integer,
    fy character varying(6) COLLATE pg_catalog."default" NOT NULL,
    sales numeric,
    sales_growth_percent numeric,
    expenses numeric,
    manufacturing_cost_percent numeric,
    employee_cost_percent numeric,
    other_cost_percent numeric,
    operating_profit numeric,
    opm_percent numeric,
    other_income numeric,
    exceptional_items numeric,
    other_income_normal numeric,
    interest numeric,
    depreciation numeric,
    profit_before_tax numeric,
    tax_percent numeric,
    net_profit numeric,
    exceptional_items_at numeric,
    profit_excl_excep numeric,
    profit_for_pe numeric,
    profit_for_eps numeric,
    eps_in_rs numeric,
    dividend_payout_percent numeric,
    CONSTRAINT pnl_pkey PRIMARY KEY (company_name, date, fy)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS financials.pnl
    OWNER to postgres;
-- Index: idx_pnl_company_name_fy

-- DROP INDEX IF EXISTS financials.idx_pnl_company_name_fy;

CREATE INDEX IF NOT EXISTS idx_pnl_company_name_fy
    ON financials.pnl USING btree
    (company_name COLLATE pg_catalog."default" ASC NULLS LAST, fy COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_pnl_fy_company_name

-- DROP INDEX IF EXISTS financials.idx_pnl_fy_company_name;

CREATE INDEX IF NOT EXISTS idx_pnl_fy_company_name
    ON financials.pnl USING btree
    (fy COLLATE pg_catalog."default" ASC NULLS LAST, company_name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;