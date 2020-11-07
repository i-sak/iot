#include <Phpoc.h>
#include <String.h>
#include "SPI.h"

// hostname of web server:
//char server_name[] = "https://rabbit3919.wixsite.com/test/blank-cfaf";
//char server_name[] = "www.google.com";
//IPAddress server_name(216,58,200,4);
IPAddress server_name(122,43,56,49);
PhpocClient client;
///////////이메일 변수
PhpocServer server(80);
PhpocEmail email;
//////////
int send_data;

int main_flag = 1;
int backup_flag = 1;
////flag 
String send_string;
void setup() {
  Serial.begin(9600);
  while(!Serial)
    ;

  Serial.println("Sending GET request to web server");

  main_flag = 1;
  backup_flag = 1;

  send_data = 0;
  
  
  // initialize PHPoC [WiFi] Shield:
  Phpoc.begin(PF_LOG_SPI | PF_LOG_NET | PF_LOG_APP);
  //Phpoc.begin();

  if(client.connect(server_name, 8080))
  {
     Serial.println("Connected to server");
     all();
     Serial.println(send_string);
  }
}

void loop() {
  delay(10000);
  all();
  
  if(client.available())
  {
    // if there is an incoming byte from the server, read them and print them to
    // serial monitor:
    
    char c = client.read();
    Serial.print(c);
  }

  if(!client.connected()) //현재 여기로 들어오고 있음 
  {
   
    // if the server's disconnected, stop the client:
    Serial.println("disconnected");
    client.stop();
    // do nothing forevermore:
    while(true)
      ;
  }
}
void all(){
  sensor_work(); //센서데이터 처리 

  String sensor_send;
  String main_fl;
  String backup_fl;
    
  sensor_send = String(send_data);
  main_fl = String(main_flag);
  backup_fl = String(backup_flag);
    
    //int send_data = analogRead(A0);
  String s1 = "GET /insertGas?gas=";   
    //String s1 = "GET /insertGas?gas="+sensor_send+",main ="+main_fl+",backup ="+backup_fl+s2; 
  String s2 = ",flag1=";
  String s3 = ",flag2=";
  String s4 = " HTTP/1.0";
   
    
  send_string = s1+sensor_send+s2+main_fl+s3+backup_fl+s4;
  //String send_string = s1+sensor_send+s4;
  //Serial.println(send_string);
  //Serial.print("\n");
}
void sensor_work(){
  int sensor_data = analogRead(A0);
  int sensor_data2 = analogRead(A2);
  if((sensor_data == 0) || (sensor_data == 1)){
    //backup work function 
    Serial.println("main sensor fail");
    Serial.println("Inspection request");
    Serial.println("---------------------------");  

    main_email();
    
    main_flag = 0;
    backup_work();
  }
  else if((sensor_data > 900)){
    //gas leak
    Serial.println("---------------------------");
    Serial.println("Gas leak");
    Serial.println("Inspection request");
    Serial.print("sensor data : ");
    Serial.println(sensor_data);
    Serial.println("---------------------------");
    main_flag = 2; //가스누출 위험이므로 flag 다르게 

    leak_email();
  }
  else
  {
    Serial.println("main sensor work");
    Serial.println(sensor_data);
    send_data = sensor_data;
    main_flag = 1;
  }
  
}
void backup_work(){
  int sensor_data = analogRead(A2);
  if((sensor_data == 0) || (sensor_data == 1)){ //보조센서 고장
    Serial.println("All sensor fail");
    Serial.println("Inspection request");
    Serial.println("---------------------------");
    backup_flag = 0;

    backup_email();
  }
  else if((sensor_data > 900)){ //가스누출 위험
    Serial.println("---------------------------");
    Serial.println("Gas leak");
    Serial.println("Inspection request");
    Serial.print("sensor data : ");
    Serial.println(sensor_data);
    Serial.println("---------------------------");
    backup_flag = 2; //가스누출 위험이므로 flag 다르게 

    leak_email();
  }
  else //정상 작동
  {
     Serial.println("backup sensor work");
     Serial.println(sensor_data);
     send_data = sensor_data;
     backup_flag = 1;
  }
}

void main_email(){//main 센서 고장났을때
  email.setOutgoingServer("smtp.naver.com", 587);
  //naver 로그인 아이디와 비번
  email.setOutgoingLogin("네이버아이디", "네이버비밀번호"); // here
  //보내는 사람 이메일은 꼭 네이버 이메일만 가능
  email.setFrom("보내는사람 이메일", "보내는사람 아이디");  // here
  
  // set receiver's e-mail address and subject
  email.setTo("받는사람 이메일", "받는사람 아이디");  //here
  email.setSubject("메인 센서 고장 알림 이메일!!");
 
  // write e-mail message
  email.beginMessage();
  email.println("Hello, USER!");
  email.println("메인 센서가 고장났습니다");
  email.println("보조 센서가 작동중입니다.");
  email.println("메인 센서를 수리받으세요");
  email.println("점검 요청");
  email.endMessage();

  if(email.send() > 0)
    Serial.println("Email send ok");
  else
    Serial.println("Email send failed");
}

void backup_email(){ //backup 센서 고장났을때
  email.setOutgoingServer("smtp.naver.com", 587);
  email.setOutgoingLogin("네이버아이디", "네이버비밀번호"); // here
  //보내는 사람 이메일은 꼭 네이버 이메일만 가능
  email.setFrom("보내는사람 이메일", "보내는사람 아이디");  // here
  
  // set receiver's e-mail address and subject
  email.setTo("받는사람 이메일", "받는사람 아이디");  //here
  email.setSubject("보조 센서 고장 알림 이메일!!");
 
  // write e-mail message
  email.beginMessage();
  email.println("Hello, USER!");
  email.println("보조 센서가 고장났습니다");
  email.println("메인과 보조 센서 모두 고장났으니 수리를 받으셔야 합니다.");
  email.println("점검 요청");
  email.endMessage();

  if(email.send() > 0)
    Serial.println("Email send ok");
  else
    Serial.println("Email send failed");
}
void leak_email(){ //가스 누출시
  email.setOutgoingServer("smtp.naver.com", 587);
  email.setOutgoingLogin("네이버아이디", "네이버비밀번호"); // here
  //보내는 사람 이메일은 꼭 네이버 이메일만 가능
  email.setFrom("보내는사람 이메일", "보내는사람 아이디");  // here
  
  // set receiver's e-mail address and subject
  email.setTo("받는사람 이메일", "받는사람 아이디");  //here
  email.setSubject("가스 누출 알림 이메일!!");

  email.beginMessage();
  email.println("Hello, USER!");
  email.println("가스 감지정도가 900을 넘었습니다.");
  email.println("가스 누출이 의심되오니 점검을 받으세요!!");
  email.println("점검 요청!!");
  email.endMessage(); 
  // send email:
  if(email.send() > 0)
    Serial.println("Email send ok");
  else
    Serial.println("Email send failed");
}