
# import subprocess, sys
# cmd = ["ssh", "-i", "C:/Users/gb/Documents/220921-070721/developers.pem", "admin@ec2-3-108-59-21.ap-south-1.compute.amazonaws.com", "-tt"]
# ip = 'exit'.encode('utf-8')

# print("Testing command ")
# # c = subprocess.call(cmd, shell=False, stdin=subprocess.PIPE)
# # c.communicate("exit")

# # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
# p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# output = p.communicate(input='exit'.encode())[0]
# # p_status = p.wait()
# # while True:
# #     out = p.stderr.read(1)
# #     if out == '' and p.poll() != None:
# #         break
# #     if out != '':
# #         sys.stdout.write(out)
# #         sys.stdout.flush()


import threading
import time

def thread_function(k):
    print("Testing thread ", k)

mythread = threading.Thread(target=thread_function, args=(1,))

def main():
    mythread.start()
    time.sleep(.9)
    mythread.join()


if __name__ == '__main__':
    main()
