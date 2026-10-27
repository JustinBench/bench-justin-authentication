import sys
sys.path.append('../')
from functions import *
import math

class RSA:
    def __init__(self):
        self.alphabet1 = "abcdefghijklmnopqrstuvwxyz"
        self.alphabet2 = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    def GenerateKeys(self, num_str1, num_str2):
        self.p = ToBase10(num_str1, self.alphabet1)
        self.q = ToBase10(num_str2, self.alphabet1)
        if self.p < 10**200 or self.q < 10**200:
            print("One or both inputs are too short.")
            return
        self.p %= (10 ** 200)
        self.q %= (10 ** 200)
        if self.p % 2 == 0:
            self.p += 1
        if self.q % 2 == 0:
            self.q += 1
        while not MonteCarlo(self.p, Miller):
            self.p += 2
        while not MonteCarlo(self.q, Miller):
            self.q += 2
        self.n = self.p * self.q
        self.r = (self.p - 1) * (self.q - 1)
        self.e = 10 ** 398 + 1
        while gcd(self.r, self.e) != 1:
            self.e += 1
        self.d = pow(self.e, -1, self.r)
        new_file = open("public.txt", "x")
        new_file.write(str(self.n) + "\n" + str(self.e) + "\n")
        new_file.close()
        new_file = open("private.txt", "x")
        new_file.write(str(self.n) + "\n" + str(self.d) + "\n")
        new_file.close()
        return
    
    def Encrypt(self, input_file, output_file):
        fin = open(input_file, "rb")
        PlainText = fin.read().decode("utf-8")
        fin.close()
        fin = open("public.txt", "r")
        a = True
        for line in fin:
            if a:
                self.n = int(line)
                a = False
            else:
                self.e = int(line)
        fin.close()
        block_size = 216
        total_chars = len(PlainText)
        num_of_blocks = math.ceil(total_chars/block_size)
        stringMessage = ""
        for index in range(num_of_blocks):
            num = ToBase10(PlainText[index * block_size:(index + 1) * block_size], self.alphabet2)
            new_num = pow(num, self.e, self.n)
            stringMessage += FromBase10(new_num, self.alphabet2) + "$"
        fout = open(output_file, "wb")
        fout.write(stringMessage.encode("utf-8"))
        fout.close()
    
    def Decrypt(self, input_file, output_file):
        fin = open(input_file, "rb")
        Etext = fin.read().decode("utf-8")
        fin.close()
        fin = open("private.txt", "r")
        a = True
        for line in fin:
            if a:
                self.n = int(line)
                a = False
            else:
                self.d = int(line)
        fin.close()
        blocks = Etext.split("$")
        blocks.pop()
        Dtext = ""
        for block in blocks:
            num = ToBase10(block, self.alphabet2)
            new_num = pow(num, self.d, self.n)
            Dtext += FromBase10(new_num, self.alphabet2)
        fout = open(output_file, "wb")
        fout.write(Dtext.encode("utf-8"))
        fout.close()
        