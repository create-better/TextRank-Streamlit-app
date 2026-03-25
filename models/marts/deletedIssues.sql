{{ config(materialized='table') }}

with deletedJira as (
    select * from {{ ref('stg_dbt_deletedIssues') }}
),

orders as (
    select issuekey as ikey
    from {{ ref('stg_dbt_deletedIssues') }}
)


select *
from deletedJira