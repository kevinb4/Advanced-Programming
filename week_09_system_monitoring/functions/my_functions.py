import json
import psutil
import smtplib
from datetime import datetime
from twilio.rest import Client

def alert_check(config):
    """Returns all of the data checked for alerts
    Arguments:
        config [dict] -- the config file"""
    alerts = {}

    cpu = psutil.cpu_percent()
    # when a CPU core is over 85%
    if cpu > 85:
        alerts["cpu"] = cpu

    ram = psutil.virtual_memory().percent
    # when memory usage is over 90%
    if ram > 90:
        alerts["ram"] = ram
    
    volumes = []
    # when a disk usage on a volune is over 70%
    for volume in psutil.disk_partitions():
        # check if volume is ready/available (empty disk drives such as cd/dvd/blueray will cause errors without this check)
        if volume.fstype == "":
            continue

        if psutil.disk_usage(volume[1]).percent > 70:
            volumes.append({ "name": volume.device, "percent": psutil.disk_usage(volume[1]).percent })

    if len(volumes) > 0:
        alerts["disk"] = volumes

    errin = psutil.net_io_counters().errin
    errout = psutil.net_io_counters().errout
    # when errors and dropped packets are appearing on the network
    if errin > 0:
        alerts["network_in"] = errin

    if errout > 0:
        alerts["network_out"] = errout

    # handle the alerts if there are any
    if len(alerts) > 0:
        handle_alerts(alerts, config)

def build_cpu_string(cpu_usage):
    """Builds a string of the CPU usage for each core
    Arguments:
        cpu_usage [dict] -- the CPU usage for each core
    Returns:
        disk_string [string] -- the formatted CPU usage for each core"""
    cpu_string = ""

    for cpu in cpu_usage:
        cpu_string += f"\t{cpu}: {cpu_usage[cpu]}\n"

    return cpu_string[:-1]

def build_disk_string(disk_usage):
    """Builds a string of the disk usage for each volume"""
    disk_string = ""

    for volume in disk_usage:
        disk_string += f"\t{volume}\n"
        disk_string += f"\t  - {disk_usage[volume]['used']}% used\n"
        disk_string += f"\t  - {disk_usage[volume]['free']} GB free\n"
        disk_string += f"\t  - {disk_usage[volume]['total']} GB total\n\n"

    return disk_string[:-2]

def get_all_stats():
    """Returns all of the required stats
    Returns:
        data [dict] -- the required stats"""
    data = {}

    # get the current CPU usage by each and every CPU core
    cpus = psutil.cpu_percent(interval=.1, percpu=True)
    cpu_usage = {}
    count = 1
    for cpu in cpus:
        cpu_usage[f"cpu_{count}"] = f"{cpu}%"
        count += 1
    
    data['cpu_usage'] = cpu_usage

    # get the current RAM usage percent
    data['ram_percent'] = psutil.virtual_memory().percent
    # get the current RAM usage in GB
    data['ram_used'] = round(psutil.virtual_memory().used / 1024 ** 3, 2)
    # get the totoal amount of RAM in GB
    data['ram_total'] = round(psutil.virtual_memory().total / 1024 ** 3, 2)

    # get used and free disk space in GB for each volume
    disk_usage = {}
    for volume in psutil.disk_partitions():
        # check if volume is ready/available (empty disk drives such as cd/dvd/blueray will cause errors without this check)
        if volume.fstype == "":
            continue

        disk_usage[volume.device] = {
            "free": round(psutil.disk_usage(volume[1]).free / 1024 ** 3, 2),
            "total": round(psutil.disk_usage(volume[1]).total / 1024 ** 3, 2),
            "used": psutil.disk_usage(volume[1]).percent
        }
    
    data['disk_usage'] = disk_usage

    # get the bytes sent and received
    data['bytes_sent'] = psutil.net_io_counters().bytes_sent
    data['bytes_received'] = psutil.net_io_counters().bytes_recv

    # get number of in/out errors
    data['network_error_in'] = psutil.net_io_counters().errin
    data['network_error_out'] = psutil.net_io_counters().errout

    # get number of dropped packets
    data['network_drop_in'] = psutil.net_io_counters().dropin
    data['network_drop_out'] = psutil.net_io_counters().dropout

    return data

def handle_alerts(alerts, config):
    """Handles all alerts
    Arguments:
        alerts [list] -- the alerts to handle
        config [dict] -- the config file"""
    time = datetime.now().strftime('%B %d, %Y %H:%M:%S').replace(' 0', ' ')

    try:
        # convert the last sent time to a datetime object
        last_sent = datetime.strptime(config['last_text'], '%B %d, %Y %H:%M:%S')

        # if the last text was sent less than 1 hour ago, don't send another text
        if (datetime.now() - last_sent).seconds < 3600:
            print(f"Text was not sent because it was sent less than 1 hour ago")
            return
    except:
        pass # this means it's the first time sending, so it's fine to keep going

    message = "ALERT!"
    for key, value in alerts.items():
        if key == "cpu":
            message += f"\n{time} - CPU is at {value}%, which is over 85%"
        elif key == "ram":
            message += f"\n{time} - RAM is at {value}%, which is over 90%"
        elif key == "disk":
            for volume in value:
                message += f"\n{time} - Disk {volume['name']} usage is {volume['percent']}%, which is over 70%"
        elif key == "network_in":
            message += f"\n{time} - Network in errors are appearing ({value} errors)"
        elif key == "network_out":
            message += f"\n{time} - Network out errors are appearing ({value} errors)"

    tw = Client(config['twilio_account_id'], config['twilio_auth_token'])

    tw.messages.create(body=message, from_=config['twilio_trial_number'], to=config['twilio_cell_number'])

    config['last_text'] = time
    
    with open('text_files/script_config.json', 'w') as config_file:
        json.dump(config, config_file)

def handle_email_report(config):
    """Handles the email report
    Arguments:
        config [dict] -- the config file"""
    data = get_all_stats()

    smtp = smtplib.SMTP(config['mail_server'], config['mail_port'])
    smtp.ehlo()
    smtp.starttls()

    smtp.login(config['username'], config['password'])

    message = """"From: """ + str(config['from_email']) + """
Subject: System Monitoring Report

    CPU Usage:
        """ + str(build_cpu_string(data['cpu_usage'])) + """

    RAM Usage:
        """ + str(data['ram_used']) + """ GB used
        """ + str(data['ram_total']) + """ GB total
        """ + str(data['ram_percent']) + """%

    Disk Usage:
        """ + str(build_disk_string(data['disk_usage'])) + """

    Internet Usage:
        Data Usage:
            """ + str(data['bytes_sent']) + """ bytes sent
            """ + str(data['bytes_received']) + """ bytes received

        Network Errors:
            """ + str(data['network_error_in']) + """ errors in
            """ + str(data['network_error_out']) + """ errors out

        Dropped Packets:
            """ + str(data['network_drop_in']) + """ dropped packets in
            """ + str(data['network_drop_out']) + """ dropped packets out
    """

    smtp.sendmail(config['from_email'], config['to_email'], message)
    smtp.close()