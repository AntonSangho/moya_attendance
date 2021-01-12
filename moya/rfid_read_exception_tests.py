import queue
from rfid_read_exception import RfidReadException

q = queue.Queue()

def RfidReadExceptionTest():
    for x in range(5):
        try:
            print('rfid 에러 발생')
            raise RfidReadException()
        except Exception as e:
            print('예외가 발생했습니다.', e)
            q.put(e)
    print(x)
    print(list(q.queue))

def rfid_read_chk():
    RfidReadExceptionTest()
    for verify in list(q.queue):
        print(verify)
        print(type(verify))
        if type(verify) == RfidReadException :
            print('queue 안에 에러가 있습니다')

rfid_read_chk()