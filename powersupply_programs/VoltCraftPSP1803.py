import serial


class VoltCraftPSP1803:
    '''
    This class is used to handele the commuication with a Voltcraft PSP1803 via Serial.

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
            baudrate=2400,
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
        
        send = b''
        send += b'\xaa'
        V = round(V*50)
        send += V.to_bytes(2, byteorder='big',signed=False)
        self.ser.write(send)

    def read_voltage(self) -> float:
        """Reads the set Volatge.

        Returns
        -------
        float
            Voltage in Volt
        """
        send = b''
        send += b'\xae'
        send += b'\x00'
        send += b'\x00'
        self.ser.reset_input_buffer()
        self.ser.write(send)
        return (int.from_bytes(self.ser.read(3)[1:3], byteorder='big')/50)

    def enable_output(self) -> None:
        """Activates the output. 

        """
        send = b''
        send += b'\xab'
        send += b'\x01'
        send += b'\x00' 
        self.ser.write(send)

    def disable_output(self) -> None:
        """Deactivate the output. 

        """
        send = b''
        send += b'\xab'
        send += b'\x00'
        send += b'\x00' 
        self.ser.write(send)
    
    def __del__(self):
        self.ser.close()