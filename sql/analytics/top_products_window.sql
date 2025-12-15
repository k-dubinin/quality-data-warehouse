-- Определение трёх видов продукции с наибольшим суммарным количеством дефектов
-- с использованием агрегатных и оконных функций ранжирования

SELECT *
FROM (
    SELECT
        p.product_code,
        SUM(f.defect_count) AS total_defects,
        RANK() OVER (ORDER BY SUM(f.defect_count) DESC) AS defect_rank
    FROM dwh.fact_quality f
    JOIN dwh.dim_product p ON f.product_key = p.product_key
    GROUP BY p.product_code
) ranked
WHERE defect_rank <= 3;