# Run two threads, one that gets input and one that prints output from the input.
# Question from Stack Overflow: https://stackoverflow.com/questions/69340357/create-two-threads-in-python-one-to-read-and-one-to-ask-something

from threading import Thread

global result
result = None


class OutPut(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global result
        while True: # Loop to check the result
            if result is not None:
                print("Number entered was: {}".format(result))
                if result == 0:
                    break  # if result is 0, break the loop
                result = None  # reset the result to None, so we don't print the same result again
        print("Thread finished")


class Write(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global result
        user_write = True

        while user_write:
            num = int(input("Enter a number? "))
            result = num

            if num == 0:
                user_write = False


threadIO = Write()
threadOutPut = OutPut()

arrThread = [threadIO, threadOutPut]

for tH in arrThread:
    tH.start()

for t in arrThread:
    t.join()

print("===== THREADS OFF =====")
