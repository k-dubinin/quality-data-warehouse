-- Многомерный анализ среднего уровня качества продукции
-- по годам и производственным площадкам
-- с использованием оператора CUBE (только полные группировки)

SELECT
    t.year,
    fct.factory_location,
    ROUND(AVG(f.quality_score), 2) AS avg_quality,
    COUNT(*) AS records_count
FROM dwh.fact_quality f
JOIN dwh.dim_time t ON f.time_key = t.time_key
JOIN dwh.dim_factory fct ON f.factory_key = fct.factory_key
GROUP BY CUBE (t.year, fct.factory_location)
HAVING t.year IS NOT NULL AND fct.factory_location IS NOT NULL
ORDER BY t.year, fct.factory_location;