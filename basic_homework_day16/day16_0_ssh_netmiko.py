from netmiko import Netmiko
import hashlib


def netmiko_show_cred(host, username, password, cmd, enable='Cisc0123', ssh=True):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
                    'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        return net_connect.send_command(cmd)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')


def compute_hash(s, algorithm='sha256'):
    hash_object = hashlib.new(algorithm)
    hash_object.update(s.encode('utf-8'))
    return hash_object.hexdigest()


def get_show_run(host, username, password):
    show_run_raw = netmiko_show_cred(host, username, password, "show run")
    show_run = 'hostname ' + show_run_raw.split('\nhostname ')[1]

    return show_run, compute_hash(show_run)


if __name__ == '__main__':
    print(get_show_run("10.1.1.253", "admin", "Cisc0123"))

