# Flask module import
# Flask, render_template
import os
from flask import Flask, render_template, request
app = Flask(__name__)	# Flask object Assign to app

# 임시 cctv 리스트에 데이터 추가
cctv_cap_list = []
cctv_cap_list2 = []

# 임시 온습도 리스트에 데이터 추가
temp_cap_list = []

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


@app.route("/cctv_list",  methods=['POST', 'GET'])
def cctv_page() :
    # 사람이 인식된 시간을 데이터로 보냄
    return render_template('cctv_list.html', rows=cctv_cap_list, rows2=cctv_cap_list2)

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

# CCTV 클라이언트로부터의 값 얻기
# 값 넣기
@app.route("/insertCctv", methods=['POST'])
def insertCctv() :
    request.values['is']    #
    current_time = request.values['time'] # 측정된 시간

    current_img = request.files['media']
    imageFileName = current_time + '.jpg'
    current_img.save(os.path.join( 'static/cctv_img/', imageFileName)) # 파일 저장
    # image 파일 저장
    cctv_cap_list2.append(imageFileName)
    cctv_cap_list.append(current_time)
    return ""

@app.route("/insertGas", methods=['POST'])
def insertGas() :

    request.values[''];

    return ""

# 온습도 클라이언트로부터의 값 얻기
# 값 넣기
@app.route("/insertTemp", methods=['POST'])
def insertTemp() :
    
    current_temp = request.values['temp'] # 온도
    current_hum = request.values['hum'] # 습도
    current_time = request.values['time'] # 측정된 시간
    
    #tempValueName = current_time
    #current_value.save(os.path.join('static/temp_value/', tempValueName))
    
    
    print(current_temp, current_hum, current_time)

    temp_cap_list.append(current_time)
    return ""




host_addr = "0.0.0.0"
port_num = "8080"
if __name__ == "__main__":
    app.run(host=host_addr, port=port_num, debug=True)
