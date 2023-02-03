WITH top_consumers as (
    SELECT customer, sum(total) as total
    from app_deals_deals
    group by customer
    order by total DESC
    limit 5
),

top_gems as (
    select * from (
        select gem, count(customer) count_customer from (
            select deals.customer, deals.gem, count(deals.id) count_deals from app_deals_deals deals
            inner join top_consumers top on top.customer=deals.customer
            group by deals.customer, deals.gem
            order by deals.customer, deals.gem
        ) as unique_gems_for_top
        group by gem
    ) as t
    where t.count_customer >= 2
),

top_consumers_gems as (
select customer,
    array_agg(gem) as gems
from (

select
    deals.customer,
    deals.gem
from app_deals_deals as deals
    inner join top_consumers top_c on top_c.customer=deals.customer
    inner join top_gems   top_p on top_p.gem=deals.gem
group by
    deals.customer,
    deals.gem
order by
    deals.customer,
    deals.gem
    ) t
group by customer
)

select top.customer, top.total, info.gems from top_consumers top inner join top_consumers_gems info on top.customer=info.customer
order by top.total DESC
;


