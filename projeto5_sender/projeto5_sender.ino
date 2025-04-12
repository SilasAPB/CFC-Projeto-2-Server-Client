static int BAUDRATE = 9600;
static float T_OPP = (0.000162) / 500; // Frequência de clock Arduino ajustada
static float DEN = (1.0 / BAUDRATE) / T_OPP; 
static float UNHDEN = ((1.0 / BAUDRATE) * 1.5) / T_OPP;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(4,OUTPUT);
  digitalWrite(4,HIGH);
}


void accu_timer(){
  for(int i = 0 ; i < DEN; i++){
    asm("NOP");  }
  }

int calc_even_parity(byte data) {
    int ones = 0;
    for (int i = 0; i < 8; i++) {
        ones += (data >> i) & 0x01;
    }
    return ones % 2;
}

char caractere = 'B';  // ASCII de 'Y' = 89 (01011001)
int p = calc_even_parity(caractere);

void loop() {
  delay(1000);

  digitalWrite(4,LOW);
  accu_timer();
  for (int i = 0; i < 8; i++) {
      bool bitParaEnviar = (caractere >> i) & 1;
      digitalWrite(4, bitParaEnviar);
      Serial.println(bitParaEnviar);
      accu_timer(); // Pequeno atraso para garantir transmissão
  }
 
  digitalWrite(4,p);
  accu_timer();
  digitalWrite(4,HIGH);
  accu_timer();
 Serial.println("------------------------------");
  // put your main code here, to run repeatedly:
}
