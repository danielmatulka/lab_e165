import serial


class VM8090:
    '''
    This class is used to handele the commuication with a Welleman VM8090 via Serial.
    minimal implementation without any read funktionality

    ...

    Attributes
    ----------
    port 
        Port the serial device is connected to

    Methods
    -------
    '''

    def __init__(self, port:str='COM1') -> None:

        self.stx = 0x04
        self.etx = 0x0f
        
        self.ser = serial.Serial(
            port='COM6',
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = 1
        )
    
    def _create_chk(self,cmd, mask, param1=0x00, param2=0x00):
        return (((~(0x04 + cmd + mask + param1 + param2)) + 0x01) & 0xff)
    
    def send_comand(self, cmd, mask, param1=0x00, param2=0x00):
        chk = self._create_chk(cmd, mask, param1, param2)
        send_string = bytes([self.stx, cmd, mask, param1, param2, chk, self.etx])
        print(send_string)
        self.ser.write(send_string)
    
        return self.ser.flush()
    
    def switch_relay_on(self, mask):
        self.send_comand(cmd=0x11,mask=mask)
    
    def switch_relay_off(self, mask):
        self.send_comand(cmd=0x12,mask=mask)
    
    def toggle_relay(self,mask):
        self.send_comand(cmd=0x14)
    
    def __del__(self):
        self.ser.close()