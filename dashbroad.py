import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Retail Orders")

# Database connection details
DB_CONFIG = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "bT8swS26BAtNGVT.root",
    "password": "7RcQUUaNCC6fW75i",
    "database": "retail_order",
}

queries = {
    "Top 10 highest revenue generating products": '''SELECT product_id, SUM(sale_price) AS total_revenue 
                                                    FROM products 
                                                    GROUP BY product_id 
                                                    ORDER BY total_revenue DESC 
                                                    LIMIT 10''',
    "Top 5 cities with the highest profit margins": '''SELECT o.city,SUM(p.profit) AS total_profit
                                                        FROM orders o
                                                        INNER JOIN products p ON o.order_id = p.order_id
                                                        GROUP BY o.city
                                                        ORDER BY total_profit DESC
                                                        LIMIT 5''',
    "Total discount given for each category": '''SELECT category, SUM(discount) AS total_discount 
                                                  FROM products 
                                                  GROUP BY category''',
    "Average sale price per product category": '''SELECT category, AVG(sale_price) AS average_price 
                                                   FROM products 
                                                   GROUP BY category''',
    "Region with the highest average sale price": '''SELECT o.region, AVG(p.sale_price) AS highest_avg_region
                                                      FROM orders o
                                                      INNER JOIN products p ON o.order_id = p.order_id
                                                      GROUP BY o.region
                                                      ORDER BY highest_avg_region DESC
                                                      LIMIT 1''',
    "Total profit per category": '''SELECT category, SUM(profit) AS total_profit 
                                     FROM products 
                                     GROUP BY category''',
    "Top 3 segments with the highest quantity of orders": '''SELECT o.segment, SUM(p.quantity) AS total_quantity
                                                              FROM orders o
                                                              JOIN products p ON o.order_id = p.order_id
                                                              GROUP BY o.segment
                                                              ORDER BY total_quantity DESC
                                                              LIMIT 3''',
    "Average discount percentage given per region": '''SELECT o.region, AVG(p.discount_percent) AS avg_discount_percent
                                                        FROM orders o
                                                        INNER JOIN products p ON o.order_id = p.order_id
                                                        GROUP BY o.region''',
    "Product category with the highest total profit": '''SELECT category, SUM(profit) AS total_profit 
                                                         FROM products 
                                                         GROUP BY category 
                                                         ORDER BY total_profit DESC 
                                                         LIMIT 1''',
                "total revenue generated per year":'''SELECT YEAR(o.order_date) AS order_year, 
                                                    SUM(p.sale_price) AS total_revenue
                                                    FROM orders o
                                                    JOIN products p ON o.order_id = p.order_id
                                                    GROUP BY order_year
                                                    ORDER BY order_year''',
                "Most Ordered Products": '''SELECT p.product_id, COUNT(o.order_id) AS total_orders
                                FROM orders o
                                JOIN products p ON o.order_id = p.order_id
                                GROUP BY p.product_id
                                ORDER BY total_orders DESC
                                LIMIT 10''',
                "Average Order Value per Month": '''SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS month, 
                                               AVG(p.sale_price) AS avg_order_value
                                        FROM orders o
                                        JOIN products p ON o.order_id = p.order_id
                                        GROUP BY month
                                        ORDER BY month''',
                "Top 3 Most Profitable Regions": '''SELECT o.region, SUM(p.profit) AS total_profit
                                        FROM orders o
                                        JOIN products p ON o.order_id = p.order_id
                                        GROUP BY o.region
                                        ORDER BY total_profit DESC
                                        LIMIT 3''',
                "Products with the Highest Discounts": '''SELECT product_id, MAX(discount) AS max_discount
                                              FROM products
                                              GROUP BY product_id
                                              ORDER BY max_discount DESC
                                              LIMIT 10''',
                "Most Profitable Sub-Category":'''SELECT sub_category, SUM(profit) AS total_profit
                                                FROM products
                                                GROUP BY sub_category
                                                ORDER BY total_profit DESC
                                                LIMIT 3''',
                "State-wise Revenue Distribution":'''SELECT o.state, SUM(p.sale_price) AS total_revenue
                                                    FROM orders o
                                                    JOIN products p ON o.order_id = p.order_id
                                                    GROUP BY o.state
                                                    ORDER BY total_revenue DESC''',
                "Highest Discounted Products":'''SELECT product_id, discount_percent
                                                FROM products
                                                ORDER BY discount_percent DESC
                                                LIMIT 10''',
                "Region with the Least Number of Orders":'''SELECT o.region, COUNT(o.order_id) AS order_count
                                                        FROM orders o
                                                        GROUP BY o.region
                                                        ORDER BY order_count ASC
                                                        LIMIT 1''',
                "Product Category That Had the Highest Price Fluctuation":'''SELECT category, MAX(list_price) - MIN(list_price) AS price_fluctuation
                                                                            FROM products
                                                                            GROUP BY category
                                                                            ORDER BY price_fluctuation DESC
                                                                            LIMIT 1''',
                " State That Purchased the Most Expensive Product":'''SELECT o.state, MAX(p.list_price) AS most_expensive_product
                                                                    FROM orders o
                                                                    JOIN products p ON o.order_id = p.order_id
                                                                    GROUP BY o.state
                                                                    ORDER BY most_expensive_product DESC
                                                                    LIMIT 1'''
}

# Layout split into two columns
left_col, right_col = st.columns([1, 2])
connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor()
with left_col:
    query_choice = st.selectbox("Select a query to run:", list(queries.keys()))
    if st.button("Run Query"):
        try:
            cursor.execute(queries[query_choice])
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            
            st.dataframe(df)
            
            with right_col:
                if len(df) > 0:
                    fig, ax = plt.subplots(figsize=(4, 4))  
                    df.plot(kind='bar', x=df.columns[0], y=df.columns[1], ax=ax, width=0.5)
                    ax.set_title(query_choice)
                    st.pyplot(fig)
                else:
                    st.write("No data available to plot.")
        except Exception as e:
            st.error(f"Error: {e}")
cursor.close()
connection.close()                                                                          