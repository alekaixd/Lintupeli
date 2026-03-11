                                                                                                                       
          ,--.                        ,--.  ,--.                             ,--.                                      
,--,--,--.`--' ,---. ,--.--. ,--,--.,-'  '-.`--' ,---. ,--,--,     ,--,--,--.`--' ,---. ,--.--. ,--,--.,--,--,  ,---.  
|        |,--.| .-. ||  .--'' ,-.  |'-.  .-',--.| .-. ||      \    |        |,--.| .-. ||  .--'' ,-.  ||      \| .-. : 
|  |  |  ||  |' '-' '|  |   \ '-'  |  |  |  |  |' '-' '|  ||  |    |  |  |  ||  |' '-' '|  |   \ '-'  ||  ||  |\   --. 
`--`--`--'`--'.`-  / `--'    `--`--'  `--'  `--' `---' `--''--'    `--`--`--'`--'.`-  / `--'    `--`--'`--''--' `----' 
              `---'                                                              `---'                                 

You are a bird migrating away from the deadly cold. Manage your energy and fly from location to location. Scavenge for food to raise your max energy or sleep to recharge all of your energy. Fly farther to get more score and reach your vacation home for the summer!

Dependencies: mysql-connector-python, geopy, bcrypt

Installing database for this project:

Open mariadb and execute the following commands:
```sql
create database bird_game;
Use "bird_game";
source full\path\to\yoursql\bird_game.sql;
```

Give rights for your mariadb user:
```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON bird_game.* TO username@localhost;
```
