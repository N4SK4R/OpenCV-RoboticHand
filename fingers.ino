#include<Servo.h>
#define NUM_SERVOS 5

Servo servos[NUM_SERVOS];

void setup() 
{
  Serial.begin(9600);
  Serial.setTimeout(20);

  servos[0].attach(11);
  servos[1].attach(10);
  servos[2].attach(9);
  servos[3].attach(6);
  servos[4].attach(5);

  servos[0].write(0);
  servos[1].write(0);
  servos[2].write(0);
  servos[3].write(0);
  servos[4].write(0);


}

void loop() 
{

  if(Serial.available())
  {
    String input=Serial.readStringUntil('\n'); //buffer
    int len= input.length();

    char servoNames[NUM_SERVOS] = {'M', 'R', 'P', 'I', 'T'};

     for (int i = 0; i < len; i++) 
     {
      char c = input.charAt(i);
      if (isAlpha(c)) 
      { 
        for (int j = 0; j < NUM_SERVOS; j++) 
        {
          if (servoNames[j] == c && i + 1 < len && isDigit(input.charAt(i + 1))) 
          {
            int angle = input.substring(i + 1).toInt();
            servos[j].write(angle);
            break;
          }
        }
      }
    }
  }
}
  

