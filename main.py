# before run program install pyyaml using command: pip install PyYAML(Windows) pip install pyyaml(Linux)
# before run program install pyserial using command: pip install pyserial(Windows, Linux)

from dongleconnector import DongleConnection


def main():
    command_name = 'sensor '
    dongle_connector = DongleConnection()
    dongle_connector.port = "COM4"  # write port
    dongle_connector.sensor_serial = "28:2C:02:40:FF:FF"  # write sensor serial
    dongle_connector.key = "1111"  # write pin
    dongle_connector.execute(command_name + "connect _SERIAL_")
    dongle_connector.execute(command_name + "set_name _SERIAL_ _KEY_ EfentoSensor")
    dongle_connector.execute(command_name + "get_name _SERIAL_ _KEY_")
    dongle_connector.execute(command_name + "set_cloud_token _SERIAL_ _KEY_ 1 abcd")
    dongle_connector.execute(command_name + "get_cloud_token _SERIAL_ _KEY_ ")


if __name__ == '__main__':
    main()
