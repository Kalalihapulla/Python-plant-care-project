# main.py -- put your code here!
from pyb import LED
from pyb import Pin, ADC
from pyb import I2C
from pyb import UART
from pyb import delay
import math
import time

	#Interpoloi lämpötilan annettujen resistanssipisteiden välillä
def interpolointi(x1,x2,y1,y2,resistanssi):
	ltila=((y1-y2)/(x1-x2)*(resistanssi-x1))+y1
	return ltila	

	#Suorittaa 1000-ms pituisen kastelun avaamalla releellä ohjatun venttiilin.
def kastelu():	
	p_out = Pin('X11', Pin.OUT_PP)
	p_out.high()
	pyb.delay(1000)
	p_out.low()
	
	#Tarkistaa kosteusanturilta saatavan arvon ja suorittaa kastelun mikäli arvo on haluttu. laskee kastelukerrat.
def kasteluTarkistus(kosteus, kastelukerrat):
	if kosteus >= 1850:
		kastelu()
		kastelukerrat = kastelukerrat + 1
	return kastelukerrat
		
		
	#Määrittelee tuulettimen toiminnan ja käynnistää sen.
def tuuletus():
	p_tuuletin = Pin('Y8', Pin.OUT_PP)
	p_tuuletin.high()

	p_tuuletin1 = Pin('Y7', Pin.OUT_PP)
	p_tuuletin1.high()

	p_tuuletin2 = Pin('Y6', Pin.OUT_PP)
	p_tuuletin2.low()
	
	#Vastaanottaa arvon analogi-digitaali konvertterilta ja laskee saadun resistanssin avulla lämpötilan celsius-asteissa.
def ltilaMittaus():
	adc = ADC(Pin('X1'))
	tulos = adc.read()
	resistanssi = ((((tulos/4095)*3.3)*1.78)/(3.3-((tulos/4095)*3.3))*1000)

	if (resistanssi < 1603):
		ltila = 0
		
	elif (resistanssi >= 1603) and (resistanssi <= 1797):
		ltila = interpolointi(1797,1603,10,0,resistanssi)

	elif (resistanssi > 1797) and (resistanssi <= 1944):
		ltila = interpolointi(1944,1797,20,10,resistanssi)
		
	elif (resistanssi > 1944) and (resistanssi <= 2020):
		ltila = interpolointi(2020,1944,25,20,resistanssi)

	elif (resistanssi > 2020) and (resistanssi <= 2102):
		ltila = interpolointi(2102,2020,30,25,resistanssi)
	
	return ltila

	#Määrittelee valoanturin toiminnan ja lukee arvot anturilta. Laskee valon intensiteetin saatujen arvojen perusteella.	
def luxMittaus():		
	i2c = I2C(1,I2C.MASTER,baudrate = 100000)
	i2c.send(0x49,0x39)
	luettu = i2c.recv(1,0x39)
	i2c.send(0x83,0x39)
	luettu2 = i2c.recv(1,0x39)
	chord = (luettu[0] >> 4) & 7
	chord2 = (luettu2[0] >> 4) & 7
	step = (luettu[0]) & 15
	step2 = (luettu2[0]) & 15
	countvalue = (int(16.5*((2**chord)-1))+(step*(2**chord)))
	countvalue2 = (int(16.5*((2**chord2)-1))+(step2*(2**chord2)))
	luxit = (countvalue*0.46*(math.exp((-3.13*countvalue2/countvalue))))
	print("Valon intensiteetti on:",luxit,"luxia.")
	return luxit

	#Määrittelee kosteusanturin toiminnan ja mittaa arvon anturilta.
def kosteusMittaus():
	adc2 = ADC(Pin('X7'))
	kosteus = adc2.read()
	kosteus = float(kosteus)
	return kosteus
	
	#Kutsuu tuuletuksen suorittavaa funktiota lämpötilan ollessa yli halutun arvon.
def tuuletusTarkistus():
	if ltilaMittaus() >= 21.5:
		tuuletus()

	#Suorittaa tietojen keräämistä ja lähettämistä Raspille kahden minuutin pituisissa silmukoissa
def main():	
	p_tuuletin = Pin('Y8', Pin.OUT_PP)
	p_tuuletin1 = Pin('Y7', Pin.OUT_PP)
	p_tuuletin2 = Pin('Y6', Pin.OUT_PP)
	
	tuuletus()
	p_tuuletin.low()
	
	kastelukerrat = 0
	
	while True:		
		ltila = ltilaMittaus()
		
		luxit = luxMittaus()
		
		kosteus = kosteusMittaus()
		
		tuuletusTarkistus()
		
		kastelukerrat = kasteluTarkistus(kosteus, kastelukerrat)
		
		print("Kosteus:",kosteus)
		print("Kasteltu", kastelukerrat, "kertaa")
		print("Lämpötila on",ltila, "°C.")
		
		uart = UART(6, 115200)
		uart.write(str(ltila)+":"+str(luxit)+":"+str(kosteus)+":"+str(kastelukerrat)+"\r\n")
		
		if kastelukerrat > 35:
			kastelukerrat = 0
		
		pyb.delay(5000)
		p_tuuletin.low()
		pyb.delay(100)
	
if __name__ == "__main__":
	main()

	
	
	

			
		
