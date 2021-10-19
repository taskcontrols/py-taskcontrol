from taskcontrol.utils import TimerBase

timer = TimerBase()

if timer:
    pass

t = timer.create({"name": "testtimer"})
print(t)
if t:
    timer.start("Testtimer")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    timer.get_timer("Testtimer")
    timer.get_elapsed_time("Testtimer")
    timer.stop("Testtimer")
    timer.get_timer("Testtimer")
    timer.get_elapsed_time("Testtimer")
    timer.start("Testtimer")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    print("Test")
    timer.get_timer("Testtimer")
    timer.get_elapsed_time("Testtimer")
    timer.stop("Testtimer")
    timer.get_timer("Testtimer")
    timer.get_elapsed_time("Testtimer")
    timer.reset("Testtimer")

