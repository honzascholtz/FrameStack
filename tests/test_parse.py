import FrameStack as fs
with open("test_paste.txt", "w") as f:
    f.write("Reach\t335\t318\nStack\t531\t440\n")

print(fs.FrameStack("test_paste.txt").geo)
