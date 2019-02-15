import cv2
import numpy as np 
import imutils

#
#	Programa de Visao Computacional - OpenCV
#	Versao: 1.0
#	Autor: Bruno Pinheiro Iglesias
#	Contato: bruno.iglesias.eng@gmail.com
#
#	Descricao:
#	Programa para servir de base para construcoes mais complexas.
#
#	Este programa implementa varias funcoes de deteccao de objetos/pessoas
#	de uma webcam utilizando a biblioteca OpenCV como por exemplo deteccao 
#	por cor ou deteccao por Haar Cascade, bastando apenas mudar os parametros 
#	de interesse e remover os comentarios da funcao captura.
#
#	Para deteccao por cor:
# 	1 - Remover do comentario a chamada da funcao detecta_por_cor dentro da funcao captura
#	2 - Passar como parametro a imagem e a cor de interesse. 
#	Ex: detecta_por_cor(imagem, 'vermelho')
#	Cores possiveis: azul, amarelo, verde, vermelho
#
#	Para deteccao por haar cascade:
#	1 - Carregar local do arquivo haar cascade para a varivel arquivo_cascade e
#	2 - Remover do comentario a chamada da funcao detecta_por_haar_cascade na funcao captura 
#	3 - Passar como parametro a imagem e o arquivo haar cascade.
# 	ex: detecta_por_haar_cascade(imagem, arquivo_cascade)
#
#	Limitacoes:
#	Usar ambiente bem iluminado e fundo de cor uniforme para melhorar a deteccao.
#	Pode ocorrer falsos positivos
#
#	Programa de uso livre desde que matidos estes comentarios.
#


def escreve(imagem, texto, posisao_x, posisao_y, cor=(255,0,0)):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imagem, texto, (posisao_x,posisao_y), fonte, 0.5, cor, 0, cv2.LINE_AA)


def detecta_por_haar_cascade(imagem, arquivo_cascade):
	imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
	deteccao = arquivo_cascade.detectMultiScale(imagem_cinza, 1.1, 3)
	for (posisao_x, posisao_y, largura, altura) in deteccao:
		cv2.rectangle(imagem, (posisao_x, posisao_y), (posisao_x+largura, posisao_y+altura), (255,0,0), 2)
		centro_deteccao = (posisao_x+(largura/2), posisao_y+(altura/2))
		cv2.circle(imagem, centro_deteccao, 10, (0,0,255),-1)


def detecta_por_cor(imagem, cor):

	if cor == 'verde':
		limite_inferior = np.array([40,100,100]) 
		limite_superior = np.array([80,255,255])
	elif cor == 'azul':
		limite_inferior = np.array([100,100,100]) 
		limite_superior = np.array([140,255,255])
	elif cor == 'amarelo':
		limite_inferior = np.array([10,100,100]) 
		limite_superior = np.array([50,255,255])
	elif cor == 'vermelho':
		limite_inferior = np.array([160,100,100]) 
		limite_superior = np.array([200,255,255])

	imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

	matiz, saturacao, valor = cv2.split(imagem_hsv)
	imagem_hsv = cv2.merge((matiz, saturacao, valor + 20))

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
	

def captura():

	cap = cv2.VideoCapture(0)

	arquivo_cascade = cv2.CascadeClassifier('corpointeiro_cascade.xml')

	while(True):

		_,frame = cap.read()
		imagem = imutils.resize(frame, width=600)
	
		# detecta_por_haar_cascade(imagem, arquivo_cascade)
		detecta_por_cor(imagem, 'amarelo')

		cv2.imshow('Imagem Original', frame)
		cv2.imshow('Deteccao', imagem)
		
		k = cv2.waitKey(5) & 0xFF

    		if k == 27:
				break
	cap.release()
	cv2.destroyAllWindows()
	

captura()
