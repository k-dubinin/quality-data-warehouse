CREATE TABLE stg.manufacturing_quality_raw (
    batch_id            TEXT,
    production_date     DATE,
    product_code        TEXT,
    shift               TEXT,
    operator_id         TEXT,
    inspection_id       TEXT,
    inspection_date     TIMESTAMP,
    inspector_id        TEXT,
    quality_score       NUMERIC(5,2),
    defect_type         TEXT,
    defect_severity     INT,
    defect_count        INT,
    rework_required     BOOLEAN,
    comments            TEXT,
    factory_location    TEXT,
    load_dt             TIMESTAMP DEFAULT now()
);
