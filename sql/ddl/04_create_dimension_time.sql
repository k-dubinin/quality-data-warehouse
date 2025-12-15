CREATE TABLE IF NOT EXISTS dwh.dim_time (
    time_key    INT PRIMARY KEY,
    date_value  DATE,
    year        INT,
    quarter     INT,
    month       INT,
    day         INT,
    weekday     INT,
    is_weekend  BOOLEAN
);

INSERT INTO dwh.dim_time
SELECT
    to_char(d, 'YYYYMMDD')::INT,
    d,
    EXTRACT(YEAR FROM d),
    EXTRACT(QUARTER FROM d),
    EXTRACT(MONTH FROM d),
    EXTRACT(DAY FROM d),
    EXTRACT(ISODOW FROM d),
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6,7) THEN TRUE ELSE FALSE END
FROM generate_series('2023-01-01'::date, '2025-12-31'::date, '1 day'::interval) d;