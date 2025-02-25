SELECT * FROM agriculture.agri_data;

-- Top 7 Rice Production by State --
select state_name,round(sum(rice_production)) as rice_production from agri_data
group by state_name
order by rice_production desc
limit 7;


-- Top 5 Wheat Producing States -- 
select state_name,round(sum(wheat_production)) as wheat_production from agri_data
group by state_name
order by wheat_production desc
limit 5;


-- Top 5 Oil Seed Production By State --
select state_name,round(sum(oilseeds_production)) as oilseeds_production from agri_data
group by state_name
order by oilseeds_production desc
limit 5;


-- Top 7 Sunflower Production By State --
select state_name,round(sum(sunflower_production)) as sunflower_production from agri_data
group by state_name
order by sunflower_production desc
limit 7;


-- India Sugasugarcane Production from last 50 years --
select year,round(sum(sugarcane_production)) sugarcane_production from agri_data
group by year
order by year desc
limit 50;


-- Rice Production vs Wheat Production last 50 years --
select year,round(sum(rice_production)) as rice_production,round(sum(wheat_production)) as wheat_production from agri_data
group by year
order by year desc
limit 50;


-- Rice Production by west bengal district --
select state_name,round(sum(rice_production)) as rice_production from agri_data where state_name = "west bengal"
group by state_name
order by rice_production desc;


-- Top 10 wheat Production Years From UP --
select year,round(sum(wheat_production)) as wheat_production from agri_data
group by year
order by wheat_production desc
limit 10;


-- Millet Production Last 50 years --
select year,round(sum(pearl_millet_production) + sum(finger_millet_production)) as pearl_millet_production from agri_data
group by year
order by year desc
limit 50;


-- Sorghum Production (Kharif and Rabi) by Region --
select state_name,round(sum(kharif_sorghum_production)) as kharif_sorghum_production,round(sum(rabi_sorghum_production)) as rabi_sorghum_production from agri_data
group by state_name
order by state_name;


-- Top 7 sates for Grountnut_Production --
select state_name,round(sum(groundnut_production)) as groundnut_production from agri_data
group by state_name
order by groundnut_production desc
limit 7;


-- Soybean Production by Top 5 States and Yield Efficiency --
select state_name,round(sum(soyabean_area)) as soyabean_area,
round(sum(soyabean_production)) as soyabean_production,
round(avg(soyabean_yield)) as yield_efficiency from agri_data
group by state_name
order by soyabean_production desc
limit 5;


-- Oilseed Production in Major States --
select state_name,round(sum(oilseeds_production)) as oilseeds_production from agri_data
group by state_name
order by oilseeds_production desc
limit 5;


-- Impact of Area Cultivated on Production (Rice, Wheat, Maize) --
select 'Rice' as crop,
    round(sum(rice_area)) as total_area, 
    round(sum(rice_production)) as total_production, 
    round(sum(rice_yield)) as avg_yield
from agri_data
union all
select 'Wheat' as crop, 
    round(sum(wheat_area)) as total_area, 
    round(sum(wheat_production)) as total_production, 
    round(sum(wheat_yield)) as avg_yield
from agri_data
union all
select 'Maize' as crop,
    round(sum(maize_area)) as total_area, 
    round(sum(maize_production)) as total_production,
    round(sum(maize_yield)) as avg_yield
from agri_data
order by total_production desc;


-- Rice vs Wheat Yield Across States --
select state_name,round(sum(rice_production)) as rice_production, round(avg(rice_yield),2) as rice_yield,
round(sum(wheat_production)) as wheat_production, round(avg(wheat_yield),2) as wheat_yield from agri_data
group by state_name
order by state_name;




-- Year Wise Trend of Rice Production Across State (Top 3) --
with topstates as (select state_name,round(sum(rice_production)) as rice_production from agri_data
group by state_name
order by rice_production desc
limit 3)
select a.year,round(sum(a.rice_production)) as rice_production from agri_data as a
join topstates as top
on a.state_name=top.state_name
group by a.year
order by a.year asc,rice_production desc
limit 3;


-- Top 5 Districts by Wheat Yield Increase Over the Last 5 Years --
select ag1.dist_name,round(avg(ag1.wheat_yield)) as wheat_yield_increase from agri_data as ag1
inner join (select year from agri_data group by year order by year desc limit 5) as ag2
on ag1.year = ag2.year
group by ag1.dist_name
order by wheat_yield_increase desc
limit 5;


