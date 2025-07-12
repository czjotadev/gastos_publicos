{{ config(
    materialized='table',
    unique_key='codigo_favorecido'
)}}

with base as (
    select * from {{ ref('stg_diarias_favorecidos') }}
),

agrupado as (
    select
        codigo_favorecido,
        nome_favorecido,
        ug,
        date_trunc('month', data_inicial) as mes,
        sum(total_empenhado) as total_empenhado,
        sum(total_liquidado) as total_liquidado,
        sum(total_pago) as total_pago
    from base
    group by 1, 2, 3, 4
)

select * from agrupado
