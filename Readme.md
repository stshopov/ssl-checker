Python sript for chek ssl certificates validity period.

1. ssl-checker.py <br/>
2. Make virtualenvironment <br/>
    python3 -m venv /opt/VENVS/ssl-check <br/> 
3. Activate it <br/>
    source /opt/VENVS/ssl-check/bin/activate <br/>
4. Install influxdb and pyopenssl in this venv <br/>
    (ssl-check) ctp-nginx-1-1:[/opt/VENVS/ssl-check]: pip install influxdb pyopenssl <br/>
5. Move ssl-checker.py in /usr/local/bin <br/>
    sudo mv ssl-checker.py /usr/local/bin/ <br/>
6. Change mode of ssl-checker.py <br/>
    sudo chmode +x /usr/local/bin/ssl-checker.py <br/>
7. Create log file <br/>
    sudo touch /var/log/ssl-checker.log && sudo chmod 777 /var/log/ssl-checker.log <br/>
8. Add Pyton script in root crontab with correct arguments. <br/>
    sudo crontab -e <br/>
    0 0 * * * /opt/VENVS/ssl-check/bin/python3 /usr/local/bin/ssl-checker.py --dbhost 34.102.212.233 --influx_user nginx --influx_pass <password> --influx_port 80 --influx_database nginx --crt_path /etc/nginx/cert --expiring_period 30 >> /var/log/ssl-checer.log 2>&1 <br/>
