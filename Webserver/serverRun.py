from vo import cctvVo, tempVo

import os
from flask import Flask, render_template, request
app = Flask(__name__)	# Flask object Assign to app

cctvVo_list = [] # 임시 cctv 리스트에 데이터 추가
tempVo_list = []  # 온습도 리스트에 데이터 추가

def getIp() :
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

#--------------------------------------------------------------------
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


#--------------------------------------------------------------------
# list page
#--------------------------------------------------------------------
# cctv_list page
@app.route("/cctv_list",  methods=['POST', 'GET'])
def cctv_list() :
    return render_template('cctv_list.html', rows=cctvVo_list)

@app.route("/temp_list",  methods=['POST', 'GET'])
def tempe_list() :
    return render_template('temp_list.html', rows=tempVo_list)

@app.route("/gas_page",  methods=['POST', 'GET'])
def gas_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)


@app.route("/dust_page",  methods=['POST', 'GET'])
def dust_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)

@app.route("/insertGas", methods=['POST'])
def insertGas() :
    request.values['']
    return ""

#--------------------------------------------------------------------
# From CCTV client / insert
@app.route("/insertCctv", methods=['POST', 'GET'])
def insertCctv() :
    request.values['is']    # 테스트

    current_time = request.values['time'] # 측정 시간
    current_img = request.files['media']  # 이미지 

    # image 파일 저장
    imageFileName = current_time + '.jpg'
    current_img.save(os.path.join( 'static/cctv_img/', imageFileName)) # 파일 저장
    
    instance = cctvVo.cctvVo(current_time, imageFileName)   # 객체에 저장
    cctvVo_list.append(instance)
    return ""

# 온습도 클라이언트로부터의 값 얻어서 넣기
@app.route("/insertTemp", methods=['POST'])
def insertTemp() :
    
    current_time = request.values['time'] # 측정된 시간
    current_temp = request.values['temp'] # 온도
    current_hum = request.values['hum'] # 습도

    instance = tempVo.tempVo(current_time, current_temp, current_hum) # 객체에 저장
    tempVo_list.append(instance)
    return ""
#--------------------------------------------------------------------

host_addr = "0.0.0.0"
port_num = "8080"
if __name__ == "__main__":
    app.run(host=host_addr, port=port_num, debug=True)
