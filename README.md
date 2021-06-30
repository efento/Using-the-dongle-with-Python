# Using the dongle with Python


USB dongle allows users to communicate with Efento sensors over Bluetooth. All sensors Bluetooth features are available using the dongle.  

-   Avaiable commands are listed in "2020-06-30 Efento dongle Documentation.pdf"
-   All the commands start with “sensor” (e.g. “sensor scan 28:2C:02:4F:FF:90")
-   If you want to repeat the recent commands, press the arrow up key on the keyboard until you find the command you want to repeat
-   If you want to use another command with the same sensor, can use “-” dongle will put in its place the recently used sensor’s MAC address and PIN (e.g. “sensor scan - -“)
-   Sensor’s MAC address needs to have “:” between each segment
-   If you press TAB key while writing a command you will list all the commands, starting with the keyed in letters (e.g. typing “get_” and pressing TAB will list all the commands starting with “get_“)
-   If you want to list all the available commands along with the list of their parameters, type “sensor”
-   Dongle’s response is a YAML message, which always contains two fields: serial number and result
