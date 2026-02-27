# Bird game
Migration game

Installing database for this project:
Open mariadb and execute the following commands:
```sql
create database bird_game;
Use "bird_game";
source:full\path\to\yoursql\bird_game.sql;
```

Give rights for your mariadb user:
```sql
GRANT SELECT, INSERT, UPDATE ON bird_game.* TO username@localhost;
```