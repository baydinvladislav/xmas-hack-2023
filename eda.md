# EDA
1. [Total movements by hours/weeks within a time range](#total-movements-by-hoursweeks-within-a-time-range)
2. [Total movements within a time range in a single table](#total-movements-within-a-time-range-in-a-single-table)
3. [Busiest router at a specific hour](#busiest-router-at-a-specific-hour)
4. [Busiest hour by connections](#busiest-hour-by-connections)
5. [Rating of the busiest hours by connections](#rating-of-the-busiest-hours-by-connections)
6. [Rating of the most moving users](#rating-of-the-most-moving-users)
7. [Rating of routers that caught the most users](#rating-of-routers-that-caught-the-most-users)
8. [Which router caught the most users at a specific hour](#which-router-caught-the-most-users-at-a-specific-hour)
9. [Average signal strength for each hour of each router](#average-signal-strength-for-each-hour-of-each-router)
10. [How many times routers caught their "favorite" users](#how-many-times-routers-caught-their-favorite-users)
11. [Which day was the busiest each week with the number of connections](#which-day-was-the-busiest-each-week-with-the-number-of-connections)
12. [Statistics of caught unique users for specified router in each hour of the day](#statistics-of-caught-unique-users-for-specified-router-in-each-hour-of-the-day)
13. [Number of movements for each week](#number-of-movements-for-each-week)
14. [Identification of peak hours](#identification-of-peak-hours)
15. [Identification of the most unloaded hours](#identification-of-the-most-unloaded-hours)
16. [Routers with the most unfavorable positions](#routers-with-the-most-unfavorable-positions)
17. [Get three key time intervals](#get-three-key-time-intervals)


## Total movements by hours/weeks within a time range
``` 
SELECT
    EXTRACT(WEEK FROM tm) AS week_number,
    COUNT(*) AS movement_count
FROM
    wifi_logs
WHERE
    EXTRACT(HOUR FROM tm) BETWEEN 6 AND 11
GROUP BY
    week_number
ORDER BY
    week_number;
```

## Total movements within a time range in a single table
```
SELECT
    EXTRACT(WEEK FROM tm) AS week_number,
    COUNT(*) AS total_movements,
    COUNT(CASE WHEN EXTRACT(HOUR FROM tm) BETWEEN 6 AND 11 THEN 1 END) AS movements_6_11,
    COUNT(CASE WHEN EXTRACT(HOUR FROM tm) BETWEEN 11 AND 17 THEN 1 END) AS movements_11_17,
    COUNT(CASE WHEN EXTRACT(HOUR FROM tm) BETWEEN 17 AND 23 THEN 1 END) AS movements_17_23
FROM
    wifi_logs
GROUP BY
    week_number
ORDER BY
    week_number;
```

## Busiest router at a specific hour
```
SELECT
    router_id,
    COUNT(*) AS connection_count
FROM
    wifi_logs
WHERE
    EXTRACT(HOUR FROM tm) = 9
GROUP BY
    router_id
ORDER BY
    connection_count DESC
LIMIT 1;
```

## Busiest hour by connections
```
SELECT
    EXTRACT(HOUR FROM tm) AS hour_of_day,
    COUNT(*) AS total_connections
FROM
    wifi_logs
GROUP BY
    hour_of_day
ORDER BY
    total_connections DESC
LIMIT 1;
```

## Rating of the busiest hours by connections | used
```
WITH HourlyConnectionCounts AS (
    SELECT
        EXTRACT(HOUR FROM tm) AS hour_of_day,
        COUNT(*) AS total_connections
    FROM
        wifi_logs
    GROUP BY
        hour_of_day
)
SELECT
    hour_of_day,
    total_connections,
    RANK() OVER (ORDER BY total_connections DESC) AS hour_rank
FROM
    HourlyConnectionCounts;
```

## Rating of the most moving users | unnecessary
```
SELECT
    user_mac,
    COUNT(*) AS catch_count,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS user_rank
FROM
    wifi_logs
GROUP BY
    user_mac
ORDER BY
    catch_count DESC;
```

## Rating of routers that caught the most users
```
SELECT
    router_id,
    COUNT(DISTINCT user_mac) AS unique_users_count,
    RANK() OVER (ORDER BY COUNT(DISTINCT user_mac) DESC) AS router_rank
FROM
    wifi_logs
GROUP BY
    router_id
ORDER BY
    unique_users_count DESC;
```

## Which router caught the most users at a specific hour - used
```
WITH RouterUserCounts AS (
    SELECT
        router_id,
        EXTRACT(HOUR FROM tm) AS hour_of_day,
        COUNT(DISTINCT user_mac) AS unique_users_count
    FROM
        wifi_logs
    GROUP BY
        router_id, hour_of_day
)
SELECT
    router_id,
    hour_of_day,
    MAX(unique_users_count) AS max_users_count
FROM
    RouterUserCounts
GROUP BY
    router_id, hour_of_day
ORDER BY
    max_users_count DESC
LIMIT 1;
```

## Average signal strength for each hour of each router - after
```
SELECT
    router_id,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 0 THEN signal END) AS signal_0,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 1 THEN signal END) AS signal_1,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 2 THEN signal END) AS signal_2,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 3 THEN signal END) AS signal_3,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 4 THEN signal END) AS signal_4,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 5 THEN signal END) AS signal_5,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 6 THEN signal END) AS signal_6,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 7 THEN signal END) AS signal_7,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 8 THEN signal END) AS signal_8,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 9 THEN signal END) AS signal_9,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 10 THEN signal END) AS signal_10,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 11 THEN signal END) AS signal_11,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 12 THEN signal END) AS signal_12,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 13 THEN signal END) AS signal_13,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 14 THEN signal END) AS signal_14,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 15 THEN signal END) AS signal_15,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 16 THEN signal END) AS signal_16,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 17 THEN signal END) AS signal_17,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 18 THEN signal END) AS signal_18,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 19 THEN signal END) AS signal_19,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 20 THEN signal END) AS signal_20,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 21 THEN signal END) AS signal_21,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 22 THEN signal END) AS signal_22,
    AVG(CASE WHEN EXTRACT(HOUR FROM tm) = 23 THEN signal END) AS signal_23
FROM
    wifi_logs
WHERE
    EXTRACT(HOUR FROM tm) BETWEEN 0 AND 23
GROUP BY
    router_id
ORDER BY
    router_id;
```

## How many times routers caught their "favorite" users
```
WITH RouterUserCounts AS (
    SELECT
        router_id,
        user_mac,
        COUNT(*) AS catch_count
    FROM
        wifi_logs
    GROUP BY
        router_id, user_mac
),
RankedUsers AS (
    SELECT
        router_id,
        user_mac,
        catch_count,
        RANK() OVER (PARTITION BY router_id ORDER BY catch_count DESC) AS user_rank
    FROM
        RouterUserCounts
)
SELECT
    ru.router_id,
    ru.user_mac,
    ru.catch_count
FROM
    RankedUsers ru
WHERE
    ru.user_rank = 1
ORDER BY
    ru.catch_count DESC;
```

## Which day was the busiest each week with the number of connections
```
WITH WeeklyTopDay AS (
    SELECT
        EXTRACT(WEEK FROM tm) AS week_number,
        tm::date AS date,
        COUNT(*) AS connection_count,
        RANK() OVER (PARTITION BY EXTRACT(WEEK FROM tm) ORDER BY COUNT(*) DESC) AS day_rank
    FROM
        wifi_logs
    GROUP BY
        week_number, date
)
SELECT
    wtd.week_number,
    wtd.date,
    TO_CHAR(wtd.date, 'Day') AS day_name,
    wtd.connection_count
FROM
    WeeklyTopDay wtd
WHERE
    wtd.day_rank = 1
ORDER BY
    wtd.week_number;
```

## Statistics of caught unique users for specified router in each hour of the day
```
SELECT
    EXTRACT(HOUR FROM tm) AS hour_of_day,
    COUNT(DISTINCT user_mac) AS unique_users_count
FROM
    wifi_logs
WHERE
    router_id = '090a6502-bfc4-4d39-bc94-b0519fee04d6'
GROUP BY
    hour_of_day
ORDER BY
    hour_of_day;
```

## Number of movements for each week
```
SELECT
    EXTRACT(WEEK FROM tm) AS week_number,
    COUNT(*) AS movement_count
FROM
    wifi_logs
GROUP BY
    week_number
ORDER BY
    week_number;
```

## Identification of peak hours
```
-- top_loaded_hours_in_year_diagram.png
WITH HourlyUserCounts AS (
    SELECT
        EXTRACT(HOUR FROM tm) AS hour_of_day,
        router_id,
        COUNT(DISTINCT user_mac) AS users_count
    FROM
        wifi_logs
    GROUP BY
        hour_of_day, router_id
)
SELECT
    hour_of_day,
    AVG(users_count) AS avg_users_count
FROM
    HourlyUserCounts
GROUP BY
    hour_of_day
ORDER BY
    avg_users_count DESC;
```

## Identification of the most unloaded hours
```
-- top_loaded_hours_in_year_diagram.png
WITH HourlyUserCounts AS (
    SELECT
        EXTRACT(HOUR FROM tm) AS hour_of_day,
        COUNT(DISTINCT user_mac) AS users_count
    FROM
        wifi_logs
    GROUP BY
        hour_of_day
)
SELECT
    hour_of_day,
    AVG(users_count) AS avg_users_count
FROM
    HourlyUserCounts
GROUP BY
    hour_of_day
ORDER BY
    avg_users_count ASC;

```

## Routers with the most unfavorable positions
```
WITH HourlyUserCounts AS (
    SELECT
        EXTRACT(HOUR FROM tm) AS hour_of_day,
        COUNT(DISTINCT user_mac) AS users_count
    FROM
        wifi_logs
    GROUP BY
        hour_of_day
)
SELECT
    hour_of_day,
    AVG(users_count) AS avg_users_count
FROM
    HourlyUserCounts
GROUP BY
    hour_of_day
ORDER BY
    avg_users_count ASC;
```

## Get three key time intervals
```
-- afternoon_hours_52_week_diagram.png
-- evening_hours_52_week_diagram.png
-- morning_hours_52_week_diagram.png
WITH router_movement_counts AS (
  SELECT
    EXTRACT(WEEK FROM tm) AS week_number,
    router_id,
    COUNT(*) AS movement_count,
    RANK() OVER (PARTITION BY EXTRACT(WEEK FROM tm) ORDER BY COUNT(*) DESC) AS rank_in_week
  FROM
    wifi_logs
  WHERE
    EXTRACT(HOUR FROM tm) BETWEEN 6 AND 11
  GROUP BY
    week_number, router_id
)

SELECT
  week_number,
  router_id,
  movement_count
FROM
  router_movement_counts
WHERE
  rank_in_week = 1
ORDER BY
  movement_count DESC;
```
