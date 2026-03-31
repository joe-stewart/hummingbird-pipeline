#include "Arduino_LED_Matrix.h"
#include "WiFiS3.h"
#include "arduino_secrets.h"
#include "RTC.h"
#include <NTPClient.h>
#include <WiFiUdp.h>
#include "digits.h"

#define DEBUG false

// Network
char ssid[] = WIFI_SSID;
char pass[] = WIFI_PASS;
int status = WL_IDLE_STATUS;

// UDP ping listener
#define PING_PORT 8888
#define MAGIC "HUMM"
WiFiUDP pingUdp;

// Counter
int birdCount = 0;

// Watchdog
#define ACTIVE_HOUR_START 6
#define ACTIVE_HOUR_END   20
#define WATCHDOG_HOURS    4
unsigned long lastPingTime = 0;

// Display
ArduinoLEDMatrix matrix;

void setupMatrix() {
    matrix.begin();
    matrix.loadSequence(LEDMATRIX_ANIMATION_WIFI_SEARCH);
    matrix.begin();
    matrix.play(true);
}

void setupWiFi() {
    if (WiFi.status() == WL_NO_MODULE) {
        while (true);
    }
    while (status != WL_CONNECTED) {
        status = WiFi.begin(ssid, pass);
        delay(10000);
    }
    if (DEBUG) Serial.println("IP: " + WiFi.localIP().toString());
    if (DEBUG) {
    byte mac[6];
    WiFi.macAddress(mac);
    Serial.print("MAC: ");
    for (int i = 0; i < 6; i++) {
        if (mac[i] < 16) Serial.print("0");
        Serial.print(mac[i], HEX);
        if (i < 5) Serial.print(":");
    }
    Serial.println();
}
}

void setupNTP() {
    RTC.begin();

    WiFiUDP ntpUdp;
    NTPClient timeClient(ntpUdp);

    timeClient.begin();
    timeClient.update();

    const int TIMEZONE_OFFSET_HOURS = -7; // PDT
    auto unixTime = timeClient.getEpochTime() + (TIMEZONE_OFFSET_HOURS * 3600);
    RTCTime timeToSet = RTCTime(unixTime);
    RTC.setTime(timeToSet);
}

void setupUDP() {
    pingUdp.begin(PING_PORT);
}

void updateDisplay() {
    byte frame[8][12];
    
    // digit cycles 0-9
    memcpy(frame, digits[birdCount % 10], sizeof(frame));
    
    // blank separator column 8
    for (int row = 0; row < 8; row++) {
        frame[row][8] = 0;
    }
    
    // ticks show number of rollovers
    int ticks = birdCount / 10;
    for (int col = 9; col < 12; col++) {
        for (int row = 0; row < 8; row++) {
            int tickNum = (col - 9) * 8 + row;
            frame[row][col] = (tickNum < ticks) ? 1 : 0;
        }
    }
    
    matrix.renderBitmap(frame, 8, 12);
    if (DEBUG) Serial.println("Count: " + String(birdCount));
}

void checkWatchdog() {
    RTCTime t;
    RTC.getTime(t);
    int hour = t.getHour();

    // only warn during active hours
    if (hour < ACTIVE_HOUR_START || hour >= ACTIVE_HOUR_END) return;

    unsigned long elapsed = (millis() - lastPingTime) / 1000 / 3600;
    if (lastPingTime > 0 && elapsed >= WATCHDOG_HOURS) {
        matrix.renderBitmap(warn, 8, 12);
        if (DEBUG) Serial.println("Watchdog: no detection in " + String(elapsed) + " hours");
    }
}

void checkForPing() {
    int packetSize = pingUdp.parsePacket();
    if (packetSize) {
        char buf[16];
        pingUdp.read(buf, sizeof(buf));
        if (strncmp(buf, MAGIC, 4) == 0) {
            birdCount++;
            lastPingTime = millis();
            if (DEBUG) Serial.println("Ping received, count: " + String(birdCount));
            updateDisplay();
        }
    }
}

void setup() {
    if (DEBUG) {
        Serial.begin(115200);
        unsigned long start = millis();
        while (!Serial && millis() - start < 3000);
    }

    setupMatrix();
    setupWiFi();
    setupNTP();
    setupUDP();
    updateDisplay(); // show zero on boot
    /*
    for(int i=0; i<10; i++) {
        matrix.renderBitmap(digits[i], 8, 12);
        delay(2000);
    }
    */
}

void loop() {
    checkForPing();
    checkWatchdog();
    delay(100);
}