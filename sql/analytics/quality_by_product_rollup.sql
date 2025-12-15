-- Анализ среднего уровня качества продукции по каждому виду изделия,
-- а также расчёт общего среднего показателя по всем продуктам
-- с использованием оператора ROLLUP

SELECT
    CASE 
        WHEN GROUPING(p.product_code) = 1 THEN 'TOTAL'
        ELSE p.product_code 
    END AS product_code,
    ROUND(AVG(f.quality_score), 2) AS avg_quality_score,
    COUNT(*) AS inspections_count
FROM dwh.fact_quality f
JOIN dwh.dim_product p ON f.product_key = p.product_key
GROUP BY ROLLUP (p.product_code)
ORDER BY 
    GROUPING(p.product_code),
    p.product_code;
