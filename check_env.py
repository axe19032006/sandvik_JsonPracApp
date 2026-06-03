import sys  # 'sys' lets us ask Python about itself

print("Which Python am I using right now?")
print(sys.executable)   # the exact Python program running this file
print()
print("Where do my packages live?")
print(sys.prefix)       # the environment this Python belongs to