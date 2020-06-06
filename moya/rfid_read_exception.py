class RfidReadException(Exception):
    def __init__(self):
        super().__init__('rfid card read error')