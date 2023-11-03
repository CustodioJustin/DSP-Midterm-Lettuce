var sheet_id = "";
var sheet_name = "Midterm Project - DHT22";
function doGet(e){
  var ss = SpreadsheetApp.openById(sheet_id);
  var sheet = ss.getSheetByName(sheet_name);
  var temp = Number(e.parameter.temp);
  var humi = Number(e.parameter.humi);
  var date = String(e.parameter.date);
  sheet.appendRow([date,temp,humi]);
}