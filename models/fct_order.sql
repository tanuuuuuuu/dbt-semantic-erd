select
    1 as order_key,
    20240901 as order_date_key,
    20240901 as first_order_date_key,
    1 as product_key,
    1 as user_key,
    "ODR001" as order_id,
    1 as order_item_no,
    datetime('2024-09-01T00:00:00') as order_date,
    5000 as item_price,
union all
select 2, 20240901, 20240901, 2, 1, "ODR001", 2, datetime('2024-09-01T00:00:00'), 7000
union all
select 3, 20240901, 20240901, 1, 2, "ODR002", 1, datetime('2024-09-01T12:00:00'), 5000
union all
select 4, 20240903, 20240903, 2, 3, "ODR003", 1, datetime('2024-09-03T01:00:00'), 7000
union all
select 5, 20240903, 20240901, 1, 1, "ODR004", 1, datetime('2024-09-03T04:00:00'), 5000