#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

WiFiUDP ntpUDP;

const int DHT_pin = 33;
const char* ntpServer = "time.google.com"; // Uses google service to get the current time and date

DHT DHT(DHT_pin, DHT22);
NTPClient timeClient(ntpUDP, ntpServer);

const char* ssid = "";
const char* pass = "";
const char* DataSheetURL = "https://script.google.com/macros/s/AKfycbyO-UiwwD87Ji4_cboRknn6ZFRTTBTOC7h5_uG-vmFy5cjtm_eZvfk69gCkrPRjzh0l/exec";

bool IsConnected = false;

float temp = 0.0;
float humi = 0.0;

const unsigned long DHT22_Interval = 900000 ; // this controls the interval of sending data to the excel in milliseconds (15 minutes)
unsigned long DHT22_PrevTime = 0;
const unsigned long ConnectionCheck_Interval = 1000;
unsigned long ConnectionCheck_PrevTime = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  NetworkAccess();
  DHT.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long CurrentTime = millis();

  // repeatedly check if the ESP32 is still connected, every 1 seconds
  if(CurrentTime - ConnectionCheck_PrevTime >= ConnectionCheck_Interval) {
    ConnectionCheck_PrevTime = CurrentTime;
    NetworkAccess();
  }

  if(CurrentTime - DHT22_PrevTime >= DHT22_Interval) {
    DHT22_PrevTime = CurrentTime;
    temp = DHT.readTemperature();
    humi = DHT.readHumidity();

    timeClient.update();
    // Get the current date and time
    time_t now = timeClient.getEpochTime();
    struct tm *timeinfo = localtime(&now);

    // Cheat sheet comment:
    int year = timeinfo->tm_year + 1900; // Years since 1900
    int month = timeinfo->tm_mon + 1;    // Month (0-11)
    int day = timeinfo->tm_mday;         // Day of the month (1-31)
    int hour = timeinfo->tm_hour;        // Hour (0-23)
    int minute = timeinfo->tm_min;       // Minute (0-59)
    int second = timeinfo->tm_sec;       // Second (0-59)

    // Format: "YY_MM_DD-HH_MM_SS"
    String formattedDateTime = String(year) + "_" +
                              (month < 10 ? "0" : "") + String(month) + "_" +
                              (day < 10 ? "0" : "") + String(day) + "-" +
                              (hour < 10 ? "0" : "") + String(hour) + "_" +
                              (minute < 10 ? "0" : "") + String(minute) + "_" +
                              (second < 10 ? "0" : "") + String(second);

    if (isnan(temp) || isnan(humi)) {
      Serial.println("Failed to read from DHT sensor!");
      temp = 0.0;
      humi = 0.0;
      //return;
    }

    // Construct the final URL to add temp and humid along with the current time to the excel sheet.
    String DataURL = String(DataSheetURL) + "?temp=" + String(temp) + "&humi=" + String(humi) + "&date=" + String(formattedDateTime);
    HTTPClient http;
    http.begin(DataURL);

    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      Serial.print("Response Code:");
      Serial.print(httpResponseCode);
      Serial.print("  ||  Temperature: ");
      Serial.print(temp);
      Serial.print(" °C  ||  ");
      Serial.print("Humidity: ");
      Serial.print(humi);
      Serial.print(" %  ||  ");
      Serial.print("Date: ");
      Serial.println(formattedDateTime);
    }
    else {
      Serial.print("Error in HTTP GET request. HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}

// Connects the ESP32 to a network and initiate the timeclient and set its timezone (GMT+8)
void NetworkAccess() {
  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED) {
      Serial.println("Connecting to WiFi...");
      delay(1000);
    }
    Serial.println("Connected to WiFi!");
    timeClient.begin();
    delay(100);
    timeClient.update();
    timeClient.setTimeOffset(28800);
  }
}
