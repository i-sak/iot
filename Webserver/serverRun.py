
from vo import cctvVo, tempVo
from flask import Flask, render_template, request
from mariadb import dbConnection
from emailService import sendEmail
import os
import datetime


app = Flask(__name__)	# Flask object Assign to app

db = dbConnection.dbConnection(host='192.168.219.111', id='latte', pw='lattepanda', db_name='test')
sessionId = ""
slist = "isaac7263@naver.com, juhea0619@naver.com, itit2014@naver.com, rabbit3919@naver.com"
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
# 회원가입 Sign-Up
@app.route("/signup")
def signup():
    return render_template('signup.html')
# 회원가입 insert
@app.route("/signupInsert", methods=['POST'])
def signupInsert():
    _id = request.values["_id"]
    # _name = request.form.get('_name')
    _name = request.values["_name"]
    _password = request.values["_password"]

    print(_id, _name, _password)
    # 회원가입
    db = dbConnection.dbConnection(host='192.168.219.111', id='latte', pw='lattepanda', db_name='test')
    db.insertMember( _id, _name, _password )
    return render_template('index.html')


# signin [log-in]
@app.route("/signin", methods=['POST'])
def siginin() :
    if request.method == 'POST' :
         # post 로 보내면 request.form.get으로 받고,
         # get으로 보내는 경우 requst.args.get으로 받음
        _id = request.form.get('_id')  
        _password = request.form.get('_password')
        _ip = getIp()

        result = db.selectLoginMember(_id, _password)
        print(result[0]['COUNT(*)'])
        if ( result[0]['COUNT(*)'] == 1 ) :
            sessionId = ""
            sessionId += _id
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
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y%m%d%H%M%S')
    #c_time = request.values['time'] # 측정된 시간
    c_time =nowDatetime         # imsi 현재시간
    c_temp = request.values['temp'] # 온도
    c_hum = request.values['hum'] # 습도
    c_sig1 = request.values['sig1'] #main sensor
    c_sig2 = request.values['sig2'] #sub sensor

    # 이상감지
    print(c_sig1, c_sig2)
    if c_sig1 == "0" and c_sig2 == "1":
        sendEmail.sendEmail("S:[온습도]메인센서 이상", "C:[온습도]메인센서 이상")
    elif c_sig1 == "1"  and c_sig2 == "0" :
        sendEmail.sendEmail("S:[온습도]서브센서 이상", "C:[온습도]서브센서 이상")
    elif c_sig1 == "0" and c_sig2 == "0" :
        sendEmail.sendEmail("S:[온습도]메인센서, 서브센서 이상", "C:[온습도]메인센서, 서브센서 이상")

    db.insertTemp(c_time, c_temp, c_hum)
    return ""

@app.route("/insertGas", methods=['POST','GET'])
def insertGas() :
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y%m%d%H%M%S')
    #c_time = request.values['time'] # 측정된 시간
    c_time =nowDatetime         # imsi 현재시간
    c_gas = request.values["gas"]
    c_sig1 = request.values['flag1'] #main sensor
    c_sig2 = request.values['flag2'] #sub sensor

    # 이상감지
    print(c_sig1, c_sig2)
    if c_sig1 == "0" and c_sig2 == "1":
        sendEmail.sendEmail("S:[Gas]메인센서 이상", "C:[Gas]메인센서 이상")
    elif c_sig1 == "1"  and c_sig2 == "0" :
        sendEmail.sendEmail("S:[Gas]서브센서 이상", "C:[Gas]서브센서 이상")
    elif c_sig1 == "0" and c_sig2 == "0" :
        sendEmail.sendEmail("S:[Gas]메인센서, 서브센서 이상", "C:[Gas]메인센서, 서브센서 이상")
    elif c_sig1 =="2" :
        sendEmail.sendEmail("S:[Gas]가스 누출 메인센서 감지", "C:[Gas]가스 누출 메인센서 감지")
    elif c_sig2 =="2" :
        sendEmail.sendEmail("S:[Gas]가스 누출 서브센서 감지", "C:[Gas]가스 누출 서브센서 감지")

    return ""
#--------------------------------------------------------------------

host_addr = "0.0.0.0"
port_num = "8080"
if __name__ == "__main__":
    app.run(host=host_addr, port=port_num, debug=True)
