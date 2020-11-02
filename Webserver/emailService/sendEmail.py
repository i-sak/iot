import smtplib
from email.mime.text import MIMEText

class sendEmail:
    # 보낼 명단
    # slist = [ "isaac7263@naver.com", "juhea0619@naver.com", "itit2014@naver.com", "rabbit3919@naver.com", "mssong1397@naver.com" ]    
    def __init__(self) :
        # 세션 생성
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.msg = {}

    def setEmail(self, eTo, Subject, content) :
        # TLS 보안 시작
        self.s.starttls()
        # 로그인 인증
        self.s.login('iotanyang@gmail.com', 'yebwsjsmnkmzdtcm')
        
        # 보낼 메시지 설정
        # 수신
        self.msg = {}
        self.msg['To'] = "isaac7263@naver.com"
        # 제목
        self.msg['Subject'] = Subject
        # 내용
        self.msg = MIMEText(content)
        
    def sendTo(self, eTo):
        # 메일 보내기
        self.s.sendmail("iotanyang@gmail.com", "isaac7263@naver.com", self.msg.as_string())
        self.s.quit()
        

#jntcqybvciaxogdf - isak7263
#yebwsjsmnkmzdtcm - iotanyang - iotserver
