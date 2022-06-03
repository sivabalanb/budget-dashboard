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
    # month = category = merchant = set()
    month  = set()
    category  = set()
    # Month,Account,Category,Merchant,Description,Amount
    for data in result:
        json_data.append({
			'month':data[0],
			'account': data[1],
            'category':data[2],
			'merchant': data[3],
            'description':data[4],
			'amount': data[5],
			})
        month.add(data[0])
        category.add(data[2])
        # merchant.add(data[3])
    month = [calendar.month_name[m] for m in month]
    # for m in month:
    #     print("month is", m)
    #     print("month name", calendar.month_name(m))
    print(f"month {month} category {category}")
    # final_data = [{"month": month, "category": category, "merchant": merchant, "data": json_data}]
    final_data = [{"month": month, "category": list(category), "data": json_data}]
    return jsonify(final_data)

@app.route('/chart', methods=['POST'])
def chart():
	asin = request.json
	print("Asin requested from React", asin)
	cur = mysql.connection.cursor()
	cur.execute(f"select  FROM_UNIXTIME(date_recorded), FLOOR(price) from amazon_202005 where asin = '{asin}'")
	result = cur.fetchall()
	json_data = []

	for data in result:
		json_data.append({
			'x':data[0],
			'y': data[1]
			})

	final_data = [{ "id":"Price History", "color": "hsl(116, 70%, 50%)", "data": json_data}]
	return jsonify(final_data)

app.run()


