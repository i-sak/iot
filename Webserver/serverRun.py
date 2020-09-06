# Flask module import
# Flask, render_template
from flask import Flask, render_template, request
app = Flask(__name__)	# Flask object Assign to app

## controller
# main page
@app.route("/")
def index() :
	return render_template('index.html')

@app.route("/signin", methods=['POST', 'GET'])
def siginin() :
    if request.method == 'POST' :
        _id = request.form.get('_id')   # post로 보낼 경우, request.form.get으로 받고, get으로 보내는 경우 requst.args.get으로 받음
        _password = request.form.get('_password')
        print(_id, _password)
        if _id == "1" and _password == "1" :
            return "login"
        else :
            return render_template('index.html')

host_addr = "0.0.0.0"
port_num = "8080"

if __name__ == "__main__":
    app.run(host=host_addr, port=port_num, debug=True)
