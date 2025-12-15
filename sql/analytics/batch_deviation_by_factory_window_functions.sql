-- Анализ отклонений показателей качества отдельных партий продукции
-- от среднего уровня качества по соответствующей производственной площадке
-- с использованием оконных функций 

SELECT
    ROW_NUMBER() OVER (
        PARTITION BY fct.factory_location
        ORDER BY f.quality_score DESC
    ) AS batch_number,
    b.batch_id,
    fct.factory_location,
    f.quality_score,
    ROUND(
        AVG(f.quality_score) OVER (PARTITION BY fct.factory_location),
        2
    ) AS avg_factory_quality,
    ROUND(
        f.quality_score
        - AVG(f.quality_score) OVER (PARTITION BY fct.factory_location),
        2
    ) AS deviation_from_avg
FROM dwh.fact_quality f
JOIN dwh.dim_factory fct ON f.factory_key = fct.factory_key
JOIN dwh.dim_batch b ON f.batch_key = b.batch_key
ORDER BY
    fct.factory_location,
    batch_number;