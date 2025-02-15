import zipfile
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import streamlit as st


zip_file_path = "C:/Users/91801/Desktop/orders.csv.zip"
zip_file = "Retail_Shop"

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(zip_file)

df = pd.read_csv("C:/Users/91801/Desktop/Retail_shop/Retail_Shop/orders.csv")

#handle the missing values
df["Ship Mode"] = df["Ship Mode"].fillna(df["Ship Mode"].mode()[0])


#rename the columns
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ","_")


#drop the row where columns have 0's
df = df[(df != 0).all(axis=1)]

#discount
df["discount"] = ((df["discount_percent"] / 100) * df["list_price"]).round(2)

#sale price
df["sale_price"] = df["list_price"] - df["discount"]


#profit
df["profit"] = df["sale_price"] - df["cost_price"]
df = df[~((df["profit"] == 0) | (df["sale_price"] == 0) | (df["discount"] == 0))]


#split two table
order_data = df[['order_id', 'order_date', 'ship_mode', 'segment', 'country', 'city','state', 'postal_code', 'region']]


order_datas = df[['order_id','category', 'sub_category','product_id', 'cost_price', 'list_price', 'quantity', 
            'discount_percent', 'discount', 'sale_price', 'profit']]



USER = 'root'
PASSWORD = '0000'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'Retail_shop'

myconnect = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD)
cursor = myconnect.cursor()

cursor.execute("create database if not exists Retail_shop")
print(f"Database {DATABASE} created or already exists.")

engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

# order_data.to_sql(name='order_data',con=engine,if_exists='replace',index=False)
# order_datas.to_sql(name='order_datas',con=engine,if_exists='replace',index=False)
print("DataFrames successfully written to the database.")

# cursor.execute("ALTER TABLE retail_shop.order_data ADD PRIMARY KEY(order_id);")
# cursor.execute("ALTER TABLE retail_shop.order_datas DROP FOREIGN KEY fk_order_id;")




#Function to connect to MySQL
def connect_to_mysql():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="0000",
        database="Retail_shop"
    )

#Function to fetch data by running a query
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