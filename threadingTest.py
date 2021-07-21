import threading
def init():
  def printit():
    threading.Timer(5.0, printit).start()
    print("Hello, World!")
  printit()
init()