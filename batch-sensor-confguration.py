# before run program install pyyaml using command: pip install PyYAML(Windows) pip install pyyaml(Linux)
# before run program install pyserial using command: pip install pyserial(Windows, Linux)
import yaml

from dongleconnector import DongleConnection

sensor_list = [
    #    SERIAL NUMBER     PIN
    "28:2C:02:40:FF:FF 1111",
    "28:2C:02:40:FF:FF 1111",
    "28:2C:02:40:FF:FF 1111"
]


def main():
    command_name = 'sensor '
    dongle_connector = DongleConnection()
    dongle_connector.port = "COM4"  # write port

    for sensor in sensor_list:
        dongle_connector.sensor_serial = sensor[0:17]  # write sensor serial
        dongle_connector.key = sensor[18:23]  # write pin

        print("--------- Set and get sensor name")
        result = dongle_connector.execute(command_name + "connect _SERIAL_")
        if result:
            result = dongle_connector.execute(command_name + "set_name _SERIAL_ _KEY_ EfentoSensor")
            if result:
                result, response = dongle_connector.execute(command_name + "get_name _SERIAL_ _KEY_")
                if result:
                    print("Full response:", response);
                    print("Cloud token: ", response['name'])
                else:
                    print('Error on getting name')
            else:
                print("Setting name failed")

            print("--------- Set and get cloud token ")
            result = dongle_connector.execute(
                command_name + "set_cloud_token _SERIAL_ _KEY_ 1 abcd")
            if result:
                result, response = dongle_connector.execute(command_name + "get_cloud_token _SERIAL_ _KEY_ ")
                if result:
                    print("Full response:", response)
                    print("Cloud token: ", response['cloudToken'])
                else:
                    print('Error on getting cloud token')
            else:
                print("Error on setting cloud token")

            dongle_connector.execute(command_name + "disconnect")
        else:
            print('Error on connection')


if __name__ == '__main__':
    main()
