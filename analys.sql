-- Сравнение месецов разных годов
SELECT date_part('month', date) as month,
       date_part('year', date) as year,
       MAX((max_temperature-32)*0.56)::numeric(10,2) as max_temperature,
       MIN((min_temperature-32)*0.56)::numeric(10,2) as min_temperature,
       MAX((max_temperature-32)*0.56)::numeric(10,2) - MIN((min_temperature-32)*0.56)::numeric(10,2) as raznica
FROM observ
WHERE date_part('month', date) IN ('6')
GROUP BY date_part('month', date), date_part('year', date)
ORDER BY date_part('month', date), date_part('year', date);

-- Сравнение конкретного месяца
SELECT date_part('day', date) as day,
       date_part('month', date) as month,
       date_part('year', date) as year,
       MAX((max_temperature-32)*0.56)::numeric(10,2) as max_temperature,
       MIN((min_temperature-32)*0.56)::numeric(10,2) as min_temperature,
       MAX((max_temperature-32)*0.56)::numeric(10,2) - MIN((min_temperature-32)*0.56)::numeric(10,2) as raznica,
       MIN((temperature-32)*0.56)::numeric(10,2) as temperature
FROM observ
WHERE date_part('month', date) IN ('6')
      AND date_part('day', date) IN ('10')
GROUP BY date_part('day', date), date_part('month', date), date_part('year', date)
ORDER BY date_part('day', date), date_part('month', date), date_part('year', date);

-- Количество дождливых дней за лето
SELECT date_part('year', date) as year,
       count(rain) as rain
FROM observ
WHERE date_part('month', date) IN ('6','7','8')
      AND rain = 't'
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);