import secrets
import hashlib

def generateRandom():
    k = secrets.token_hex(20)
    key = "{0:08b}".format(int(k, 16))
    return key

class Tag:
    def __init__(self, id_tag):
        self.id_tag = id_tag
        self.pid = ""
        self.x = ""
        self.Rr = ""
        self.Rt = ""

    def setValue(self, pid, x):
        self.pid = pid
        self.x = x


    def step_2(self, dict):
        self.Rt = generateRandom()
        self.Rr = dict['Rr']
        string = self.x +  dict['Rr'] + self.Rt + str(self.id_tag)
        result = hashlib.sha1(string.encode())

        return {"Rt": self.Rt, "B1": result, 'Pid': self.pid}

    def step_6(self, dict):
        # xi2 = h(xi | | Rt | | Rr | | IDi)
        # PIDi2 = h(xi | | Rt | | Rr | | PIDi)
        # check  B7? = h(h(xi | | xi2 | | PIDi | | PIDi2| | IDi) | | Rt)
        # update(xi, PIDi)
        # with (xi2, PIDi2)
        x_new_str = self.x + self.Rt + self.Rr + str(self.id_tag)
        x_new = hashlib.sha1(x_new_str.encode()).hexdigest()
        # print("x_new_tag")
        # print(x_new)
        # print(self.x)

        x_new = "{0:08b}".format(int(x_new, 16))
        pid_new_str = self.x + self.Rt + self.Rr + self.pid
        pid_new = hashlib.sha1(pid_new_str.encode()).hexdigest()
        # print("pid_new_tag")
        # print(pid_new)
        # print(self.pid)

        pid_new = "{0:08b}".format(int(pid_new, 16))

        temp_str = self.x + x_new + self.pid + pid_new + str(self.id_tag)
        # B3_str = tag["x_old"] + tag["x_new"] + tag["p_old"] + tag["p_new"] + str(tag["id_tag"])

        temp = hashlib.sha1(temp_str.encode()).hexdigest()
        # print("temp =")
        # print(temp)

        b7_str = temp + self.Rt
        b7 = hashlib.sha1(b7_str.encode()).hexdigest()

        # print(self.Rt)
        # print(self.Rr)

        # print(b7)

        if b7 == dict["B7"]:
            self.pid = pid_new
            self.x = x_new
            return True
        else:
            return False



