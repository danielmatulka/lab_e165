import serial


class HCS3400:
    '''
    This class is used to handele the commuication with a Manson HCS-34xx via Serial.

    ...

    Attributes
    ----------
    port 
        Port the serial device is connected to

    Methods
    -------
    '''

    def __init__(self, port:str='COM1') -> None:
        
        self.ser = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = 1
        )
    
    def set_voltage(self,V:float) -> None:
        """Sets the outputvoltage in Volt.

        Parameters
        ----------
        V
            Voltage to be set in Volt
        """
        if V >= 10:
            send = 'VOLT' + str(V.round(1))
        elif V >= 1:
            send = 'VOLT0' + str(V.round(1))
        elif V >= 0:
            send = 'VOLT00' + str(V.round(1))
        else:
            print('input err') 
            pass

        self.ser.write(send.encode('ASCII'))
        if self.ser.readline() != 'OK':
            print('something wrong')

    def set_current(self,I:float) -> None:
        """Sets the outputvoltage in Volt.

        Parameters
        ----------
        I
            Curent to be set in Ampere
        """


    def read_voltage(self) -> float:
        """Reads the set Volatge.

        Returns
        -------
        float
            Voltage in Volt
        """
        pass

    def enable_output(self) -> None:
        """Activates the output. 

        """
        self.switch_output(1)

    def disable_output(self) -> None:
        """Deactivate the output. 

        """
        self.switch_output(0)

    def switch_output(self, value:int) -> None:
        """Activates/Deactivate the output. 

        """
        send = 'SOUT' + str(value)
        self.ser.write(send.encode('ASCII'))
        if self.ser.readline() != 'OK':
            print('something wrong')

    
    def __del__(self):
        self.ser.close()