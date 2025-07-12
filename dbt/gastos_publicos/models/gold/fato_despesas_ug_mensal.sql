{{ config(
    materialized='table',
    unique_key='ug'
)}}

with base as (
    select * from {{ ref('stg_diarias_resumo') }}
),

agrupado as (
    select
        ug,
        descricao_ug,
        date_trunc('month', data_inicial) as mes,
        sum(total_empenhado) as total_empenhado,
        sum(total_liquidado) as total_liquidado,
        sum(total_pago) as total_pago
    from base
    group by 1, 2, 3
)

select * from agrupado
