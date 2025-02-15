import streamlit as st
import pandas as pd
import pymysql

# Function to connect to MySQL
def connect_to_mysql():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="0000",
        database="Retail_shop"
    )

# Function to fetch data by running a query
def fetch_data(query):
    connection = connect_to_mysql()
    try:
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        return f"Error: {e}"
    finally:
        connection.close()

# # Streamlit UI
st.title("MySQL Query Viewer")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Sidebar for Topics
st.sidebar.title("Topics")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Initialize session state to track selected topic
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

# Handle button clicks for topics
if st.sidebar.button("Profit Analysis"):
    st.session_state.selected_topic = "Profit Analysis"

if st.sidebar.button("Sales and Discounts"):
    st.session_state.selected_topic = "Sales and Discounts"

if not st.session_state.selected_topic:
    # Show summary on the main page
    st.subheader("Welcome to the MySQL Query Viewer")
    st.markdown("""
        This application allows you to explore and analyze data from a **Retail Shop** database.
        
        ### Key Features:
        - **Profit Analysis** : Explore data about profits, top-performing cities, and categories.
        - **Sales and Discounts** : Analyze sales performance, discounts, and regional sales metrics.

        ### How to Use:
        1. Select a topic from the left sidebar (e.g., **Profit Analysis** or **Sales and Discounts**).
        2. Click on a question to view the query results directly below the question.""")

