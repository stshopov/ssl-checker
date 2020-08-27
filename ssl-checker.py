import os
import datetime
import argparse
from influxdb import InfluxDBClient
from OpenSSL import crypto


def get_cert_names(path):

    names = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".crt"):
                names.append(os.path.join(root, file))

    return names


def check_certs(cert_names):

    all_certs = {}

    for cert in cert_names:
        cert_name = cert.split('/')[-1]
        open_cert = open(cert, 'r')
        read_cert = open_cert.read()
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, read_cert)
        period = x509.get_notAfter().decode("utf-8")
        all_certs[cert_name] = datetime.datetime.strptime(period.split('Z')[0], "%Y%m%d%H%M%S")
        open_cert.close()

    return all_certs


def period_of_validity(date_info):

    today = datetime.datetime.today()
    cert_status = {}
    for name in date_info:
        period = date_info[name] - today
        period_in_days = period.days
        cert_status[name] = period_in_days

    return cert_status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbhost', type=str, help='Influx server ip address <35.134.1.221>')
    parser.add_argument('--influx_user', type=str, help='Influx user name <user>')
    parser.add_argument('--influx_pass', type=str, help='Influx user password <mega secret password>')
    parser.add_argument('--influx_port', type=str, help='Influx server port <8086>')
    parser.add_argument('--influx_database', type=str, help='Influx database name <test>')
    parser.add_argument('--crt_path', type=str, help='Path to your sites certificates </some/path>')
    parser.add_argument('--expiring_period', type=int, help='Expiring period in days <30>')
    args = parser.parse_args()
    path_certs = args.crt_path
    dbhost = args.dbhost
    influx_database = args.influx_database
    influx_user = args.influx_user
    influx_pass = args.influx_pass
    influx_port = args.influx_port
    expiring_period = args.expiring_period
    server_name = os.uname()[1]
    all_cert_names = get_cert_names(path_certs)
    checked_certs = check_certs(all_cert_names)
    all_certs = period_of_validity(checked_certs)

    client = InfluxDBClient(host=dbhost, port=influx_port, username=influx_user, password=influx_pass)

    for line in all_certs:
        if 0 < int(all_certs[line]) < expiring_period:
            data = ["{},host={},cert_name={} value={}".format("all_cert", server_name, line, float(all_certs[line]))]
            print(data)
            client.write_points(data, database=influx_database, time_precision='ms', batch_size=10000, protocol='line')


if __name__ == '__main__':
    main()
