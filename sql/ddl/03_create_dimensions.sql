CREATE TABLE dwh.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_code TEXT UNIQUE
);

CREATE TABLE dwh.dim_factory (
    factory_key SERIAL PRIMARY KEY,
    factory_location TEXT UNIQUE
);

CREATE TABLE dwh.dim_operator (
    operator_key SERIAL PRIMARY KEY,
    operator_id TEXT UNIQUE
);

CREATE TABLE dwh.dim_inspector (
    inspector_key SERIAL PRIMARY KEY,
    inspector_id TEXT UNIQUE
);

CREATE TABLE dwh.dim_defect (
    defect_key SERIAL PRIMARY KEY,
    defect_type TEXT,
    defect_severity INT
);

CREATE TABLE dwh.dim_batch (
    batch_key SERIAL PRIMARY KEY,
    batch_id TEXT UNIQUE,
    production_date DATE,
    product_key INT REFERENCES dwh.dim_product(product_key)
);
