import time

from qh import Qh

while True:
    nowTime = time.strftime("%H:%M:%S", time.localtime())

    if ("08:59:59" < nowTime < "11:30:01") or ("10:15:01" < nowTime < "10:29:59") or (
            "13:29:59" < nowTime < "15:00:01"):
        t_id = Qh().RunTime()
        Qh().RunOI(t_id)
        Qh().RunP(t_id)
        Qh().RunRB(t_id)
        Qh().RunOIP(t_id)
        Qh().RunJD(t_id)
        Qh().RunFG(t_id)

    time.sleep(10)