else:
# Define each question as a button with its query
    if st.session_state.selected_topic == "Profit Analysis":
        st.info("Questions for Profit Analysis")
        if st.button("Find the top 5 cities with the highest profit margins?"):
            query = """
                select city,sum(profit) as total_profit from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by city order by total_profit desc limit 5;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Calculate the total discount given for each category"):
            query = """
                select category,sum(discount) as total_discount from retail_shop.order_datas 
                group by category;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Find the average sale price per product category"):
            query = """
                select category,avg(sale_price) as average_sales from retail_shop.order_datas
                group by category;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Find the region with the highest average sale price"):
            query = """
                select region,avg(sale_price) as average_sale_price from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by region
                order by average_sale_price desc
                limit 1;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Find the total profit per category"):
            query = """
                select category,sum(profit) as profit from retail_shop.order_datas
                group by category;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Identify the top 3 segments with the highest quantity of orders"):
            query = """
                select segment,sum(quantity) as highest_order from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by segment;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Determine the average discount percentage given per region"):
            query = """
                select region,avg(discount_percent) as avg_discount_percent from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by region;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Find the product category with the highest total profit"):
            query = """
                select category,sum(profit) as highest_profit from retail_shop.order_datas
                group by category
                order by highest_profit desc
                limit 1;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Calculate the total revenue generated per year"):
            query = """
                select year(order_date) as year,sum(sale_price * quantity) as total_revenue 
                from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by year(order_date)
                order by year;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

    elif st.session_state.selected_topic == "Sales and Discounts":
        st.info("Questions for Sales and Discounts")
        if st.button("Find the comparission between the previous year"):
            query = """with monthly_sales as (
                select year(o2.order_date) as year,month(o2.order_date) as month,sum(sale_price * quantity) as total_sale 
                from retail_shop.order_datas o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by year(o2.order_date),month(o2.order_date)
                order by year,month
                ),
                sale_change as (
                        select m1.year,m1.month,m1.total_sale as current_year,m2.total_sale as previous_year,
                        round(((m1.total_sale - m2.total_sale)/m2.total_sale)*100,2) as percentage
                        from monthly_sales as m1
                        inner join monthly_sales as m2
                        on m1.month = m2.month and m1.year = m2.year + 1)
                select year,month,current_year,previous_year,percentage from sale_change order by year,month;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("product with best profit margins"):
            query = """
                select category,sub_category,product_id,sum(sale_price * quantity) as total_revenue,
                sum((sale_price - cost_price) * quantity) as total_profit,
                round((sum((sale_price - cost_price) * quantity)/sum(sale_price * quantity))*100,2) as profit_margin
                from retail_shop.order_datas group by category,sub_category,product_id
                order by profit_margin desc
                limit 10;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Rank products by revenue and profit margin"):
            query = """
                select category,sub_category,product_id,
                total_profit,total_revenue,profit_margin,
                row_number() over(partition by category,sub_category order by total_revenue desc) as revenue_rank,
                row_number() over(partition by category,sub_category order by profit_margin desc) as profit_margin_rank
                from (
                    select category,sub_category,product_id,sum(sale_price * quantity) as total_revenue,
                    sum((sale_price - cost_price) * quantity) as total_profit, 
                    round((sum((sale_price - cost_price) * quantity)/sum(sale_price * quantity))*100.2) as profit_margin
                    from retail_shop.order_datas 
                    group by category,sub_category,product_id
                    ) as profit_revenue limit 10;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("find the regional sales order"):
            query = """
                select region,sum(sale_price * quantity) as total_sales,count(o2.order_id) as total_orders,
                round(avg(o1.sale_price * o1.quantity),2) as average_sales
                from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by region
                order by total_sales desc;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Find the distribution of discount"):
            query = """
                select category,sub_category,product_id,
                case
                    when ((list_price - sale_price)/list_price * 100) < 5 then '0 - 5%'
                    when ((list_price - sale_price)/list_price * 100) between 5 and 10 then '5 - 10%'
                    else '> 10%'
                    end as discount_range
                    from retail_shop.order_datas
                    group by category,sub_category,product_id,discount_range
                    order by discount_range desc
                    limit 10;"""    
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)
        
        if st.button("Find the business margin"):
            query = """
                select category,sub_category,
                case
                when (sum((sale_price - cost_price)*quantity)/(sum(sale_price * quantity)))*100 < 20 then 'Bad business'
                else 'Good business'
                end as business_margin
                from retail_shop.order_datas
                group by category,sub_category,product_id
                order by business_margin desc
                limit 10;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)
        
        if st.button("find which city eran lowest profit"):
            query = """
                select city,sum(sale_price) as sale_price,sum(cost_price) as cost_price,sum((sale_price-cost_price)*quantity) as low_profit
                from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by city
                order by low_profit
                limit 10;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:   
                st.error(result)
        
        if st.button("Stock status based on quantity and profit analysis"):
            query = """
                select category,sub_category,product_id,sum(quantity) as quantity,sum(profit) as profit,
                case
                    when sum(quantity) < 10 and sum(profit) > 100 then 'Under stocked'
                    when sum(quantity) < 5 and avg(discount_percent) > 20 then 'Over stocked'
                    else 'Normal stocked'
                    end as stock_status
                from retail_shop.order_datas
                group by category,sub_category,product_id
                limit 10;"""
            
            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)

        if st.button("Top sales day analysis"):
            query = """
                select dayname(order_date) as day_name,sum(sale_price*quantity) as total_sale
                from retail_shop.order_datas as o1
                inner join retail_shop.order_data as o2
                on o1.order_id = o2.order_id
                group by day_name
                order by total_sale desc
                limit 1;"""

            st.write("**Result :**")
            result = fetch_data(query)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            else:
                st.error(result)


# Retail Shop Data Insights

#     This analysis uncovers insights about profit trends, sales performance, discounts, and stock status
#     to guide better business decisions. It leverages data to identify key opportunities
#     for growth and optimization in retail operations


# 1. Profit Analysis
#     Top Cities: Identifies the 5 cities with the highest profit margins.
#     Category Profit: Shows total profit for each product category.
#     Best Region: Highlights the region with the highest average sale price.
#     Yearly Revenue: Tracks yearly revenue trends.
#     Top Categories: Finds the category with the highest total profit.
#     Segment Orders: Identifies the 3 segments with the highest order quantities.
#     Discount by Region: Calculates the average discount percentage per region.
#     Total Discounts: Summarizes total discounts given per category


# 2. Sales and Discounts
#     Sales Comparison: Compares sales between the current and previous year.
#     Top Products: Lists products with the best profit margins.
#     Revenue & Profit Rank: Ranks products by revenue and profit margin.
#     Discount Ranges: Groups products by low, medium, and high discounts.
#     Stock Status: Flags overstocked, understocked, and normal-stocked products.
#     Low-Profit Cities: Shows cities earning the lowest profits.
#     Regional Sales: Highlights total sales and orders by region.
#     Business Margin: Categorizes segments as "Good" or "Bad" business.
#     Top Sales Day: Identifies the day with the highest total sales.

# Tools Used:
#     Python (Streamlit, Pandas, PyMySQL)
#     SQL for querying the Retail Shop database