import secrets
import hashlib

def generateRandom():
    k = secrets.token_hex(20)
    key = "{0:08b}".format(int(k, 16))
    return key
def xor_two_str(a, b):
    return ''.join([hex(ord(a[i % len(a)]) ^ ord(b[i % (len(b))]))[2:] for i in range(max(len(a), len(b)))])


class Reader:
    def __init__(self, id_reader):
        self.id_reader = id_reader
        self.pid = ""
        self.x = ""
        self.Rr = ""
        self.Rt = ""

    def setValue(self, pid, x):
        self.pid = pid
        self.x = x

    def step_1(self):
        self.Rr = generateRandom()
        return {"Rr": self.Rr}

    def step_3(self, dict):
        self.Rt = dict['Rt']
        string = self.x + self.Rr + dict['Rt'] + str(self.id_reader)
        result = hashlib.sha1(string.encode())

        return {"Rt": dict["Rt"], "B1": dict["B1"], 'Pid': dict["Pid"], "Rid": self.pid, "B2": result,
                "Rr": self.Rr}

    def step_5(self, dict):
        # print("from reader side")
        x_new_str = self.x + self.Rt + self.Rr + str(self.id_reader)
        x_new = hashlib.sha1(x_new_str.encode()).hexdigest()
        # print("x_new")
        # print(x_new)
        # print(self.x)

        x_new = "{0:08b}".format(int(x_new, 16))

        # h(xoldi ||Rt ||Rr||PIDi)
        pid_new_str = self.x + self.Rt + self.Rr + self.pid
        pid_new = hashlib.sha1(pid_new_str.encode()).hexdigest()
        # print("pid_new")
        # print(pid_new)
        # print(self.pid)

        pid_new = "{0:08b}".format(int(pid_new, 16))
        # print("pid_new")
        # print(pid_new)

        tmp = self.x + x_new + self.pid + pid_new + str(self.id_reader) + self.Rr
        tmp = hashlib.sha1(tmp.encode()).hexdigest()
        a_list = [chr(ord(a) ^ ord(b)) for a, b in zip(dict["B4"], tmp)]
        # print(a_list)
        data = "".join(a_list)
        # h(xj||RIDj||PRIDj||Datai||Rr)
        b5_str = self.x + str(self.id_reader) + self.pid + data + self.Rr
        b5 = hashlib.sha1(b5_str.encode()).hexdigest()
        flag = False
        # print("b5 =")
        # print(b5)
        # print(self.Rt)
        # print(self.Rr)
        if (dict["B5"] == b5):
            flag = True

        if (flag):
            # B6 = B3 ⊕h(xj2 | | PRIDj2 | | Rr)
            # B7 = h(B6||Rt)
            dataj = x_new + pid_new + self.Rr

            dataj = hashlib.sha1(dataj.encode()).hexdigest()
            a_list = [chr(ord(a) ^ ord(b)) for a, b in zip(dict["B3"], dataj)]
            # print(a_list)
            B6 = "".join(a_list)

            # print("dataj")
            # print(dataj)

            # print("B3 =")
            # print(B6)
            B7_str = B6 + self.Rt

            B7 = hashlib.sha1(B7_str.encode()).hexdigest()
            self.pid = pid_new
            self.x = x_new
            # print("B7 =")
            # print(B7)
            return {"B7": B7}
