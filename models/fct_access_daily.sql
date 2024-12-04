select
    1 as access_daily_key,
    20240901 as date_key,
    1 as product_key,
    date('2024-09-01') as snapshot_date,
    100 as session
union all
select 2, 20240901, 2, date('2024-09-01'), 200
union all
select 3, 20240902, 1, date('2024-09-02'), 112
union all
select 4, 20240902, 2, date('2024-09-02'), 195
union all
select 5, 20240903, 1, date('2024-09-03'), 118
union all
select 6, 20240903, 2, date('2024-09-03'), 203