class Candle:
    
    def __init__(self, op, high, low, clse, volume, open_time, tstamp):
        self._op = op
        self._high = high
        self._low = low
        self._clse = clse
        self._volume = volume
        self._open_time = open_time
        self._tstamp = tstamp
    
    def __str__(self) -> str:
        return f"open_time': {self._open_time}, 'timestamp': {self._tstamp}, 'open': {self._op}, 'high': {self._high}, 'low': {self._low}, 'close': {self._clse}"
    
        
    # GETTERS
    @property
    def op(self):
        return self._op
    
    @property
    def high(self):
        return self._high
    
    @property
    def low(self):
        return self._low
    
    @property
    def clse(self):
        return self._clse
    
    @property
    def volume(self):
        return self._volume
    
    @property
    def open_time(self):
        return self._open_time
    
    @property
    def tstamp(self):
        return self._tstamp