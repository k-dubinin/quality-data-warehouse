INSERT INTO dwh.fact_quality (
    batch_key,
    product_key,
    factory_key,
    operator_key,
    inspector_key,
    defect_key,
    time_key,
    quality_score,
    defect_count,
    rework_required
)
SELECT
    b.batch_key,
    p.product_key,
    f.factory_key,
    o.operator_key,
    i.inspector_key,
    d.defect_key,
    t.time_key,
    r.quality_score,
    r.defect_count,
    r.rework_required
FROM stg.manufacturing_quality_raw r
JOIN dwh.dim_batch b
    ON r.batch_id = b.batch_id
JOIN dwh.dim_product p
    ON r.product_code = p.product_code
JOIN dwh.dim_factory f
    ON r.factory_location = f.factory_location
JOIN dwh.dim_operator o
    ON r.operator_id = o.operator_id
JOIN dwh.dim_inspector i
    ON r.inspector_id = i.inspector_id
LEFT JOIN dwh.dim_defect d
    ON r.defect_type = d.defect_type
   AND r.defect_severity = d.defect_severity
JOIN dwh.dim_time t
    ON t.date_value = r.inspection_date::DATE;
