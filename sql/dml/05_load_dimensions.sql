
-- PRODUCT
INSERT INTO dwh.dim_product (product_code)
SELECT DISTINCT product_code
FROM stg.manufacturing_quality_raw
WHERE product_code IS NOT NULL
ON CONFLICT (product_code) DO NOTHING;

-- FACTORY
INSERT INTO dwh.dim_factory (factory_location)
SELECT DISTINCT factory_location
FROM stg.manufacturing_quality_raw
WHERE factory_location IS NOT NULL
ON CONFLICT (factory_location) DO NOTHING;

-- OPERATOR
INSERT INTO dwh.dim_operator (operator_id)
SELECT DISTINCT operator_id
FROM stg.manufacturing_quality_raw
WHERE operator_id IS NOT NULL
ON CONFLICT (operator_id) DO NOTHING;

-- INSPECTOR
INSERT INTO dwh.dim_inspector (inspector_id)
SELECT DISTINCT inspector_id
FROM stg.manufacturing_quality_raw
WHERE inspector_id IS NOT NULL
ON CONFLICT (inspector_id) DO NOTHING;

-- DEFECT
INSERT INTO dwh.dim_defect (defect_type, defect_severity)
SELECT DISTINCT defect_type, defect_severity
FROM stg.manufacturing_quality_raw
WHERE defect_type IS NOT NULL
ON CONFLICT DO NOTHING;

-- BATCH
INSERT INTO dwh.dim_batch (batch_id, production_date, product_key)
SELECT DISTINCT
    r.batch_id,
    r.production_date,
    p.product_key
FROM stg.manufacturing_quality_raw r
JOIN dwh.dim_product p
    ON r.product_code = p.product_code
ON CONFLICT (batch_id) DO NOTHING;
