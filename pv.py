import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

def istZahl(s):
  try:
    float(s)
    return float(s)
  except ValueError:
    return s

url= 'http://sunnymk.selfhost.me/home.ajax'
u = urlopen(url)
soup = BeautifulSoup(u, 'html.parser')
    
seitentxt = str(soup)

#print(seitentxt)
data = json.loads(seitentxt)
#print(data)
leistung = data['Items'][0]['Power'].split(' ')
energie = data['Items'][1]['DailyYield'].split(' ')
gesEnergie = data['Items'][2]['TotalYield'].split(' ')
euroKwhBrutto = 0.3914
euroKwhNetto  = 0.3914/1.19
faktorCo2=0.7


energie = {
	'heute':istZahl(energie[0].replace(',','.')),
	'einheit':energie[1],
	'gesamt':istZahl(gesEnergie[0].replace(',','.')),
	'gesEinheit':gesEnergie[1]
}
	
leistung = {
	'aktuell':istZahl(leistung[0].replace(',','.')),
	'einheit':leistung[1],
}

if energie['einheit']!='kWh':
  energie['heute']=energie['heute']/1000

if leistung['einheit']!='kW':
  leistung['aktuell']=leistung['aktuell']/1000
  
verguetung = {
	'heuteNetto':round(energie['heute']*euroKwhNetto, 2),
	'heuteBrutto':round(energie['heute']*euroKwhBrutto, 2),
	'gesamtNetto':round(energie['gesamt']*euroKwhNetto * 1000),
	'gesamtBrutto':round(energie['gesamt']*euroKwhBrutto * 1000)
}

co2Vermeidung = {
  'heute':round(energie['heute']*faktorCo2,2),
  'gesamt':round(energie['gesamt']*faktorCo2,2)
}

x = {
	"EnergieHeute": round(energie['heute'],2),
	"EnergieGesamt": energie['gesamt'],
	"Leistung": round(leistung['aktuell'],2),
	"Verguetung_Heute_Brutto" : verguetung['heuteBrutto'],
	"Verguetung_Heute_Netto"  : verguetung['heuteNetto'],
	"Verguetung_Gesamt_Brutto": verguetung['gesamtBrutto'],
	"Verguetung_Gesamt_Netto" : verguetung['gesamtNetto'],
  "Co2_Vermeidung_Heute": co2Vermeidung['heute'],
  "Co2_Vermeidung_Gesamt": co2Vermeidung['gesamt']
}

y = json.dumps(x)
print(y)
