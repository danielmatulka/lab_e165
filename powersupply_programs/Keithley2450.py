from distutils.log import error
import pyvisa
import time
import pandas as pd
import numpy as np



class Keithley2450:
    '''
    This class is used to handele the commuication with a Keithley2450.

    ...

    Attributes
    ----------
    port 
        Port the device is connected to

    Methods
    -------
    '''

    def __init__(self, port:str=''):
        rm = pyvisa.ResourceManager()

        if port == '':
            self.port = rm.list_resources()[0]
        else:
            self.port = port

        self.sm = rm.open_resource(self.port)
        self.reset()
        
    def reset(self) -> None:
        self.sm.write('*RST')
        self.sens = 'current'
        self.source = 'voltage'
        self.two_wire = True
        self.enable = False
          
    def set_output_state(self, on_off:bool)-> None:
        if type(on_off) == bool or on_off == 1 or 0:
            self.sm.write(':OUTPut '+ str(int(on_off)))
            
    def set_output_state(self, on_off:bool)-> None:
        if type(on_off) == bool or on_off == 1 or 0:
            self.sm.write(':OUTPut '+ str(int(on_off)))

    def enable_output(self) -> None:
        """Activates the output. 

        """       
        self.set_output_state(True)
    
    def disable_output(self) -> None:
        """Disables the output. 

        """  
        self.set_output_state(False)

    def query_output_state(self):
        return self.sm.query_ascii_values(':OUTP?')

    def set_output_voltage(self, level:float) -> None:
        """Sets the output voltage in Volt.


        Parameters
        ----------
        level
            Voltage to be set in Volt
        """
        if self.source == 'voltage':
            self.sm.write('SOUR:VOLT '+ str(level))
        else:
            pass
    
    def set_output_current(self, level) -> None:
        """Sets the output current in Amper.

        Parameters
        ----------
        level
            Current to be set in Amper
        """
        if self.source == 'current':
            self.sm.write('SOUR:CURR '+ str(level))
        else:
            pass

    def set_wire(self, two_wire:bool = True) -> None:
        if two_wire == True:
            if self.sens == 'current':
                self.sm.write('SENS:CURR:RSEN OFF')
            else:
                self.sm.write('SENS:VOLT:RSEN OFF')

            self.two_wire = True

        if two_wire == False:
            if self.sens == 'current':
                self.sm.write('SENS:CURR:RSEN ON')
            else:
                self.sm.write('SENS:VOLT:RSEN ON')

            self.two_wire = False     
    
    def use_two_wire(self) -> None: 
        self.set_wire(two_wire=True)
    
    def use_four_wire(self) -> None:
        self.set_wire(two_wire=False)

    def sens_voltage(self) -> None:
        self.sm.write('SENS:FUNC "VOLT"')
        if self.sens != 'voltage':
            self.sens = 'voltage'
            self.two_wire = True

    def sens_current(self) -> None:
        self.sm.write('SENS:FUNC "CURR"')
        if self.sens != 'current':
            self.sens = 'current'
            self.two_wire = True
    
    def set_sens_range(self, range:float) -> None:
        if range == 'auto':
            if self.sens == 'voltage':
                self.sm.write('VOLT:RANG:AUTO ON')

            if self.sens == 'current':
                self.sm.write('CURR:RANG:AUTO ON')
        else:
            if self.sens == 'voltage':
                self.sm.write('VOLT:RANG '+str(range))

            if self.sens == 'current':
                self.sm.write('CURR:RANG '+str(range))
               
        self.sens_range = range
        
    def source_voltage(self, readback:bool = True) -> None:
        self.sm.write('SOUR:FUNC VOLT')
        if readback:
            pass
            #self.sm.write(':SOUR:VOLT:READ:BACK ' + str(int(readback)))
        self.source = 'voltage'
        self.readback = readback

    def source_current(self,readback:bool = True) -> None:
        self.sm.write('SOUR:FUNC CURR')
        if readback:
            pass
            #self.sm.write(':SOUR:CURR:READ:BACK?' + str(int(readback)))
        self.source = 'current'
        self.readback = readback

    def set_source_range(self, range:float) -> None:
        if range == 'auto' or type(range) == float or int:
            if self.source == 'voltage':
                self.sm.write('SOUR:VOLT:RANG '+ str(range))
            if self.source == 'current':
                self.sm.write('SOUR:CURR:RANG '+ str(range))
            else:
                pass
        else:
            pass
        self.source_range = range
    
    def set_source_limit(self,limit:float) -> None:
        if self.source == 'voltage':
            self.sm.write('SOUR:VOLT:ILIM '+ str(limit))
        if self.source == 'current':
            self.sm.write('SOUR:CURR:VLIM '+ str(limit))

        self.source_limit = limit

    def setup_sweep(self,function:str,start:float,stop:float,steps:int,delay:float=0.1,count:int=1,rangeType:str='BEST',failAbort:str='OFF',dual='OFF',bufferName:str='defbuffer1',sweep_type:str='linear') -> None:
        dict_types = {
            'linear':'LIN',
            'LIN':'LIN',
            'log':'LOG',
            'logarithmic':'LOG'
        }
        command_string = ''
        for i in [start, stop, steps, delay, count, rangeType, failAbort, dual]:
            command_string += str(i) + ', '
        command_string += '"' + str(bufferName) + '"'
        self.sm.write(':SOUR:SWE:'+ function +':' + dict_types[sweep_type] + ' ' + command_string)
    
    def setup_voltage_sweep(self,start:float,stop:float,steps:int,delay:float=0.1) -> None:
        self.setup_sweep('VOLT',start,stop,steps,delay)

    def setup_current_sweep(self,start:float,stop:float,steps:int,delay:float=0.1) -> None:
        self.setup_sweep('CURR',start,stop,steps,delay)

    def setup_cyclovoltammetrie(self,start:float,stop:float,steps:int,delay:float,cycles:int=1) -> None:
        self.setup_sweep('VOLT',start,stop,steps,delay,cycles,dual='ON')

    def initialise(self) -> None:
        self.sm.write('INIT')

    def elements_in_buffer(self, buffer:str='defbuffer1') -> None:
        return int(self.sm.query_ascii_values(':TRACe:ACTual? ' + '"' +str(buffer) + '"')[0])

    def read_buffer(self, buffer:str='defbuffer1', source:bool = True, reading:bool = True, sourceunit:bool = False, readingunit:bool = False, utc_sec:bool = False, status:bool = False) -> pd.DataFrame:

        timeout = 30 ## timout in sekunden ist abhänign von sm.timeout()
        while True:
            try:
                if self.sm.query_ascii_values('*OPC?') == [1]:
                    break
                else:
                    time.sleep(2)
                    timeout -= 1
                    if timeout == 0:
                        pass

            except:     
                if timeout == 0:
                    break

        elements = self.elements_in_buffer(buffer=buffer)
        bufferelements = ''
        return_index = []

        if source:
            bufferelements += 'SOUR, '
            return_index.append('Source')

        if sourceunit:
            bufferelements += 'SOURUNIT, '
            return_index.append('Sourceunit')

        if reading:
            bufferelements += 'READ, '
            return_index.append('Read')
        
        if readingunit:
            bufferelements += 'UNIT, '
            return_index.append('Readingunit')

        if utc_sec:
            bufferelements += 'SEC, '
            return_index.append('UTC_Time')

        if status:
            bufferelements += 'STAT, '
            return_index.append('Read_Status')
        
        bufferelements = bufferelements[:-2]
        
        if elements != 0:
            query = self.sm.query_ascii_values('TRAC:DATA? 1, ' + str(int(elements)) + ', "' + str(buffer) + '", ' + bufferelements)
            n = len(return_index)
            data_np = np.array(query).reshape(int(len(query)/n),n)
            return pd.DataFrame(data_np, columns=return_index)
        else:
            return []  
    
    def define_output_terminals(self,front:bool):
        if front:
            self.sm.write(':ROUT:TERM FRON')
        if not front:
            self.sm.write(':ROUT:TERM REAR')
        else:
            pass
    
    def use_front_terimals(self):
        self.define_output_terminals(True)
    
    def use_back_terminals(self):
        self.define_output_terminals(False)
    
    def eletrodeposition(self):
        pass
            
    def measure(self):
        return float(self.sm.query_ascii_values(':MEASure?')[0])


