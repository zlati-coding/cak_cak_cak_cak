#include <Wire.h>

// APDS-9930 Sensor Definitions
#define APDS9930_I2C_ADDR  0x39
#define APDS9930_ENABLE    0x80
#define APDS9930_ATIME     0x81
#define APDS9930_CONTROL   0x8F
#define APDS9930_ID        0x92
#define APDS9930_DATA0LOW  0x94
#define APDS9930_DATA0HIGH 0x95

// GY-31 TCS3200 Sensor Definitions
#define s0 8
#define s1 9
#define s2 10
#define s3 11
#define out 12

void apds9930_init() {
    Wire.begin();
    Wire.beginTransmission(APDS9930_I2C_ADDR);
    Wire.write(APDS9930_ID);
    Wire.endTransmission();
    Wire.requestFrom(APDS9930_I2C_ADDR, 1);
    if (Wire.available()) {
        byte device_id = Wire.read();
    }
    Wire.beginTransmission(APDS9930_I2C_ADDR);
    Wire.write(APDS9930_ENABLE);
    Wire.write(0x03);
    Wire.endTransmission();
    Wire.beginTransmission(APDS9930_I2C_ADDR);
    Wire.write(APDS9930_ATIME);
    Wire.write(0xFF);
    Wire.endTransmission();
    Wire.beginTransmission(APDS9930_I2C_ADDR);
    Wire.write(APDS9930_CONTROL);
    Wire.write(0x02);
    Wire.endTransmission();
}

uint16_t read_light() {
    Wire.beginTransmission(APDS9930_I2C_ADDR);
    Wire.write(APDS9930_DATA0LOW);
    Wire.endTransmission();
    Wire.requestFrom(APDS9930_I2C_ADDR, 2);
    if (Wire.available() == 2) {
        byte data_low = Wire.read();
        byte data_high = Wire.read();
        return (data_high << 8) | data_low;
    }
    return 0;
}

void tcs3200_init() {
    pinMode(s0, OUTPUT);
    pinMode(s1, OUTPUT);
    pinMode(s2, OUTPUT);
    pinMode(s3, OUTPUT);
    pinMode(out, INPUT);
    digitalWrite(s0, HIGH);
    digitalWrite(s1, LOW);
}

int GetData() {
    int data = pulseIn(out, LOW);
    float freq = (1 / (data * 0.000001));
    int scaledValue = map(freq, 0, 120000, 0, 255);
    return constrain(scaledValue, 0, 255);
}

void read_tcs3200() {
    int red, green, blue;
    digitalWrite(s2, LOW); digitalWrite(s3, LOW); red = GetData();
    digitalWrite(s2, HIGH); digitalWrite(s3, HIGH); green = GetData();
    digitalWrite(s2, LOW); digitalWrite(s3, HIGH); blue = GetData();
    char hexColor[8];
    red += 84; // 5V - colors from cup only measurements:
    green += 69;
    blue += 20;
    // red += 128; // 3.3V - colors from cup only measurements: //129,130,33
    // green += 128;
    // blue += 52;
    red = (red > 255) ? (red - 256) : red;
    green = (green > 255) ? (green - 256) : green;
    blue = (blue > 255) ? (blue - 256) : blue;
    // if(red < 110 && green < 110) {red -= 8; green -= 8;}
    // if(red > 140 || green > 140) {red += 8; green += 12;}
    sprintf(hexColor, "#%02X%02X%02X", red, green, blue);
    Serial.println(hexColor);
}

void setup() {
    Serial.begin(9600);
    Wire.begin();
    apds9930_init();
    tcs3200_init();
}

void loop() {
    //Serial.print("Ambient Light: "); Serial.print(read_light()); Serial.println(" lux");
    if(read_light() == 1024) Serial.print("Clear urine with hex color: ");
    else Serial.print("! Unclear urine !  Hex color: ");
    read_tcs3200();
    delay(1000);
}