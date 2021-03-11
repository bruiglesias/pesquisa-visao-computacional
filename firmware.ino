#include <AccelStepper.h>

int velocidade_motor = 1500;
int aceleracao_motor = 1500;
int numero = 0;
int numeroAnterior = -1;
int positionAtual = 0;
int positionAnterior = 0;
int pino_enable = 10;
long distancia = 150000;
int retorno;

AccelStepper motor1(1, 7, 4 );


void calibraMotor()
{
  digitalWrite(pino_enable, LOW);
  motor1.moveTo(-10000);
  sentidoAntiHorario();
}

void parandoMotor()
{
  motor1.moveTo(0);
  digitalWrite(pino_enable, HIGH);
}

void sentidoHorario()
{
  digitalWrite(pino_enable, LOW);;
  motor1.moveTo(10000);

}

void sentidoAntiHorario()
{
  digitalWrite(pino_enable, LOW);
  motor1.moveTo(-10000);
}

void setup()
{
  Serial.begin(9600);
  pinMode(pino_enable, OUTPUT);
  motor1.setMaxSpeed(velocidade_motor);
  motor1.setSpeed(velocidade_motor);
  motor1.setAcceleration(aceleracao_motor);
}

void loop()
{

  if (Serial.available() > 0)
  {
    numero = Serial.read();


    if (numero == '1' && numero != numeroAnterior && positionAtual == 0)
    {
      if (positionAtual < 100)
      {
        sentidoHorario();
        positionAnterior = positionAtual;
        numeroAnterior = numero;
        positionAtual = positionAtual + 100; // move distancia + 100
      }

      if ( positionAtual >= 100)
      {
        positionAtual = 100;
      }

      distancia = 150000;
    }
    else if (numero == '1' && numeroAnterior != numero && positionAtual == 50)
    {
      if (positionAtual < 100)
      {
        sentidoHorario();
        numeroAnterior = numero;
        positionAnterior = positionAtual;
        positionAtual = positionAtual + 50; // move distancia + 50
      }

      if ( positionAtual >= 100)
      {
        positionAtual = 100;
      }

      distancia = 105000;;
    }
    else if (numero == '2' && numeroAnterior != numero && positionAtual == 100)
    {
      if (positionAtual > 0 )
      {
        sentidoAntiHorario();
        numeroAnterior = numero;
        positionAnterior = positionAtual;
        positionAtual = positionAtual - 100;  // move distancia - 100
      }

      if ( positionAtual < 0)
      {
        positionAtual = 0;
      }

      distancia = 150000;
    }

    else if (numero == '2' && numeroAnterior != numero && positionAtual == 50)
    {
      if (positionAtual > 0 )
      {
        sentidoAntiHorario();
        numeroAnterior = numero;
        positionAnterior = positionAtual;
        positionAtual = positionAtual - 50;  // move distancia - 50
      }

      if ( positionAtual < 0)
      {
        positionAtual = 0;
      }

      distancia = 105000;;
    }
    else if (numero == '3' && numeroAnterior != numero && positionAtual == 0 )
    {
      if (positionAtual < 100)
      {
        sentidoHorario();
        numeroAnterior = numero;
        positionAtual = positionAtual + 50; // move distancia + 50
      }

      if ( positionAtual >= 100)
      {
        positionAtual = 100;
      }

      distancia = 105000;
    }
    else if (numero == '3' && numeroAnterior != numero && positionAtual == 100)
    {
      if (positionAtual > 0)
      {
        numeroAnterior = numero;
        sentidoAntiHorario();
        positionAtual = positionAtual - 50; // move distancia - 50
      }

      if ( positionAtual <= 0)
      {
        positionAtual = 0;
      }
      distancia = 105000;
    }
    else if (numero == '9')
    {
      parandoMotor(); // Desliga o motor
    }


  }

  for (long i = 0; i < distancia; i++)
  {
    motor1.run();
  }

  parandoMotor();

}
