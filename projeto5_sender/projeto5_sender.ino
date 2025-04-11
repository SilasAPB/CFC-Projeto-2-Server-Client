void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Monitoramento Iniciado!");
  pinMode(3,OUTPUT);
  pinMode(4,INPUT);
  digitalWrite(3,HIGH);
}

static int BAUDRATE = 9600;
static float T_OPP = 162e-6/500;
static float DEN = 1/BAUDRATE*T_OPP;

void accu_timer(){
  for(int i = 0 ; i < DEN ; i++){
    asm("NOP");  }
  }

int calc_even_parity(byte data) {
    int ones = 0;
    for (int i = 0; i < 8; i++) {
        ones += (data >> i) & 0x01;
    }
    return ones % 2;
}


void loop() {
  accu_timer();
  char caractere = 'Y'; // ASCII de 'A' = 65 (01000001)
  int p = calc_even_parity(caractere);
  digitalWrite(3,LOW);
  accu_timer();
  for (int i = 7; i >= 0; i--) {
      bool bitParaEnviar = (caractere >> i) & 1;

      Serial.println(bitParaEnviar);
      digitalWrite(3, bitParaEnviar);
      // if (bitParaEnviar == 1){
      //   digitalWrite(3, HIGH);
      // }
      // else{
      //   digitalWrite(3, LOW);
      // }
      accu_timer(); // Pequeno atraso para garantir transmissão
  }
  // Serial.println("Bit de paridade:");

  digitalWrite(3,p);
  digitalWrite(3,HIGH);
  Serial.println("----------------------------------------------");
  // put your main code here, to run repeatedly:
}
