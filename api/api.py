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
    # Initializing the cursor
    cur = mysql.connection.cursor()

    if request.method == 'GET':
        # TBD - filter data based on month
        # select merchant, sum(spent) from budget_dashboard.data  where DATE_FORMAT(month, '%b') in ('Apr')  group by merchant order by spent desc;
        merchant_query = f"select merchant, sum(spent) from budget_dashboard.data group by merchant order by spent desc;"
        cur.execute(merchant_query)
        result_merchant = cur.fetchall()
        cur.execute(
            f"select category, sum(spent) from budget_dashboard.data group by category order by spent desc;")
        result_category = cur.fetchall()
        cur.execute(
            f"select FORMAT(sum(spent),0) AS total from budget_dashboard.data;")
        result_spent = cur.fetchall()
        pie_chart_data_merchant = []
        pie_chart_data_category = []

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

        final_data = [{"pie_chart_data_merchant": list(pie_chart_data_merchant), "pie_chart_data_category": list(
            pie_chart_data_category), "total": result_spent[0]}]
        return jsonify(final_data)

    if request.method == 'POST':
        json_data = request.json
        print("Json_data", json_data)
        # Updating where clause in query

        received_month = json_data['month'] if json_data['month'] else "','".join(
            json_data['all_months'])
        received_year = json_data['year'] if json_data['year'] else "','".join(
            json_data['all_years'])
        received_category = json_data['category'] if json_data['category'] else "','".join(
            json_data['all_categories'])

        category = []
        # month = category = merchant = set()
        print(
            f"select distinct(category) AS month from budget_dashboard.data where DATE_FORMAT(month, '%b') in ('{received_month}') and DATE_FORMAT(month, '%Y') in ('{received_year}');")
        cur.execute(
            f"select distinct(category) AS month from budget_dashboard.data where DATE_FORMAT(month, '%b') in ('{received_month}') and DATE_FORMAT(month, '%Y') in ('{received_year}');")
        unique_category = cur.fetchall()
        # Unique category for selected month
        category = [c[0] for c in unique_category]
        # Fetch only relevant month in response for dropdown value
        cur.execute(
            f"select distinct(DATE_FORMAT(month, '%b')) AS month from budget_dashboard.data where DATE_FORMAT(month, '%b') in ('{received_month}') and DATE_FORMAT(month, '%Y') in ('{received_year}');")
        unique_month = cur.fetchall()
        # Unique category for selected month
        month = [m[0] for m in unique_month]

        if len(received_category) >= 1:
            where_clause = f"where DATE_FORMAT(month, '%b') in ('{received_month}') and category in ('{received_category}') and DATE_FORMAT(month, '%Y') in ('{received_year}') "
        else:
            where_clause = f"where DATE_FORMAT(month, '%b') in ('{received_month}') and DATE_FORMAT(month, '%Y') in ('{received_year}') "

        merchant_query = f"select DATE_FORMAT(month, '%b') AS month, account, category, merchant, description, sum(spent) from budget_dashboard.data " + \
            where_clause+" group by merchant order by 5 desc;"
        cur.execute(merchant_query)
        result_merchant = cur.fetchall()
        cur.execute(f"select DATE_FORMAT(month, '%b') AS month, category, sum(spent) from budget_dashboard.data " +
                    where_clause+" group by category order by 3 desc;")
        result_category = cur.fetchall()

        cur.execute(
            f"select FORMAT(sum(spent),0) AS total from budget_dashboard.data "+where_clause+";")
        result_spent = cur.fetchall()
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

        final_data = [{"pie_chart_data_merchant": list(pie_chart_data_merchant), "pie_chart_data_category": list(
            pie_chart_data_category), "category": category, "total": result_spent[0], "month": month}]
        return jsonify(final_data)


@app.route('/default', methods=['GET'])
def dropdown_values():

    # Default values in dropdown
    cur = mysql.connection.cursor()
    cur.execute(
        f"select distinct(DATE_FORMAT(month, '%b')) AS month from budget_dashboard.data;")
    unique_month = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute(
        f"select distinct(DATE_FORMAT(month, '%Y')) AS month from budget_dashboard.data;")
    unique_year = cur.fetchall()
    cur.execute(
        f"select distinct(category) AS month from budget_dashboard.data;")
    unique_category = cur.fetchall()
    cur.execute(
        f"select FORMAT(sum(spent),0) AS total from budget_dashboard.data;")
    sum_total = cur.fetchall()
    print("sum total", sum_total[0])
    # Unique month and category for dropdown
    month = [m[0] for m in unique_month]
    year = [y[0] for y in unique_year]
    category = [c[0] for c in unique_category]
    total = sum_total[0]

    # month = category = merchant = set()
    line_chart_data_category = []
    cur.execute(f"select DATE_FORMAT(month, '%Y-%m') AS month, category, sum(round(spent)) as spent from budget_dashboard.data group by category, month order by 1 desc;")
    line_chart_data = cur.fetchall()
    # Parsing Line Chart Data
    temp_data = []
    for c in category:
        for t in line_chart_data:
            if t[1] == c:
                temp_data.append({'x': t[0], 'y': t[2]})
        line_chart_data_category.append({'id': c, 'data': temp_data})
        temp_data = []

    final_data = [{"year": year, "month": month, "category": category,
                   "total": total, "line_chart_data": line_chart_data_category}]
    return jsonify(final_data)


app.run()
