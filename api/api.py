from unicodedata import category
import flask
from flask_mysqldb import MySQL
from flask import jsonify, request
from flask_cors import CORS 
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tests'
app.config['MYSQL_DB'] = 'budget_dashboard'

@app.route('/home', methods=['GET'])
def default_dashboard():
    json_data = request.json    
    
    #Default values in dropdown
    cur = mysql.connection.cursor()
    cur.execute(f"select distinct(DATE_FORMAT(month, '%b')) AS month from budget_dashboard.data;")
    unique_month = cur.fetchall()
    cur.execute(f"select distinct(category) AS month from budget_dashboard.data;")
    unique_category = cur.fetchall()
    #Unique month and category for dropdown
    month  = [m[0] for m in unique_month]    
    category  = [c[0] for c in unique_category]
    
    #Updating where clause in query
    
    received_month = json_data['month'] if json_data['month'] else month
    received_category = json_data['category'] if json_data['category'] else category
    
    where_clause = f"where DATE_FORMAT(month, '%b') in ('"+"','".join(received_month)+"') and category in ('"+"','".join(received_category)+"') "
    
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
    
    final_data = [{"month": month, "category": category, "pie_chart_data_merchant" : list(pie_chart_data_merchant), "pie_chart_data_category" : list(pie_chart_data_category)}]
    return jsonify(final_data)


app.run()


