from unicodedata import category
import flask
from flask_mysqldb import MySQL
from flask import jsonify, request
from flask_cors import CORS 
import calendar
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'budget_dashboard'

@app.route('/home', methods=['GET'])
def default_dashboard():
    cur = mysql.connection.cursor()
    cur.execute(f"select month(month), account, category, merchant, description, spent from budget_dashboard.data;")
    result = cur.fetchall()
    json_data = []
    bar_chart_data = []
    # month = category = merchant = set()
    month  = set()
    category  = set()
    # Month,Account,Category,Merchant,Description,Amount
    '''     {
              "merchant": "SharkNinja",
              "amount": 116,
            },
    '''
    for data in result:
        json_data.append({
			'month':data[0],
			'account': data[1],
            'category':data[2],
			'merchant': data[3],
            'description':data[4],
			'amount': data[5],
			})
        bar_chart_data.append({
            'merchant': data[3],
            'amount': data[5],
            'category':data[2]
        })
        month.add(data[0])
        category.add(data[2])
        # merchant.add(data[3])
    month = [calendar.month_name[m] for m in month]
    # for m in month:
    #     print("month is", m)
    #     print("month name", calendar.month_name(m))
    
    # final_data = [{"month": month, "category": category, "merchant": merchant, "data": json_data}]
    final_data = [{"month": month, "category": list(category), "data": json_data, "bar_chart_data" : list(bar_chart_data)}]
    return jsonify(final_data)


app.run()


