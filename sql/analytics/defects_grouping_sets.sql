
-- Анализ количества дефектов:
-- 1) по типам дефектов,
-- 2) по производственным площадкам,
-- 3) по комбинации типа дефекта и площадки
-- с использованием GROUPING SETS

SELECT
    d.defect_type,
    fct.factory_location,
    SUM(f.defect_count) AS total_defects
FROM dwh.fact_quality f
LEFT JOIN dwh.dim_defect d ON f.defect_key = d.defect_key
JOIN dwh.dim_factory fct ON f.factory_key = fct.factory_key
GROUP BY GROUPING SETS (
    (d.defect_type),
    (fct.factory_location),
    (d.defect_type, fct.factory_location)
)
ORDER BY d.defect_type, fct.factory_location;