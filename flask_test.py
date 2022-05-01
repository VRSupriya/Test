
from flask import Flask, request
# import mysql.connector
from flask_mysqldb import MySQL
import traceback


app = Flask(__name__)

app = Flask(__name__)
 
app.config['MYSQL_HOST'] = "electricity.cbvsurjzzr0t.ap-south-1.rds.amazonaws.com"
app.config['MYSQL_USER'] = 'adminuser'
app.config['MYSQL_PASSWORD'] = 'jishoy123'
app.config['MYSQL_DB'] = 'electricity'
 
mysql = MySQL(app)
  
# connection = mysql.connector.connect(
#   host="electricity.cbvsurjzzr0t.ap-south-1.rds.amazonaws.com",
#   user="adminuser",
#   password="jishoy123",
#   database = "electricity"

# )

  
@app.route('/insertdb',methods = ['POST'])
def insertdb():
    try:
        content = request.json
        uname = content['username']
        uid = content['uid']
        current = content['current']
        voltage = content['voltage']
        power = content['power']
        energy=content['energy']
        frequency=content['frequency']
        pf=content['pf']
        
        dbcursor = mysql.connection.cursor()

        table_name = f'{uname}_{str(uid)}'

        dbcursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(table_name.replace('\'', '\'\'')))
        if dbcursor.fetchone()[0] == 1:
            print("true")
        else:
            create_table_query = f"create table {table_name} ( row_id INT NOT NULL AUTO_INCREMENT, user_id INT NOT NULL, user_name VARCHAR(50) NOT NULL, current DECIMAL(10,2) NOT NULL, voltage DECIMAL(10,2) NOT NULL, power DECIMAL(10,2) NOT NULL, energy DECIMAL(10,2) NOT NULL, frequency DECIMAL(10,2) NOT NULL, PF DECIMAL(10,2) NOT NULL, PRIMARY KEY ( row_id ) );"
            dbcursor.execute(create_table_query)
            print(dbcursor)

        insert_query  = f"INSERT INTO {table_name} (user_id, user_name, current, voltage, power, energy, frequency, PF) \
            VALUES ({uid}, '{uname}', {current}, {voltage}, {power}, {energy},{frequency}, {pf});"

        dbcursor.execute(insert_query)
        mysql.connection.commit()
        dbcursor.close()

        return {"message":"success"}
    except:
        traceback.print_exc()
        return {"message": "failure"}

@app.route('/test',methods = ['POST'])
def test():
    try:
        content = request.data
        print(content)
        return {"message":"success"}
    except:
        traceback.print_exc()
        return {"message": "failure"}

  
if __name__ == '__main__':
   app.run(debug = True)



#pip install Flask
#####pip install mysql_connector_python
#pip install flask_mysqldb





