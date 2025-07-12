{{ config(
    alias='stg_diarias_favorecidos',
    materialized='table',
    unique_key='codigo_favorecido',
    schema='silver'
)}}

with base as (
    select *
    from gastos_publicos_bronze.diarias_favorecidos
),

formatado as (
    select
        ug,
        codigo_favorecido,
        nome_favorecido,
        to_date(data_inicial, 'DD/MM/YYYY') as data_inicial,
        to_date(data_final, 'DD/MM/YYYY') as data_final,
        replace(replace(total_empenhado, '.', ''), ',', '.') as total_empenhado,
        replace(replace(total_liquidado, '.', ''), ',', '.') as total_liquidado,
        replace(replace(total_pago, '.', ''), ',', '.') as total_pago
    from base
)

select * from formatado
