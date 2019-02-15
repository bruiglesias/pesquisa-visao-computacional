import cv2
import numpy as np 
import imutils

#
#	Programa de Visao Computacional por Haar Cascade - OpenCV
#	Versao: 1.0
#	Autor: Bruno Pinheiro Iglesias
#	Contato: bruno.iglesias.eng@gmail.com
#
#	Descricao:
#	Programa para servir de base para construcoes mais complexas.
#
#	Este programa faz a deteccao por cor atraves uma webcam utilizando 
#	a biblioteca opencv bastando apenas mudar os parametros de interesse e remover os 
#	comentarios da funcao captura.
#
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

def captura():

	cap = cv2.VideoCapture(0)
    arquivo_cascade = cv2.CascadeClassifier('corpointeiro_cascade.xml')

	while(True):

		_,frame = cap.read()
		imagem = imutils.resize(frame, width=600)
	
		# detecta_por_haar_cascade(imagem, arquivo_cascade)

		cv2.imshow('Imagem Original', frame)
		cv2.imshow('Deteccao', imagem)
		
		k = cv2.waitKey(5) & 0xFF

    		if k == 27:
			    break
	cap.release()
	cv2.destroyAllWindows()
	

captura()