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

-- Количество теплых дней за лето
SELECT date_part('year', date) as year,
       count(*) as hot_days
FROM observ
WHERE date_part('month', date) IN ('6','7','8')
      AND (temperature-32)*0.56::numeric(10,2) > 23
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество холодных дней за лето
SELECT date_part('year', date) as year,
       count(*) as hot_days
FROM observ
WHERE date_part('month', date) IN ('6','7','8')
      AND (temperature-32)*0.56::numeric(10,2) < 18
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество холодных и дождливых дней за лето
SELECT date_part('year', date) as year,
       count(*) as hot_rain_days
FROM observ
WHERE date_part('month', date) IN ('6','7','8')
      AND (temperature-32)*0.56::numeric(10,2) < 18
      AND rain = TRUE
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество дней лета по годам
SELECT date_part('year', date) as year,
       count(*) as days
FROM observ
--WHERE date_part('month', date) IN ('6','7','8')
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Все дни лета 2019
SELECT *
FROM observ
WHERE date_part('month', date) IN ('6','7','8')
    AND date_part('year', date) IN ('2019')
ORDER BY date;

-- Удалить все данные по лету 2019
DELETE FROM observ
WHERE date >= '2019-06-01'

-- Добавить проверку на уникальность даты
ALTER TABLE observ ADD PRIMARY KEY (date);

-- Дней в таблице
SELECT count(*) FROM temperature;

-- Погода за один конкретный день
SELECT *
FROM observ
WHERE date = '2019-06-13'

-- Количетсво дней по годам
SELECT date_part('year', date) as year, count(*)
FROM temperature
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);

-- Количество летних дней по годам
SELECT date_part('year', date) as year, count(*)
FROM temperature
WHERE date_part ('month', date) IN ('6', '7', '8')
GROUP BY date_part('year', date)
ORDER BY date_part('year', date);