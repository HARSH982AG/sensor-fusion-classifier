/*
 * Industrial Multi-Modal Chemical Sensor-Fusion Instrument
 * Author: Harsh Agarwal (HARSH982AG)
 * Target: ESP32 Dev Module (240MHz)
 */

#define NUM_CHANNELS 6
const int SENSOR_PINS[NUM_CHANNELS] = {34, 35, 32, 33, 36, 39};
const char* SENSOR_NAMES[NUM_CHANNELS] = {"mq3", "mq135", "mq2", "tgs", "cond1", "cond2"};

#define SAMPLE_WINDOW 16
float sample_buffers[NUM_CHANNELS][SAMPLE_WINDOW];
int buffer_idx = 0;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // 12-bit ADC (0 - 4095)
  analogSetAttenuation(ADC_11db); // 0 - 3.3V range

  for (int c = 0; c < NUM_CHANNELS; c++) {
    pinMode(SENSOR_PINS[c], INPUT);
    for (int i = 0; i < SAMPLE_WINDOW; i++) {
      sample_buffers[c][i] = 0.0;
    }
  }
}

float get_rolling_average(int channel, float new_val) {
  sample_buffers[channel][buffer_idx] = new_val;
  float sum = 0.0;
  for (int i = 0; i < SAMPLE_WINDOW; i++) {
    sum += sample_buffers[channel][i];
  }
  return sum / SAMPLE_WINDOW;
}

void loop() {
  Serial.print("{\"timestamp\":");
  Serial.print(millis());
  Serial.print(",\"readings\":{");

  for (int c = 0; c < NUM_CHANNELS; c++) {
    int raw = analogRead(SENSOR_PINS[c]);
    float voltage = (raw / 4095.0) * 3.3;
    float filtered = get_rolling_average(c, voltage);

    Serial.print("\"");
    Serial.print(SENSOR_NAMES[c]);
    Serial.print("\":");
    Serial.print(filtered, 4);
    if (c < NUM_CHANNELS - 1) Serial.print(",");
  }

  Serial.println("}}");

  buffer_idx = (buffer_idx + 1) % SAMPLE_WINDOW;
  delay(100); // 10Hz sampling frequency
}
