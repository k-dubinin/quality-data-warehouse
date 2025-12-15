CREATE TABLE dwh.fact_quality (
    fact_id SERIAL PRIMARY KEY,

    batch_key      INT REFERENCES dwh.dim_batch(batch_key),
    product_key    INT REFERENCES dwh.dim_product(product_key),
    factory_key    INT REFERENCES dwh.dim_factory(factory_key),
    operator_key   INT REFERENCES dwh.dim_operator(operator_key),
    inspector_key  INT REFERENCES dwh.dim_inspector(inspector_key),
    defect_key     INT REFERENCES dwh.dim_defect(defect_key),
    time_key       INT REFERENCES dwh.dim_time(time_key),

    quality_score  NUMERIC(5,2),
    defect_count   INT,
    rework_required BOOLEAN
);
