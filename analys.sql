-- Сравнение месецов разных годов
SELECT date_part('month', date) as month,
       date_part('year', date) as year,
       MAX((max_temperature-32)*0.56)::numeric(10,2) as max_temperature,
       MIN((min_temperature-32)*0.56)::numeric(10,2) as min_temperature,
       MAX((max_temperature-32)*0.56)::numeric(10,2) - MIN((min_temperature-32)*0.56)::numeric(10,2) as raznica
FROM temperature
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
FROM temperature
WHERE date_part('month', date) IN ('6')
      AND date_part('day', date) IN ('10')
GROUP BY date_part('day', date), date_part('month', date), date_part('year', date)
ORDER BY date_part('day', date), date_part('month', date), date_part('year', date);

-- Количество дождливых дней за лето
SELECT date_part('year', date) as year,
       count(rain) as rain
FROM temperature
WHERE date_part('month', date) IN ('6','7','8')
      AND rain = 't'
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество теплых дней за лето по годам
SELECT date_part('year', date) as year,
       count(*) as hot_days
FROM temperature
WHERE date_part('month', date) IN ('6','7','8')
      AND  temperature > 23
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество холодных дней за лето по годам
SELECT date_part('year', date) as year,
       count(*) as hot_days
FROM temperature
WHERE date_part('month', date) IN ('6','7','8')
      AND temperature < 18
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество холодных и дождливых дней за лето
SELECT date_part('year', date) as year,
       count(*) as hot_rain_days
FROM temperature
WHERE date_part('month', date) IN ('6','7','8')
      AND (temperature-32)*0.56::numeric(10,2) < 18
      AND rain = TRUE
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество дней лета по годам
SELECT date_part('year', date) as year,
       count(*) as days
FROM temperature
WHERE date_part('month', date) IN ('6','7','8')
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Все дни лета 2019
SELECT *
FROM temperature
WHERE date_part('month', date) IN ('6','7','8')
    AND date_part('year', date) IN ('2019')
ORDER BY date;

-- Удалить все данные по лету 2019
DELETE FROM temperature
WHERE date >= '2019-06-01'

-- Дней в таблице
SELECT count(*) FROM temperature;

-- Погода за один конкретный день
SELECT *
FROM temperature
WHERE date = '2019-06-13'

-- Количетсво дней по годам
SELECT date_part('year', date) as year, count(*)
FROM temperature
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

SELECT *
FROM temperature;

-- Поиск дней в которые нет записей
SELECT d.date::date, t.temperature
from generate_series(date '2005-02-01',
                       date '2019-09-05',
                       interval '1 day') as d
LEFT JOIN temperature as t
ON d.date = t.date
WHERE t.temperature IS NULL;

-- Дополняем данные которых не хватает
INSERT INTO temperature (date, temperature)
values ('2005-02-07', -8.4),
('2005-07-19', 18),
('2005-07-25', 25),
('2005-09-07', 18.6),
('2008-02-13', -5.15),
('2008-05-06', 21.1),
('2008-06-11', 22.1),
('2008-06-17', 18.95),
('2008-06-28', 18.95),
('2008-07-05', 22.1),
('2009-07-24', 22.9),
('2009-09-30', 6.85),
('2009-12-21', -7.25),
('2011-07-31', 24.9),
('2012-12-16', -15.1)
ON CONFLICT DO NOTHING;