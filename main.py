# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import secrets

from Tag import Tag
from Reader import Reader
from Server import Server

import time


def generateRandom():
    k = secrets.token_hex(20)
    key = "{0:08b}".format(int(k, 16))
    return key



def reader_registration(reader):
    dict = Server.set_reader(reader.id_reader)
    reader.setValue(dict["pid"], dict["x"])

def tag_registration(tag):
    dict = Server.set_tag(tag.id_tag)
    tag.setValue(dict["pid"], dict["x"])

def Authentication(reader, tag):
    dict = reader.step_1()
    if (dict):
        dict = tag.step_2(dict)
    if (dict):
        dict = reader.step_3(dict)
    # print("Time Consumed in step 3 (by Reader)")
    # print("% s seconds" % (time.time() - start))
    start = time.time()

    if (dict):
        dict = Server.step_4(dict)
    # print("Time Consumed in step 4 (by Server)")
    # print("% s seconds" % (time.time() - start))
    start = time.time()
    if (dict):
        dict = reader.step_5(dict)
    # print("Time Consumed in step 5 (by reader)")
    # print("% s seconds" % (time.time() - start))
    start = time.time()

    if (dict):
        if (tag.step_6(dict)):
            print("tag verified ")
        else:
            print("not verified")
    else:
        print("not verified")
    # print("Time Consumed in step 6 (by Tag)")
    # print("% s seconds" % (time.time() - start))


if __name__ == "__main__":


    reader1 = Reader(11542) # creating new Reader object reader1

    reader_registration(reader1) # registration of reader1 (1152) with server


    tag1 = Tag(103)   # creating new Tag object tag1
    tag_registration(tag1) # registration of tag1 (101) with server
    # print("Time Consumed in Tag Registration ")
    # print("% s seconds" % (time.time() - start))
    tag2 = Tag(102)  # creating new Tag object(tag2) which is not register with server
    tag2.pid = generateRandom() # assigning fake pid to tag2 object
    tag2.x = generateRandom() # assigning fake x to tag2 object

    # start = time.time()
    print("Authentication result of tag1 using reader1 =>")
    Authentication(reader1, tag1) # trying to authenticate tag1 using reader1
    print("Authentication result of tag2 using reader1 =>")
    Authentication(reader1, tag2) # trying to authenticate tag2 using reader1

    # print("Time Consumed in tag Authentication ")
    # print("% s seconds" % (time.time() - start))





# cProfile.run('run()')





