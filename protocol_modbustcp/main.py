import time
from pyModbusTCP.client import ModbusClient

c = ModbusClient(host="192.168.1.222", port=502, unit_id=1, auto_open=True)


angleToSet = int(input("Angle to set:"))
regs = c.write_single_register(1001,angleToSet)


while(True):
    if(regs != angleToSet):
        regs = c.read_holding_registers(1002,1)[0]
        print("Angle: ",regs)
    else:
        angleToSet = int(input("Angle to set:"))
        if angleToSet == 360:
            angleToSet = 0
        regs = c.write_single_register(1001,angleToSet)
    time.sleep(0.05)

    

