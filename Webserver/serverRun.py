
from vo import cctvVo, tempVo
from flask import Flask, render_template, request
from mariadb import dbConnection
import os
import datetime


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

    # database에서 값 꺼내기
    db = dbConnection.dbConnection(host='192.168.219.111', id='latte', pw='lattepanda', db_name='test')
    dataFrame = db.selectTemp()
    
    # converting to dict
    data_dict = dataFrame.to_dict()

    # t_no
    # t_time
    # t_temp
    # t_humi
    tempVo_list.clear()
    print(  len(data_dict['t_time'] )  )
    
    for i in range( len( data_dict['t_time'] ) ) :
        obj = tempVo.tempVo(  data_dict['t_time'][ i ],  data_dict['t_temp'][ i ],  data_dict['t_humi'][ i ]  )
        tempVo_list.append(obj)
    
    return render_template('temp_list.html', rows=tempVo_list)

@app.route("/gas_page",  methods=['POST', 'GET'])
def gas_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)

@app.route("/dust_page",  methods=['POST', 'GET'])
def dust_page() :
    _ip = getIp()
    return render_template('menu.html', _ip=_ip)

@app.route("/insertGas", methods=['POST','GET'])
def insertGas() :
    gas = request.args.get("gas");
    print(gas)
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

# From Temperature/Humidity 온습도 클라이언트로부터의 값 얻어서 넣기
@app.route("/insertTemp", methods=['POST', 'GET'])
def insertTemp() :

    # 본래 소스코드
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    c_time = request.values['time'] # 측정된 시간
    c_time =nowDatetime         # imsi 현재시간
    c_temp = request.values['temp'] # 온도
    c_hum = request.values['hum'] # 습도
    c_sig1 = request.values['sig1'] #main sensor
    c_sig2 = request.values['sig2'] #main sensor
    # test 소스코드
    #current_time = "20201015"
    #current_temp = 36.6
    #current_hum = 45.3

    instance = tempVo.tempVo(c_time, c_temp, c_hum) # 객체에 저장
    tempVo_list.append(instance)
        
    db = dbConnection.dbConnection(host='192.168.219.111', id='latte', pw='lattepanda', db_name='test')
    db.insertTemp(c_time, c_temp, c_hum)
    return ""
#--------------------------------------------------------------------

host_addr = "0.0.0.0"
port_num = "8080"
if __name__ == "__main__":
    app.run(host=host_addr, port=port_num, debug=True)
