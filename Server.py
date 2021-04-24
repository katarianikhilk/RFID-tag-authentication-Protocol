import secrets
from Reader import Reader
from Tag import Tag
import pymongo
import hashlib

def xor_two_str(a,b):
  return ''.join([hex(ord(a[i%len(a)]) ^ ord(b[i%(len(b))]))[2:] for i in range(max(len(a), len(b)))])

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]

mycol = mydb["customers"]

def generateRandom():
    k = secrets.token_hex(20)
    key = "{0:08b}".format(int(k, 16))
    return key



class Server:
    def set_reader(id):
        pid = generateRandom()
        x = generateRandom()
        my_dict = {"id_reader": id, "p_new": pid, "p_old": pid, "x_new": x, "x_old": x}
        mycol.insert_one(my_dict)
        return {"pid": pid, "x":x}

    def set_tag(ID):
        pid = generateRandom()
        x = generateRandom()
        my_dict = {"id_tag": ID, "p_new": pid, "p_old": pid, "x_new": x, "x_old": x}
        mycol.insert_one(my_dict)
        return {"pid": pid, "x":x}

    def step_4(dist):
        pid = dist['Pid']
        rid = dist['Rid']
        tag_query = {"p_new": pid}
        tag = mycol.find_one(tag_query)

        # print(tag)
        reader_query = {"p_new": rid}
        reader = mycol.find_one(reader_query)

        # PIDi = Poldi and PRIDj = Pnew
        # PIDi = Poldi and PRIDj = Pold
        if (tag == None):
            tag_query = {"p_old": pid}
            tag = mycol.find_one(tag_query)
            reader_query = {"p_old": rid}
            reader = mycol.find_one(reader_query)
            if(reader == None):
                reader_query = {"p_new": rid}
                reader = mycol.find_one(reader_query)

        if (tag == None ):
            return False

        if( reader == None):
            return False

        # print(reader)
        string2 = reader["x_new"] + dist["Rr"] + dist["Rt"] + str(reader["id_reader"])
        string1 = tag["x_new"] + dist["Rr"] + dist["Rt"] + str(tag["id_tag"])
        b1 = hashlib.sha1(string1.encode())
        b2 = hashlib.sha1(string2.encode())
        # print(b1.hexdigest())
        # print(b2.hexdigest())

        # print("/////////////////////////")
        # print(dist["B1"].hexdigest())
        # print(dist["B2"].hexdigest())

        flag = False
        if (b1.hexdigest() == dist["B1"].hexdigest()):
            if (b2.hexdigest() == dist["B2"].hexdigest()):
                flag = True
            else:
                return False
        else:
            return False

        if (flag):
            # h(xoldi ||Rt ||Rr||IDi
            tag["x_old"] = tag["x_new"]
            tag["p_old"] = dist["Pid"]
            reader["x_old"] = reader["x_new"]
            reader["p_old"] = dist["Rid"]
            tag_x_new = tag["x_old"] + dist["Rt"] + dist["Rr"] + str(tag["id_tag"])
            tag_x_new = hashlib.sha1(tag_x_new.encode()).hexdigest()
            # print("tag_x_new")
            # print(tag_x_new)
            # print("tag_x_old")
            # print(tag["x_old"])
            tag["x_new"]  = "{0:08b}".format(int(tag_x_new, 16))

            # h(xoldi ||Rt ||Rr||PIDi)
            tag_pid_new = tag["x_old"] + dist["Rt"] + dist["Rr"] + tag["p_old"]
            tag_pid_new = hashlib.sha1(tag_pid_new.encode()).hexdigest()
            # print("tag_pid_new")
            # print(tag_pid_new)
            # print("tag_pid_old")
            # print(tag["p_old"])
            tag["p_new"] = "{0:08b}".format(int(tag_pid_new, 16))


            reader_x_new = reader["x_old"] + dist["Rt"] + dist["Rr"] + str(reader["id_reader"])
            reader_x_new = hashlib.sha1(reader_x_new.encode()).hexdigest()
            # print("reader_x_new")
            # print(reader_x_new)
            # print("reader_x_old")
            # print(reader["x_old"])
            reader["x_new"] = "{0:08b}".format(int(reader_x_new, 16))
            # h(xoldi ||Rt ||Rr||PIDi)
            reader_pid_new = reader["x_old"] + dist["Rt"] + dist["Rr"] + reader["p_old"]
            reader_pid_new =  hashlib.sha1(reader_pid_new.encode()).hexdigest()
            # print("reader_pid_new")
            # print(reader_pid_new)
            # print("reader_pid_old")
            # print(reader["p_old"])

            reader["p_new"] = "{0:08b}".format(int(reader_pid_new, 16))
            # = h(xoldi ||xnew i ||Pold i ||Pnew i ||IDi) //self.x + x_new + self.pid + pid_new + str(self.id_tag)
            B3_str = tag["x_old"] + tag["x_new"] + tag["p_old"] + tag["p_new"] + str(tag["id_tag"])
            # print("B# str =")
            # print(B3_str)
            # print(dist["Rt"])
            # print(dist["Rr"])
            # h(xnewj || Pnewj || Rr)
            dataj = reader["x_new"] + reader["p_new"] + dist["Rr"]
            dataj = hashlib.sha1(dataj.encode()).hexdigest()
            # print("dataj pre")
            # print(dataj)

            B3 = hashlib.sha1(B3_str.encode()).hexdigest()

            a_list = [chr(ord(a) ^ ord(b)) for a, b in zip(B3, dataj)]
            # print(a_list)
            B3 = "".join(a_list)
            # print("B3 ==")
            # print(B3)
            #  h(xoldj ||xnewj ||Poldj ||Pnew j ||RIDj||Rr)
            B4_str = reader["x_old"] + reader["x_new"] + reader["p_old"] + reader["p_new"] + str(reader["id_reader"]) + dist[
                "Rr"]
            B4 = hashlib.sha1(B4_str.encode()).hexdigest()
            a_list = [chr(ord(a) ^ ord(b)) for a, b in zip(B4, dataj)]
            # print(a_list)
            B4 = "".join(a_list)
            #h(xj||xj2||PRIDj||PRIDj2||RIDj||Rr)
            # B5 = h(xoldj ||RIDj||Poldj ||B4||Rr)
            B5_str = reader["x_old"] + str(reader["id_reader"]) + reader["p_old"] + dataj + dist["Rr"]
            B5 = hashlib.sha1(B5_str.encode()).hexdigest()

            tag_query = {"p_new": pid}
            reader_query = {"p_new": rid}
            tag_update = { "$set": { 'id_reader': tag["id_tag"] ,'p_new': tag["p_new"], 'p_old': tag["p_old"], 'x_new': tag["x_new"], 'x_old': tag["x_old"]}
                           }
            reader_update = {"$set": {'id_reader': reader["id_reader"], 'p_new': reader["p_new"], 'p_old': reader["p_old"],
                                   'x_new': reader["x_new"], 'x_old': reader["x_old"]}
                          }
            mycol.update_one(tag_query, tag_update)
            mycol.update_one(reader_query, reader_update)
            # print("output from server side")
            # print("B3 =")
            # print(B3)
            # print("B4 =")
            # print(B4)
            # print("B5 =")
            # print(B5)



            return {"B3": B3, "B4": B4, "B5": B5}
