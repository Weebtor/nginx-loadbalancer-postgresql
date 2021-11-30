from flask import Flask, json, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def connect_to_master():
    return psycopg2.connect(
        dbname="my_database",
        user="zuka",
        password="zukaritas",
        host="localhost",
        port="55432"
    )

def connect_to_slave():
    return psycopg2.connect(
        dbname="my_database",
        user="zuka",
        password="zukaritas",
        host="localhost",
        port="65432"
    )

@app.route("/")
def hello_world():
    pid = os.getpid()
    return f"<h1> Hello World </h1> <hr> from {pid}"

@app.route("/AddProduct",  methods = ["POST"])
def add_product():
    if request.method == "POST":
        product_json = request.json
        try:
            # Postgres
            conn = connect_to_master()
            cursor = conn.cursor()
            query = """
                INSERT INTO producto (nombre,codigo,precio)
                VALUES (%s,%s,%s)
            """
            cursor.execute(
                query,
                (
                    product_json["nombre"],
                    product_json["codigo"].upper(),
                    product_json["precio"]
                )            
            )
            conn.commit()
            conn.close()
            return jsonify({
                "msg":"producto agregado correctamente",
                "pid": str(os.getpid())
            })
        except Exception as e:
            conn.close()
            return jsonify({
                "error":str(e),
                "pid": str(os.getpid())
            })
        


@app.route("/GetProduct",  methods = ["GET"])
def get_product():
    if request.method == "GET":
        try:

            search_query = request.args.get("q")    

            # Postgres
            conn = connect_to_slave()
            cursor = conn.cursor()
            query = """
                SELECT array_to_json(array_agg(row_to_json(t)))
                FROM (
                    SELECT nombre,codigo,precio
                    FROM producto
                    WHERE nombre like %s
                ) as t
                
            """
            cursor.execute(query,("%"+search_query+"%",))
            product_list = cursor.fetchall()
            conn.close()
            return jsonify({
                "pid": str(os.getpid()),
                "product_list":product_list[0][0]
            })
        except Exception as e:
            conn.close()
            return jsonify({
                "error":str(e),
                "pid": str(os.getpid())
            })

if __name__ == "__main__":
    # app.run(debug=True,host="0.0.0.0")
    app.run(debug=True)
