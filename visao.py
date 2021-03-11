import cv2
import numpy as np 
import imutils
import serial

flag_a = False;
flag_b = False;
flag_c = False;

comunicacao = serial.Serial('/dev/ttyACM0', 9600)
def escreve(imagem, texto, posixao_x, posixao_y, cor = (255, 0, 0)):
	fonte = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(imagem, texto, (posixao_x, posixao_y), fonte, 0.5, cor, 0, cv2.LINE_AA)

# fim da funcao escreve

def detecta_por_cor(imagem, cor):

	global posicao_atual 
	global posicao_anterior

	if cor == 'verde':
		limite_inferior = np.array([40, 100,  100])
		limite_superior = np.array([80, 255, 255])
	elif cor == 'azul':
		limite_inferior = np.array([100, 100, 100])
		limite_superior = np.array([140, 255, 255])
	elif cor == 'amarelo':
		limite_inferior = np.array([10, 100, 100])
		limite_superior = np.array([50, 255, 255])
	elif cor == 'vermelho':
		limite_inferior = np.array([160, 100, 100])
		limite_superior = np.array([200, 255, 255])

	imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

	matiz, saturacao, valor = cv2.split(imagem_hsv)
	imagem_hsv = cv2.merge((matiz, saturacao, valor))

	imagem_segmentada = cv2.inRange(imagem_hsv, limite_inferior, limite_superior)

	elemento_estruturante = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
	imagem_primeiro_tratamento = cv2.morphologyEx(imagem_segmentada, cv2.MORPH_OPEN, elemento_estruturante)
	imagem_segundo_tratamento = cv2.morphologyEx(imagem_primeiro_tratamento, cv2.MORPH_CLOSE, elemento_estruturante)

	
	modo  = cv2.RETR_TREE
	metodo = cv2.CHAIN_APPROX_SIMPLE

	contornos, hierarquia = cv2.findContours(imagem_segundo_tratamento, modo, metodo)

	if len(contornos) > 0:
		contorno = contornos[0]
		posicao_x, posicao_y, largura, altura = cv2.boundingRect(contorno)
		posicao_x = posicao_x - 20
		posicao_y = posicao_y - 20
		imagem = cv2.rectangle(imagem, (posicao_x, posicao_y), (posicao_x+largura+40, posicao_y+altura+40), (0,255,0), 3)
		(posicao_a, posicao_b), raio = cv2.minEnclosingCircle(contorno)
		centro = (int(posicao_a), int(posicao_b))
		imagem = cv2.circle(imagem, centro, 10, (0,0,255), -1)

		if posicao_a < 200:
			escreve(imagem, 'Objeto detectado na esquerda', 10, 20, cor=(0,255,0))
			global flag_a
			global flag_b
			global flag_c
			if flag_a == False:
				comunicacao.write(b'2')
				flag_a = True
				flag_b = False
				flag_c = False
		elif posicao_a > 200 and posicao_a < 400:
			escreve(imagem, 'Objeto detectado no centro', 10, 20, cor=(0,255,0))

			if flag_b == False:
				comunicacao.write(b'3')
				flag_b = True
				flag_a = False
				flag_c = False
		else:
			escreve(imagem, 'Objeto detectado na direita', 10, 20, cor=(0,255,0))

			if flag_c == False:
				comunicacao.write(b'1')
				flag_c = True
				flag_a = False
				flag_b = False


# fim da funcao detecta por cor

def captura():
	cap = cv2.VideoCapture(0)

	while(True):

		_, frame = cap.read()
		imagem = imutils.resize(frame, width = 600)

		detecta_por_cor(imagem, 'verde')

		#cv2.imshow('Imagem Original', frame)
		cv2.imshow('Deteccao', imagem)

		k = cv2.waitKey(5) & 0xFF

		if k == 27:
			break

	cap.release()
	cv2.destroyAllWindows()

captura()
