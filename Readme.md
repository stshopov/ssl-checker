Python sript for chek ssl certificates validity period.

1. ssl-checker.py <br/>
2. Make virtualenvironment <br/>
    python3 -m venv /opt/VENVS/ssl-check <br/> 
3. Install influxdb and pyopenssl in this venv <br/>
    test-nginx-1: /opt/VENVS/ssl-check/bin/pip install influxdb pyopenssl <br/>
4. Move ssl-checker.py in /usr/local/bin <br/>
    sudo mv ssl-checker.py /usr/local/bin/ <br/>
5. Change mode of ssl-checker.py <br/>
    sudo chmode +x /usr/local/bin/ssl-checker.py <br/>
6. Create log file <br/>
    sudo touch /var/log/ssl-checker.log && sudo chmod 777 /var/log/ssl-checker.log <br/>
7. Add Pyton script in root crontab with correct arguments. <br/>
    sudo crontab -e <br/>
    0 0 * * * /opt/VENVS/ssl-check/bin/python3 /usr/local/bin/ssl-checker.py --dbhost 1.2.3.4 --influx_user <user> --influx_pass <password> --influx_port <port> --influx_database <dbname> --crt_path /etc/nginx/cert --expiring_period 30 >> /var/log/ssl-checer.log 2>&1 <br/>
