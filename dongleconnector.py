import serial
import sys
import re
import yaml
import logging
import time
from time import sleep


class DongleConnection:

    def __init__(self):
        self.port = "COM4"
        self.sensor_serial = "28:2C:02:40:28:3C"
        self.key = "3925"
        self.retries_timeout = 3
        self.retries_seq = 3
        try:
            self.connection = serial.Serial(self.port,
                                            115200,
                                            parity=serial.PARITY_NONE,
                                            stopbits=serial.STOPBITS_ONE,
                                            rtscts=False,
                                            timeout=0)

        except serial.SerialException:
            logging.exception("Cannot open serial port: %s" % self.port)
            sys.exit(-1)

    def get_response(self):
        s1 = ""
        regexp = re.compile("efento-dongle*")
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cmd_send = False
        response_started = False
        while not regexp.search(s1):
            if self.connection.inWaiting() > 0:
                line = self.connection.read()

                if response_started or (line != b'\r' and line != b'\n'):
                    s1 += str(line, 'utf-8', 'ignore')

                if not cmd_send:
                    if self.lastCommand == s1:
                        cmd_send = True

                elif not response_started:
                    if line != b'.' and line != b'\r' and line != b'\n':
                        response_started = True
                        s1 = str(line, 'utf-8', 'ignore')

            sleep(0.001)
        s1 = s1[:s1.rfind('\n')]
        s1 = ansi_escape.sub('', s1)
        response = yaml.safe_load(s1)
        escape = re.compile(r'\r\n')
        s1 = escape.sub("\r", s1)
        if response['result'] == 'OK' or response['result'] == 'Not changed':
            # print(response)
            result = True
        else:
            # print(response['result'])
            result = False

        return result, response

    def execute(self, command):
        result = bool()
        response = []
        retry_counter_timeout = self.retries_timeout
        retry_counter_seq = self.retries_seq
        if retry_counter_timeout < 1 or retry_counter_seq < 1:
            exit(-1)
        while retry_counter_timeout > 0 and retry_counter_seq > 0:

            result, response = self.execute_command(command)
            if response['result'] == "Response timeout":
                retry_counter_timeout -= 1
                logging.debug("Remaining timeout retries: " + str(retry_counter_timeout) + "\n")
                time.sleep(2)
            elif response['result'] == "Command sequence error":
                retry_counter_seq -= 1
                logging.debug("Remaining sequence error retries: " + str(retry_counter_seq) + "\n")
                time.sleep(2)
            else:
                retry_counter_seq = 0
                retry_counter_timeout = 0

        return result, response

    def execute_command(self, command):
        serial_regex = re.compile("_SERIAL_")
        key_regex = re.compile("_KEY_")
        command = serial_regex.sub(self.sensor_serial, command)
        command = key_regex.sub(self.key, command)
        self.lastCommand = command
        print(command)
        command += "\r\n"

        while self.connection.inWaiting() > 0:
            self.connection.read()
        cmds = command.split(' ')
        for cmd in cmds:
            self.connection.write((cmd + " ").encode())
            time.sleep(0.01)
        self.connection.write("\r\n".encode())
        logging.debug((command.encode('UTF-8')[:-2]).decode('UTF-8'))
        return self.get_response()

    def close(self):
        self.connection.close()
