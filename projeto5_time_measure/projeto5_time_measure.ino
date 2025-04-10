void setup() {
  // put your setup code here, to run once:
  pinMode(5,OUTPUT);
}

int time = 500;
// 162 us para 500 iterações
/*
  162/500 = tempo para cada iteração (em us)
  1/(162/500) = frequencia de clock
*/

void loop() {
  digitalWrite(5,HIGH); 
  for (int i=0;i<500;i++){
    asm("NOP");
  };
  digitalWrite(5,LOW);
  for (int i=0;i<1000;i++){
    asm("NOP");
  };
}
