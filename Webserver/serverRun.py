# Flask module import
# Flask, render_template
from flask import Flask, render_template, request
app = Flask(__name__)	# Flask object Assign to app

def getIp() :
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

## controller
# main page
@app.route("/")
def index() :
	return render_template('index.html')

# signin [log-in]
@app.route("/signin", methods=['POST', 'GET'])
def siginin() :
    if request.method == 'POST' :
         # post 로 보내면 request.form.get으로 받고,
         # get으로 보내는 경우 requst.args.get으로 받음
        _id = request.form.get('_id')  
        _password = request.form.get('_password')
        _ip = getIp()
        if _id == "1" and _password == "1" :
            return render_template('menu.html', _ip=_ip)
        else :
            return render_template('index.html')


@app.route("/cctv_page",  methods=['POST', 'GET'])
def cctv_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)

@app.route("/gas_page",  methods=['POST', 'GET'])
def gas_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)

@app.route("/temperature_page",  methods=['POST', 'GET'])
def temperature_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)

@app.route("/dust_page",  methods=['POST', 'GET'])
def dust_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)



host_addr = "0.0.0.0"
port_num = "8080"
if __name__ == "__main__":
    app.run(host=host_addr, port=port_num, debug=True)