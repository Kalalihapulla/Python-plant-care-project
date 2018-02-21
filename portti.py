import serial
import subprocess
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def lahetaSposti():
	
	# Määrittele viestin lähettäjä ja vastaanottaja
	
	strFrom = 'pate.py@gmail.com'
	strTo = 'pate.py@gmail.com'

	# Avaa tiedosto, jossa mittaustulokset, ja tallenna ne muuttujiin

	tiedosto = open("tiedot.txt","r")
	sisalto = tiedosto.readlines()
	
	numerot = sisalto[0]
	
	x = numerot.split(":")
	lampo = x[0]
	valot = x[1]
	kosteus = x[2]
	kastelukerrat = x[3]
	vesimaara = int(kastelukerrat)*25
	jaljmaara = 900-vesimaara
	
	tiedosto.close()
	
	# Luo viesti ja täytä lähettäjän ja vastaanottajan tiedot
	
	msgRoot = MIMEMultipart()
	msgRoot['Subject'] = 'Tulokset'
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	
	# Avaa lähetettävä kuva
	
	fp = open('pate.png', 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	# Määrittele kuvan nimi sekä numero ja lisää se viestiin
	
	msgImage.add_header('pate.png', '<image1>')
	msgRoot.attach(msgImage)

	# Viitataan kuvan numeroon
	
	msgText = MIMEText('<b> Lampotila(°C): {0}, Valoisuus(luxit): {1}, Kosteus: {2}, Kasteltu {3} kertaa, Vetta kaytetty {4}, ml Vetta jaljella {5} ml <b><br><img src="cid:image1"><br>Nifty!'.format(lampo, valot, kosteus, kastelukerrat, vesimaara, jaljmaara), 'html')
	msgRoot.attach(msgText)
	
	# Lähetä sähköposti
	
	smtp = smtplib.SMTP()
	smtp.connect('smtp.metropolia.fi')
	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
	smtp.quit()
	
def lahetaValovaroitus():
	# Määrittele viestin lähettäjä ja vastaanottaja
	
	strFrom = 'pate.py@gmail.com'
	strTo = 'pate.py@gmail.com'

	# Avaa tiedosto, jossa mittaustulokset, ja tallenna ne muuttujiin

	tiedosto = open("tiedot.txt","r")
	sisalto = tiedosto.readlines()
	
	numerot = sisalto[0]
	
	x = numerot.split(":")
	lampo = x[0]
	valot = x[1]
	kosteus = x[2]
	kastelukerrat = x[3]
	vesimaara = int(kastelukerrat)*25
	jaljmaara = 900-vesimaara
	
	tiedosto.close()
	
	# Luo viesti ja täytä lähettäjän ja vastaanottajan tiedot
	
	msgRoot = MIMEMultipart()
	msgRoot['Subject'] = 'Tulokset'
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	
	# Avaa lähetettävä kuva
	
	fp = open('pate1.png', 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	# Määrittele kuvan nimi sekä numero ja lisää se viestiin
	
	msgImage.add_header('pate1.png', '<image1>')
	msgRoot.attach(msgImage)

	# Viitataan kuvan numeroon
	
	msgText = MIMEText('<b> Kasvi varjossa tai ei saa tarpeeksi valoa! Valoisuus on vain {1} luxia<b><br><img src="cid:image1"><br>Nifty!'.format(lampo, valot, kosteus, kastelukerrat, vesimaara, jaljmaara), 'html')
	msgRoot.attach(msgText)
	
	# Lähetä sähköposti
	
	smtp = smtplib.SMTP()
	smtp.connect('smtp.metropolia.fi')
	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
	smtp.quit()
	
	

def lahetaVesivaroitus():
	# Määrittele viestin lähettäjä ja vastaanottaja
	
	strFrom = 'pate.py@gmail.com'
	strTo = 'pate.py@gmail.com'

	# Avaa tiedosto, jossa mittaustulokset, ja tallenna ne muuttujiin

	tiedosto = open("tiedot.txt","r")
	sisalto = tiedosto.readlines()
	
	numerot = sisalto[0]
	
	x = numerot.split(":")
	lampo = x[0]
	valot = x[1]
	kosteus = x[2]
	kastelukerrat = x[3]
	vesimaara = int(kastelukerrat)*25
	jaljmaara = 900-vesimaara
	
	tiedosto.close()
	
	# Luo viesti ja täytä lähettäjän ja vastaanottajan tiedot
	
	msgRoot = MIMEMultipart()
	msgRoot['Subject'] = 'Tulokset'
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	
	# Avaa lähetettävä kuva
	
	fp = open('pate.png', 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	# Määrittele kuvan nimi sekä numero ja lisää se viestiin
	
	msgImage.add_header('pate.png', '<image1>')
	msgRoot.attach(msgImage)

	# Viitataan kuvan numeroon
	
	msgText = MIMEText('<b> Vesi vahissa! Lisaa vesisailio tayteen ja kaynnista kastelujarjstelma uudelleen. Kasteltu {3} kertaa, Vetta kaytetty {4}, ml Vetta jaljella {5} ml <b><br><img src="cid:image1"><br>Nifty!'.format(lampo, valot, kosteus, kastelukerrat, vesimaara, jaljmaara), 'html')
	msgRoot.attach(msgText)
	
	# Lähetä sähköposti
	
	smtp = smtplib.SMTP()
	smtp.connect('smtp.metropolia.fi')
	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
	smtp.quit()

def createRRD():
	
	#Luo tietokanta.rrd tiedoston jonne tallennetaan mittausdataa
	
	subprocess.call(['rrdtool', 'create', 'tietokanta.rrd', '--step', '120',
					'DS:temp:GAUGE:120:0:30',
					'DS:light:GAUGE:120:0:500',
					'DS:kosteus:GAUGE:120:0:2000',
					'RRA:MAX:0.5:1:1440' ])
					
def addData(ltila, luxit, kosteus):
	
	#Lisää tietokanta.rrd tiedostoon mittausdataa
	
	subprocess.call(['rrdtool', 'update', 'tietokanta.rrd',
					'N:'+str(ltila)+':'+ str(luxit)+':'+str(kosteus)])
					
def graphRRD():
	
	#Piirrä mitatusta datasta kuvaaja (viimeinen 24h)
	
	subprocess.call(['rrdtool', 'graph', 'pate.png', '-w', '1000', '-h', '400', '--start', '-86400', '--end', 'N', 'DEF:temperature=tietokanta.rrd:temp:MAX', 'DEF:light=tietokanta.rrd:light:MAX','DEF:kosteus=tietokanta.rrd:kosteus:MAX', 'CDEF:valoa=light,10,/', 'CDEF:kosteuz=kosteus,100,/', 'LINE1:temperature#ff0000:Lampotila', 'LINE2:valoa#00000f:Valoisuus(lux/10)','LINE3:kosteuz#00ff00:Kosteus']) 
					

def valoRRD():
	
	#Piirrä mitatuista valon arvoista tarkennettu kuvaaja
	
	subprocess.call(['rrdtool', 'graph', 'pate1.png', '-w', '1000', '-h', '400', '--start', '-3600', '--end', 'N', 'DEF:light=tietokanta.rrd:light:MAX', 'LINE2:light#00000f:Valoisuus(lux)']) 




def main():

	# Luo tietokanta
	
	createRRD()
	
	# Asetetaan muuttuja kakstuntii Trueksi alussa, jotta ohjelman logiikka toimii oikein
	
	kakstuntii = True
	
	# Suoritetaan ohjelmaa silmukassa
	
	while True:
		
		# Tarkistaa kellonajan
		
		aika = time.strftime("%X")
		
		# Muutetaan kellonaika muotoon, jossa sitä voidaan käyttää ehtolausekkeissa
		
		kokoaika = aika.split(":")
		osa1 = kokoaika[0]
		osa2 = kokoaika[1]
		osa3 = kokoaika[2]
		kaikki = osa1+osa2+osa3
		kaikki = int(kaikki)
		
		# Tarkistaa onko yö, jotta voidaan asettaa valovaroituksen tarkistusehto Falseksi
		# Lähettää tilannepäivityksen sähköpostiin klo 6 ja 18
		
		if ((60000 <= kaikki) and (kaikki <= 60200)) or ((180000 <= kaikki) and (kaikki <= 180200)):
			lahetaSposti()
			if (kaikki >= 180000):
				tarkistavaloa = False
			else:
				tarkistavaloa = True
		else:
			tarkistavaloa = True
		
		# Vastaanottaa ja lukee pyboardin lähettämää dataa
		
		while True:
			port = serial.Serial('/dev/ttyAMA0', 115200, timeout = 0.1)
			port.write(bytes("alarm on\r".encode('ascii')))
			x = port.readline().decode('ascii')
			if x != "":
				break
			
		
		# Tallennetaan mittaustulokset muuttujiin
		
		tulokset = x.split(":")
		ltila = (tulokset[0])
		valo = (tulokset[1])
		kosteus = (tulokset[2])
		kastelukerrat = (tulokset[3])
		kosteus = float(kosteus)
		valo = float(valo)
		
		# Lisätään mittaustulokset tietokantaan
		
		addData(ltila, valo, kosteus)

		# Tehdään mittaustuloksista tekstitiedosto, jota voidaan hyödyntää sähköpostien lähetyksessä
		
		tiedosto = open("tiedot.txt","w")
		tiedosto.write(x)
		tiedosto.close()

		# Tarkistetaan kastelukerrat, ja lähetetään tarvittaessa varoitussähköposti
		
		if int(kastelukerrat) > 32:
			lahetaVesivaroitus()

		# Jotta vältyttäisiin turhilta sähköposteilta asetetaan ehto, että pimeässä lähetetään valovaroitusviesti vain kerran kahdessa tunnissa
		
		kaikkitaas = 0
		if kaikkitaas != 0 and (kaikkitaas+20000 <= kaikki):
			kakstuntii = True
		

		# Lähetetään valovaroitusviesti sähköpostiin, mikäli luxit ovat liian pienet, tarkistavaloa on True eli on päivä ja edellisestä varoitusviestistä on yli kaksi tuntia

		if int(valo) < 70 and tarkistavaloa and kakstuntii:
			valoRRD()
			lahetaValovaroitus()
			aikab = time.strftime("%X")
			rajoitus = aikab.split(":")
			eka = rajoitus[0]
			toka = rajoitus[1]
			kolmas = rajoitus[2]
			kaikkitaas = eka+toka+kolmas
			kaikkitaas = int(kaikkitaas)
			kakstuntii = False
			
		# Piirretään kuvaaja datasta
			
		graphRRD()

		# Nollataan luettu data
		
		x = ""
		time.sleep(1)

		
if __name__ == "__main__":
	main()