-- States with the Highest Growth in Oilseed Production 5 Year --
select curr.state_name,curr.oilseeds_production as current_production,
    round(((curr.oilseeds_production - prev.oilseeds_production) / prev.oilseeds_production) * 100,2) as growth_percentage
from agri_data as curr
inner join agri_data as prev 
    ON curr.state_name = prev.state_name and curr.year = (select MAX(year) from agri_data) and prev.year = (select MAX(year) from agri_data) - 5  
order by growth_percentage desc
limit 5;


-- District-wise Correlation Between Area and Production for Major Crops (Rice, Wheat, and Maize) --
with corr as (
    select 
        dist_name,
        COUNT(*) as n,
        
        SUM(rice_area) as sum_rice_x,
        SUM(rice_production) as sum_rice_y,
        SUM(rice_area * rice_production) as sum_rice_xy,
        SUM(rice_area * rice_area) as sum_rice_xx,
        SUM(rice_production * rice_production) as sum_rice_yy,

        SUM(wheat_area) as sum_wheat_x,
        SUM(wheat_production) as sum_wheat_y,
        SUM(wheat_area * wheat_production) as sum_wheat_xy,
        SUM(wheat_area * wheat_area) as sum_wheat_xx,
        SUM(wheat_production * wheat_production) as sum_wheat_yy,

        SUM(maize_area) as sum_maize_x,
        SUM(maize_production) as sum_maize_y,
        SUM(maize_area * maize_production) as sum_maize_xy,
        SUM(maize_area * maize_area) as sum_maize_xx,
        SUM(maize_production * maize_production) as sum_maize_yy
    from agri_data
    group by dist_name
)
select 
    dist_name,
    round(((n * sum_rice_xy - sum_rice_x * sum_rice_y) / 
    (SQRT(n * sum_rice_xx - sum_rice_x * sum_rice_x) * SQRT(n * sum_rice_yy - sum_rice_y * sum_rice_y)))*100,2) as rice_correlation,

    round(((n * sum_wheat_xy - sum_wheat_x * sum_wheat_y) / 
    (SQRT(n * sum_wheat_xx - sum_wheat_x * sum_wheat_x) * SQRT(n * sum_wheat_yy - sum_wheat_y * sum_wheat_y)))*100,2) as wheat_correlation,

    round(((n * sum_maize_xy - sum_maize_x * sum_maize_y) /
    (SQRT(n * sum_maize_xx - sum_maize_x * sum_maize_x) * SQRT(n * sum_maize_yy - sum_maize_y * sum_maize_y)))*100,2) as maize_correlation

from corr
order by dist_name;



-- Yearly Production Growth of Cotton in Top 5 Cotton Producing States --
with cotton as (
    select state_name, SUM(cotton_production) as total_production
    from agri_data
    group by state_name
    order by total_production desc
    limit 5
), yearly_data as (
    select state_name, year, sum(cotton_production) as total_production
    from agri_data
    where state_name in (select state_name from cotton)
    group by state_name, year
)
select 
    curr.state_name, 
    curr.year, 
    ROUND(((curr.total_production - prev.total_production) / (prev.total_production)) * 100, 2) AS growth_percentage
FROM yearly_data as curr
inner join yearly_data as prev
    on curr.state_name = prev.state_name
    and curr.year = prev.year + 1
order by curr.state_name, curr.year;


-- Districts with the Highest Groundnut Production in 2010 --
select dist_name,sum(groundnut_production) as groundnut_production from agri_data
where year = 2010
group by dist_name
order by groundnut_production desc
limit 5;


-- Annual Average Maize Yield Across All States --
select year,state_name,avg(maize_yield) as maize_yield from agri_data
group by year,state_name
order by year,state_name desc;


-- Total Area Cultivated for Oilseeds in Each State --
select state_name,round(sum(oilseeds_area),2) as total_area from agri_data
group by state_name
order by state_name;


-- Districts with the Highest Rice Yield --
select dist_name,round(avg(rice_yield)) as rice_yield from agri_data
group by dist_name
order by rice_yield desc
limit 5;


-- Compare the Production of Wheat and Rice for the Top 5 States Over 10 Years --
with state_names as (
    select state_name from agri_data 
    group by state_name 
    order by sum(rice_production) + sum(wheat_production) desc 
    limit 5
),last_years as (
    select distinct year from agri_data 
    order by year desc 
    limit 10
)
select ag.state_name,round(sum(ag.wheat_production)) as wheat_production,round(sum(ag.rice_production)) as rice_production from agri_data as ag
inner join state_names as st
on ag.state_name = st.state_name
inner join last_years as ys
on ag.year = ys.year
group by state_name;