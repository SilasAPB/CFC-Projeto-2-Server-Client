static int PINO = 3;
static int BAUDRATE = 100;
static float T_OPP = 162e-6/500;
static float DEN = 1/BAUDRATE*T_OPP;
static float UNHDEN = 1/BAUDRATE*T_OPP*1.5;

char reading;

void setup() {
  pinMode(PINO,INPUT);
  Serial.begin(9600);
}

int calc_even_parity(byte data) {
  int ones = 0;
  for (int i = 0; i < 8; i++) {
        ones += (data >> i) & 0x01;
  }
  return ones%2;
}

void accu_timer(){
    for(int i = 0 ; i < 1000 ; i++){
      asm("NOP");
    }
}

void unh_accu_timer(){
    for(int i = 0 ; i < 500 ; i++){
      asm("NOP");
    }
}

void loop() {
  Serial.println("Esperando start bit");
  bool start_bit = digitalRead(PINO);
  while(start_bit){
    for(int i = 0 ; i < 10 ; i++){
      asm("NOP");
    }
    start_bit = digitalRead(PINO);
  }
  // Serial.println("Início da transmissão:");
  unh_accu_timer();
  accu_timer();
  for(int i = 7 ; i>=0 ; i--){
    // bool bit = digitalRead(PINO);
    reading |= digitalRead(PINO)<<i;
    accu_timer();
    // Serial.println(bit);
  }
  bool parity = digitalRead(PINO);
  // Serial.println(parity);
  int calc = calc_even_parity(reading);
  if (parity!=calc){
    Serial.println("Erro de paridade");
  }
  Serial.println(reading);
  Serial.println("--------");
  
}
