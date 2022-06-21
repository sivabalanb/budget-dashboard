from unicodedata import category
import flask
from flask_mysqldb import MySQL
from flask import jsonify, request
from flask_cors import CORS
from itsdangerous import json 
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'budget_dashboard'

@app.route('/home', methods=['GET', 'POST'])
def default_dashboard():
    #Initializing the cursor
    cur = mysql.connection.cursor()
    
    if request.method == 'GET':
        print("GET request")
        #TBD - filter data based on month
        #select merchant, sum(spent) from budget_dashboard.data  where DATE_FORMAT(month, '%b') in ('Apr')  group by merchant order by spent desc;
        merchant_query = f"select merchant, sum(spent) from budget_dashboard.data   group by merchant order by spent desc;"
        cur.execute(merchant_query)
        result_merchant = cur.fetchall()
        cur.execute(f"select category, sum(spent) from budget_dashboard.data group by category order by spent desc;")
        result_category = cur.fetchall()
        pie_chart_data_merchant = []
        pie_chart_data_category = []
        # month = category = merchant = set()

        for data in result_merchant:
            pie_chart_data_merchant.append({
                'id': data[0],
                'label': data[0],
                'value': data[1],
            })
            
        for data in result_category:
            pie_chart_data_category.append({
                'id': data[0],
                'label': data[0],
                'value': data[1],
            })
        
        final_data = [{ "pie_chart_data_merchant" : list(pie_chart_data_merchant), "pie_chart_data_category" : list(pie_chart_data_category)}]
        return jsonify(final_data)
    
    if request.method == 'POST':
        json_data = request.json
        print("Json_data", json_data)
        
        
        
        #Updating where clause in query
        print("json month", json_data['month'])
        received_month = json_data['month'] if json_data['month'] else []
        received_category = json_data['category'] if json_data['category'] else []
        print(f" received_month {received_category} month {received_month}")
        
        where_clause = f"where DATE_FORMAT(month, '%b') in ('{received_month}') and category in ('{received_category}') "
        
        merchant_query = f"select DATE_FORMAT(month, '%b') AS month, account, category, merchant, description, spent from budget_dashboard.data "+where_clause+" group by merchant;"
        print("merchantquery", merchant_query)
        cur.execute(merchant_query)
        result_merchant = cur.fetchall()
        cur.execute(f"select DATE_FORMAT(month, '%b') AS month, category, sum(spent) from budget_dashboard.data "+where_clause+" group by category order by 3 desc;")
        result_category = cur.fetchall()
        json_data = []
        pie_chart_data_merchant = []
        pie_chart_data_category = []
        # month = category = merchant = set()
        
        # Month,Account,Category,Merchant,Description,Amount
        '''     {
                "merchant": "SharkNinja",
                "amount": 116,
                },
        '''
        for data in result_merchant:
            pie_chart_data_merchant.append({
                'id': data[3],
                'label': data[3],
                'value': data[5],
            })
            
        for data in result_category:
            pie_chart_data_category.append({
                'id': data[1],
                'label': data[1],
                'value': data[2],
            })
        
        final_data = [{ "pie_chart_data_merchant" : list(pie_chart_data_merchant), "pie_chart_data_category" : list(pie_chart_data_category)}]
        return jsonify(final_data)

@app.route('/default', methods=['GET'])
def dropdown_values():
        
    #Default values in dropdown
    cur = mysql.connection.cursor()
    cur.execute(f"select distinct(DATE_FORMAT(month, '%b')) AS month from budget_dashboard.data;")
    unique_month = cur.fetchall()
    cur.execute(f"select distinct(category) AS month from budget_dashboard.data;")
    unique_category = cur.fetchall()
    #Unique month and category for dropdown
    month  = [m[0] for m in unique_month]    
    category  = [c[0] for c in unique_category]
    
    # month = category = merchant = set()
    
  
    
    final_data = [{"month": month, "category": category}]
    return jsonify(final_data)
app.run()


