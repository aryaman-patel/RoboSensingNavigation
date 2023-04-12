# A helpful guide to my PA1 assignment

## Turtlesim:
The directory ``PA1/src/Images`` contains the relevant images showcasing the proofs of completion of the following tasks: 

1. Spawn a new robot with a fun name (Here's Bob):
![plot](PA1/src/Images/1.Spawn_Bob.png)

2. Changing the background color of the Turtlesim:
![plot](PA1/src/Images/2.Background_Change.png)

3. Create a fun doodle (I call it Picasso's Lost Art):
![plot](PA1/src/Images/3.Fun_doodle.png)

## Game of telephone:
The directory ``PA1/src/PA1/`` contains all the necessary files to run and verify this task. The files relevant to this tasks are, ``talker.py`` and ``listner.py``.
Here are how to run and verify the task:
1. Start the talker node (publisher) by the command:  
`` rosrun PA1 talker.py ``
2. Start the listner node (subscriber) by the command:  
`` rosrun PA1 listner.py ``

The input messages reads -  
`` "She sells sea shells on the sea shore."``  
The output messages has been modified to interchange the words, ``sea shells`` and ``sea shore``, which finally reads to -   
``  "She sells sea shore on the sea shells." ``

## Service:
The directory ``PA1/src/PA1/`` contains all the necessary files to run and verify this task. The files relevant to this tasks are, ``service_client.py`` and ``service_server.py``.
Here is how to run and verify the task:
1. Start the server node by the command:  
`` rosrun PA1 service_server.py ``
2. The client takes user arguments for the two ``floats`` to the multiplied.  
`` rosrun PA1 service_client.py <arg1> <arg2> ``  
Eg:  
`` rosrun PA1 service_client.py 1.2 3.4 ``  







