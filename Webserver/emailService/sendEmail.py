import smtplib
from email.mime.text import MIMEText

class sendEmail:
    # 생성자
    def __init__(self, subject, content) :
        # 보낼 명단
        sendEmail.slist = [ "isaac7263@naver.com", "juhea0619@naver.com", "itit2014@naver.com", "rabbit3919@naver.com" ] 
        sendEmail.str = ','.join(sendEmail.slist)

        # 세션 생성
        sendEmail.s = smtplib.SMTP('smtp.gmail.com', 587)
        #sendEmail.toUser = toUser
        sendEmail.subject = subject
        sendEmail.content = content
        # TLS 보안 시작
        sendEmail.s.starttls()
        # 로그인 인증
        sendEmail.s.login('iotanyang@gmail.com', 'yebwsjsmnkmzdtcm')
        # 보낼 메시지 설정
        # 내용
        sendEmail.msg = MIMEText(content)
        # 수신
        sendEmail.msg['To'] = sendEmail.str #"isaac7263@naver.com"
        # 제목
        sendEmail.msg['Subject'] = subject
        # 메일 보내기
        sendEmail.s.sendmail("iotanyang@gmail.com", sendEmail.slist, sendEmail.msg.as_string())
        sendEmail.s.quit()

        
#jntcqybvciaxogdf - isak7263
#yebwsjsmnkmzdtcm - iotanyang - iotserver
