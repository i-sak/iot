import pymysql
import pandas as pd

class dbConnection:
    def __init__(self, host, id, pw, db_name) :
        self.conn = pymysql.connect(host=host, user=id, passwd=pw, db=db_name, charset='utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    # 온습도 저장
    def insertTemp( self , t_time, t_temp, t_humi ) :
        sql = "INSERT INTO `temperature` ( t_time, t_temp, t_humi ) VALUES ( %s, %s, %s ) ;" % ( t_time, t_temp, t_humi ) 
        self.curs.execute(sql)
        self.conn.commit()

    # 온습도 전체 불러오기
    def selectTemp(self):
        sql = "SELECT * FROM `temperature` ORDER BY t_time DESC LIMIT 10;"
        self.curs.execute(sql)
        
        result = self.curs.fetchall()
        result = pd.DataFrame(result)
        return result
    
    # 회원가입
    def insertMember( self , memail, mname, mpassword ) :
        sql = '''INSERT INTO `member` ( m_email, m_name, m_password ) VALUES ( "%s", "%s", "%s" ) ;'''%( memail, mname, mpassword ) 
        self.curs.execute(sql)
        self.conn.commit()

        

