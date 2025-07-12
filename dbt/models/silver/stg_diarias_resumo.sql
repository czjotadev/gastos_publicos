{{ config(
    alias='stg_diarias_resumo',
    materialized='table',
    unique_key='ug',
    schema='silver'
)}}

with base as (
    select *
    from gastos_publicos_bronze.diarias_resumo
),

formatado as (
    select
        ug,
        descricao_ug,
        to_date(data_inicial, 'DD/MM/YYYY') as data_inicial,
        to_date(data_final, 'DD/MM/YYYY') as data_final,
        replace(replace(total_empenhado, '.', ''), ',', '.') as total_empenhado,
        replace(replace(total_liquidado, '.', ''), ',', '.') as total_liquidado,
        replace(replace(total_pago, '.', ''), ',', '.') as total_pago
    from base
)

select * from formatado