const int buttonPin1 = 8;      //  8 번핀 스위치 입력 테스트 (PLC의 ready신호)

char LEDpin1 = 12;    //  OK LED 포트 설정
char LEDpin2 = 13;    //  NG

int flag = 0;
int NGflag = 0;
int OKflag = 0;

// LED확인용 함수.
void OK(void)
{
    digitalWrite(LEDpin1, HIGH);
    digitalWrite(LEDpin2, LOW);
}
void NG(void)
{
    digitalWrite(LEDpin2, HIGH);
    digitalWrite(LEDpin1, LOW);
}


void setup() {
  Serial.begin(115200);              //  시리얼 통신의 시작, 보레이트 입력
  pinMode(buttonPin1, INPUT_PULLUP);  //  스위치 내부풀업저항 입력포트로 셋팅.
  
  pinMode(LEDpin1, OUTPUT);           //  OK, NG LED 출력포트 지정.
  pinMode(LEDpin2, OUTPUT);
}

void loop() {
  char c = Serial.read();           //  PC로부터온 값을 읽음.
  int buttonValue1 = digitalRead(8); //  8번 핀에서 읽음.
  
  if(buttonValue1 == LOW )           //  스위치가 눌릴때 ready신호를 보냄. (PLC -> PC)
  {
    flag = 1;
  }
  if(flag == 1)
  {
      Serial.println("ready");      //  준비가 되었다고 PC에 신호를 보냄.
      delay(500);
      flag = 0;
  }

  // 아스키코드 0x31 들어올때, OK
  if( c == '1')
  {
      OKflag = 1;
  }

  // 아스키코드 0x32 들어올때, NG
  else if( c == '2')
  {
      NGflag = 1;
  }

  

  if(OKflag == 1)
  {
    OK();
    OKflag = 0;
  }
  if(NGflag == 1)
  {
    NG();
    NGflag = 0;
  }

}