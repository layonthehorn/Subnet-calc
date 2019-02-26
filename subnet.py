#!/usr/bin/env python3

# Layonthehorn
# This program will take in an IP address. It will then return the subnet mask, network address, and broadcast address.
# 
# Created in 4 hours on 2/26/19. The power was down not like I had anything else to do.

import sys, re

class takeinput():


    def checkip(self,ipaddress):
        if not (re.match("""^(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$""",ipaddress)):
            print("You must enter a valid IP address.")
            print(sys.argv[1])
            sys.exit(0)
        else:
            return re.split("\.",ipaddress)
    def __init__(self):
       
        if len(sys.argv) < 2:
            print("Usage: (ipaddress)")
            sys.exit(0)
        self.ipaddress = self.checkip(sys.argv[1])

class subnetcalc():

    def findclass(self, addresslist):
        if int(addresslist[0]) <= 127:
            subnetmask = 8 
        elif int(addresslist[0]) <= 191:
            subnetmask = 16
        elif int(addresslist[0]) <= 223:
            subnetmask = 24
        else:
            print("Must be a class A, B, or C.")
            sys.exit(0)
        
        return subnetmask


    def findhostrange(self,net,broad):
        net1 = net[:]
        broad1 = broad[:]
        stringnet = ""
        stringbroad = ""
        lastoctnet = net1.pop()
        net1.append((int(lastoctnet)+1))
        lastoctbroad = broad1.pop()
        broad1.append((int(lastoctbroad)-1))
        
        stringnet = "{0}.{1}.{2}.{3}".format(net1[0],net1[1],net1[2],net1[3])
        
        stringbroad = "{0}.{1}.{2}.{3}".format(broad1[0],broad1[1],broad1[2],broad1[3])



        return """The usable host range is: {} - {}  """.format(stringnet,stringbroad)


    def findnetadd(self,addresslist,subnetmask):
        listinbinary = []
        newlist = []
        if subnetmask == 8:
            for i in range(len(addresslist)):
                listinbinary.append(self.dectobin(addresslist[i]))
            listinbinary.pop()
            listinbinary.pop()
            listinbinary.pop()
            listinbinary.append("00000000")
            listinbinary.append("00000000")
            listinbinary.append("00000000")
            for i in range(len(listinbinary)):
                newlist.append(self.bintodec(listinbinary[i]))
            return newlist
        elif subnetmask == 16:
            for i in range(len(addresslist)):
                listinbinary.append(self.dectobin(addresslist[i]))
            listinbinary.pop()
            listinbinary.pop()
            listinbinary.append("00000000")
            listinbinary.append("00000000")
            for i in range(len(listinbinary)):
                newlist.append(self.bintodec(listinbinary[i]))
            return newlist
        elif subnetmask == 24:
            for i in range(len(addresslist)):
                listinbinary.append(self.dectobin(addresslist[i]))
            listinbinary.pop()
            listinbinary.append("00000000")
            for i in range(len(listinbinary)):
                newlist.append(self.bintodec(listinbinary[i]))
            return newlist


    def findbroadcast(self,addresslist,subnetmask):
        listinbinary = []
        newlist = []
        if subnetmask == 8:
            for i in range(len(addresslist)):
                listinbinary.append(self.dectobin(addresslist[i]))
            listinbinary.pop()
            listinbinary.pop()
            listinbinary.pop()
            listinbinary.append("11111111")
            listinbinary.append("11111111")
            listinbinary.append("11111111")
            for i in range(len(listinbinary)):
                newlist.append(self.bintodec(listinbinary[i]))
            return newlist
        elif subnetmask == 16:
            for i in range(len(addresslist)):
                listinbinary.append(self.dectobin(addresslist[i]))
            listinbinary.pop()
            listinbinary.pop()
            listinbinary.append("11111111")
            listinbinary.append("11111111")
            for i in range(len(listinbinary)):
                newlist.append(self.bintodec(listinbinary[i]))
            return newlist
        elif subnetmask == 24:
            for i in range(len(addresslist)):
                listinbinary.append(self.dectobin(addresslist[i]))
            listinbinary.pop()
            listinbinary.append("11111111")
            for i in range(len(listinbinary)):
                newlist.append(self.bintodec(listinbinary[i]))
            return newlist



    def dectobin(self,num):
        """This program converts from decimal to binary"""
        finalprint = ""
        num = int(num)
        list =[]
        if num == 0:
            pass
        else:
            while num > 0:

                remander = num%2
                list.append(remander)
                num = num //2
            list.reverse()
        while len(list) % 8 != 0 or list == []:

            list.insert(0,0)

        for i in list:
            finalprint = finalprint + str(i)
        return finalprint
    

    def bintodec(self,num):
        """This program converts from binary to decimal"""
        loop = 0
        finalan = 0
        list =[]
        power2 = 1
        if num == "00000000":
            finalan = "0"
        else:
            for i in str(num):
                conum= int(i)
                list.append(conum)
            list.reverse()
            #print(list)
            for i in list:
                if i != 0 or loop !=0:
                    finalan = finalan + power2
                power2 = power2 * 2
        return finalan

    def __init__(self):
        self.ip = takeinput()
        self.subnet = self.findclass(self.ip.ipaddress)
        self.netadd = self.findnetadd(self.ip.ipaddress,self.subnet)
        self.broadadd = self.findbroadcast(self.ip.ipaddress,self.subnet)
        self.usablehost = self.findhostrange(self.netadd,self.broadadd)
        
        print("The network address is: {0}.{1}.{2}.{3}".format(self.netadd[0],self.netadd[1],self.netadd[2],self.netadd[3]))
        print("The broadcast address is: {0}.{1}.{2}.{3}".format(self.broadadd[0],self.broadadd[1],self.broadadd[2],self.broadadd[3]))
        print("The subnet mask is: /{0}".format(self.subnet))
        print("{0}".format(self.usablehost))
    

if __name__ == "__main__":
    subnetcalc()



