from flask import Flask	# Flask module import

app = Flask(__name__)	# Flask 객체를 app에 할당

@app.route("/")
def hello() :
	return "<h1>Hello World!</h1>"

host_addr = "122.43.56.49"
port_num = "8080"

if __name__ == "__main__":              
    app.run(host=host_addr, port=port_num)
