# Wisdomcc

steps to Install and setup the server, basic run.
0. Pre Requsits 
    `sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl`
1. Create a Venv
    `python3 -m venv venv`
    `git clone https://github.com/livinghumanz/wisdomcc.git app`
2. install the dependencies 
    `pip install -r requirements.txt` -- need to wait until it succedes 
3. update the localsettings.py
4. install postgrees and other sudo related tools 
5. Login to postgres 
    `sudo -u postgres psql`
    1. Create a Database
        `CREATE DATABASE wisdomcc_db;`
    2. Create a Database User
        `CREATE USER wisdomcc WITH PASSWORD 'coldfeet1';`
    3. Alter the user to be a super user
        `alter user wisdomcc with Superuser;`
6. Make Migrations
    `python manage.py makemigrations`
7. Migrate
    `python manage.py migrate`
8. Create a super user
    `python manage.py createsuperuser`
9. collectstatic 
    `python manage.py collectstatic`

10. ssh 
    autossh -i "wisdomccPemKey.pem" -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 10" ubuntu@ec2-3-146-206-192.us-east-2.compute.amazonaws.com

    tmux new -s mysession
    Ctrl + B, then D
    tmux attach -t mysession
