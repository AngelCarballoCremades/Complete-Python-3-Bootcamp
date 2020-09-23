'''
Milestone Project 2
BlackJack
'''

from random import shuffle
import os

palos = ["Corazones","Diamantes","Tréboles","Picas"]
numeros = ['Dos','Tres','Cuatro','Cinco','Seis','Siete','Ocho','Nueve','Diez','Joto','Quina','Rey','As']
valor = {'Dos':2,'Tres':3,'Cuatro':4,'Cinco':5,'Seis':6,'Siete':7,'Ocho':8,'Nueve':9,'Diez':10,'Joto':10,'Quina':10,'Rey':10,'As':11}

class Carta():
	"""Clase para una carta de la baraja"""
	def __init__(self, numero, palo):
		self.numero = numero
		self.palo = palo
		self.valor = valor[numero]

	def __str__(self):
		return self.numero + ' de ' + self.palo

class Baraja():
	"""Baraja de Cartas"""
	def __init__(self):
		self.contenido = []

		for palo in palos:
			for numero in numeros:
				self.contenido.append(Carta(numero,palo))

	def __str__(self):
		string = ''
		for carta in self.contenido:
			string += str(carta) + '\n'
		return string

	def mezclar(self):
		shuffle(self.contenido)

	def repartir(self):
		return self.contenido.pop()

	def vaciar(self):
		self.contenido = []

	def valor_mano(self):
		suma = 0
		for carta in self.contenido:
			suma += carta.valor
		self.valor = suma
		return suma

	def hay_as(self):
		for carta in self.contenido:
			if carta.numero == 'As':
				return True
			else:
				pass
		return False



	def __str__(self):
		string = ''
		for carta in self.contenido:
			string += str(carta) + '\n'
		return string

class Jugador():
	"""Jugador de Blackjack, con nombre y cuenta de dinero"""
	def __init__(self):
		self.nombre = input('¿Cuál es tu nombre?  ')

		respuesta = 0
		while True:
			respuesta = input('¿Con cuánto dinero entrarás a la mesa?  ')
			try:
				if int(respuesta) >= 10:
					self.dinero = int(respuesta)
				else:
					print('El monto mínimo de entrada a la mesa es $10, intenta de nuevo.')
			except:
				print('Valor no válido, por favor intenta de nuevo.')
			else:
				if self.dinero >= 10:
					break

		print(f'\nBienvenidx al casino, {self.nombre}, tienes ${self.dinero} en fichas, ¡Suerte!\n')

	def __str__(self):
		return f'{self.nombre}, tienes ${self.dinero} en fichas.'

	def apostar(self,minima):
		"""Apuesta del jugador"""
		self.apuesta = 0
		# print(f"{self.nombre}, tienes ${self.dinero}.")
		while True:
			respuesta = input('¿Cuánto apuestas para esta ronda?   ')
			try:
				if int(respuesta) >= minima and int(respuesta) <= self.dinero:
					self.apuesta = int(respuesta)
					self.dinero -= int(respuesta)
				
				elif int(respuesta) < minima:
					print('La apuesta mínima es $1.\n')
				
				elif int(respuesta) > self.dinero:
					print(f'La apuesta máxima es ${self.dinero}.\n')
			except:
				print('Valor no válido, por favor intenta de nuevo.\n')
			else:
				if self.apuesta >= minima and self.apuesta <= self.dinero+self.apuesta:
					break
		print(f'\nHas apostado ${self.apuesta}.\n')		

def mostrar_mesa(manoj,manod,turno_dealer):
	'''Función para imprimir lo que hay en la mesa,	cartas de dealer y jugador.'''
	print('\nCartas sobre la mesa:')
	if turno_dealer:
		print('Cartas del dealer:')
		for carta in range(len(manod.contenido)):
			print(manod.contenido[carta])
	
		print(f'Valor de mano = {manod.valor}\n')
	
	else:
		print(f'\nEl dealer tiene: {manod.contenido[0]} y una carta oculta.')
	
	print(f'\nTus cartas son:')
	
	for carta in range(len(manoj.contenido)):
		print(manoj.contenido[carta])
	
	print(f'Valor de mano = {manoj.valor}\n')
		
def clear():
	os.system('cls')


# Crear baraja y mezclar
clear()

mano_jugador = Baraja()
mano_dealer = Baraja()

