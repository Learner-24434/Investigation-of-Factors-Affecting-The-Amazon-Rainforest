import time, subprocess as sb

code = ""

while True:
    with open("main.py",  "r") as source:
        if code != source.readlines():
            sb.run("python main.py")
        for line in source.readlines():
            if "<STOP>" in line:
                break
        
        time.sleep(1)