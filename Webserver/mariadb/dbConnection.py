import pymysql
import pandas as pd

class dbConnection:
    def __init__(self, host, id, pw, db_name) :
        self.conn = pymysql.connect(host=host, user=id, passwd=pw, db=db_name, charset='utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    def insertTemp( self , t_time, t_temp, t_humi ) :
        sql = "INSERT INTO `temperature` ( t_time, t_temp, t_humi ) VALUES ( %s, %s, %s ) ;" % ( t_time, t_temp, t_humi ) 
        self.curs.execute(sql)
        self.conn.commit()

    def selectTemp(self):
        sql = "SELECT * FROM `temperature`;"
        self.curs.execute(sql)
        
        result = self.curs.fetchall()
        result = pd.DataFrame(result)
        return result
        
        

