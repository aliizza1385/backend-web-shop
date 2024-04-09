from flask import Blueprint, jsonify, request
from initialize import db
import sqlite3


blueprint = Blueprint('kpi', __name__)



@blueprint.route('/kpi', methods=["GET"])
def KPI():
    conn = sqlite3.Connection('shop.db')
    c = conn.cursor()

    # total_sales = c.fetchone()
    c.execute('''SELECT DATE(o.order_date) as order_date, SUM(od.quantity) as total_sales
             FROM orderItem od
             JOIN order o ON od.order_id = o.id
             GROUP BY DATE(o.order_date)
             ORDER BY DATE(o.order_date)''')
    total_sales_by_date = c.fetchall()
    total_sales_data = [{"date": row[0], "total_sales": row[1]} for row in total_sales_by_date]

    print('aascascascascascasasc')

    c.execute('''SELECT DATE(order_date) as order_date, SUM(total_amount) as revenue
             FROM orders
             GROUP BY DATE(order_date)
             ORDER BY DATE(order_date)''')
    revenue_by_date = c.fetchall()
    revenue_data = [{"date": row[0], "revenue": row[1]} for row in revenue_by_date]


    
    c.execute(''' SELECT products.name, SUM(quantity) as total_sales 
                 FROM orderDetails 
                 JOIN products 
                 ON products.id = orderDetails.product_id
                 GROUP BY product_id 
                 ORDER BY total_sales DESC 
                 LIMIT 5 
                ''')
    top_products = c.fetchall()

    top_products_data = [{"product_name": row[0], "quantity": row[1]} for row in top_products]

    c.close()
    conn.close()
    return jsonify({
        "total_sales": total_sales_data,
        "revenue": revenue_data,
        "top_products": top_products_data
    }), 200