# Preguntar nombre y dinero de entrada a jugador
jugador1 = Jugador()

# Comienza juego
jugando = True
apuesta_minima = 1
while jugando:
	
	empate = False

	baraja = Baraja()
	baraja.mezclar()
	
	mano_dealer.vaciar()
	mano_jugador.vaciar()

	# Preguntar apuesta

	jugador1.apostar(apuesta_minima)

	input('Repartiendo...')

	# Repartir a jugador y a dealer
	mano_jugador.contenido.append(baraja.repartir())
	mano_jugador.contenido.append(baraja.repartir())
	mano_dealer.contenido.append(baraja.repartir())
	mano_dealer.contenido.append(baraja.repartir())

	mano_jugador.valor_mano()
	mano_dealer.valor_mano()

	mostrar_mesa(mano_jugador,mano_dealer,False)

	# Ciclo de jugador pidiendo cartas
	jugador_gana = False 
	jugador_pasado = False
	turno_jugador = True
	empate = False
	otra = ''
	print(f"Tu turno, {jugador1.nombre}")
	while turno_jugador:

		# Jugador pide cartas
		otra = input('\n¿Quieres otra carta? (si/no):   ')
		if otra != 'no' and otra != 'si':
			print('Respuesta inválida.')
			continue

		if otra == 'no':
			turno_jugador = False

		elif otra == 'si':
			mano_jugador.contenido.append(baraja.repartir())
			print(f'Te ha salido: {mano_jugador.contenido[-1]}')

			if mano_jugador.valor_mano() > 21 and mano_jugador.hay_as():
				print(f'Valor de mano = {mano_jugador.valor_mano()-10}')
				mano_jugador.valor -= 10
			else:
				print(f'Valor de mano = {mano_jugador.valor_mano()}')

			if mano_jugador.valor >21:
				print("Te has pasado de 21, perdiste la ronda.")
				turno_jugador = False
				jugador_pasado = True

	turno_dealer = True

	if jugador_pasado:
		turno_dealer = False

	if turno_dealer:
		mostrar_mesa(mano_jugador,mano_dealer,True)
		input()
		
		print(f"Turno del dealer")
		input()

	while turno_dealer:

		if mano_dealer.valor_mano() > 21 and mano_dealer.hay_as():
				mano_dealer.valor -= 10

		if mano_dealer.valor > mano_jugador.valor:
			print('El dealer ha ganado.')
			turno_dealer = False

		else:
			mano_dealer.contenido.append(baraja.repartir())
			print(f'Al dealer le ha salido: {mano_dealer.contenido[-1]}')

			if mano_dealer.valor_mano() > 21 and mano_dealer.hay_as():
				mano_dealer.valor -= 10

			print(f'Valor de mano = {mano_dealer.valor}')

			if mano_dealer.valor < mano_jugador.valor:
				input()
				continue

			elif mano_dealer.valor == mano_jugador.valor:
				print('¡Es un empate!')
				turno_dealer = False
				empate = True
				input()

			elif mano_dealer.valor >21:
				print("El dealer se ha pasado de 21, ganaste la ronda!")
				turno_dealer = False
				jugador_gana = True
				input()

			elif mano_dealer.valor > mano_jugador.valor:
				print('El dealer ha ganado la ronda')
				turno_dealer = False
				input()

			else:
				print('Error en comparación turno dealer')

	if jugador_gana:
		jugador1.dinero += 2*jugador1.apuesta

	if empate:
		jugador1.dinero += jugador1.apuesta

	jugador1.apuesta = 0
	print(f'{jugador1.nombre}, tienes ${jugador1.dinero} en fichas')

	if jugador1.dinero <= 0:
		print('No tienes más dinero para apostar, gracias por jugar, perdedor...')
		break

	if input('¿Seguir jugando?  (si/no)  ') == 'si':
		jugando = True
		print("--------------------------------------------")
	else:
		print("¡Gracias por jugar!")
		jugando = False


		# Revisar si se pasó el jugador
			# Revisar si una de sus cartas es As y cambiar valor

	# Dealer pide cartas hasta que se pasó o le gana a jugador
		# Dealer pide cartas

		# Revisar si ya pasó al jugador y si se pasó
			# Revisar si una de sus cartas es As y cambiar valor

	# Pagar o cobrar apuesta

	# Continúa el juego o se retira?
	































