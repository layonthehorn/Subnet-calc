#!/usr/bin/env python3

# Layonthehorn
# This program will subnet an IP address with a provided CIDR mask.
# ./subnet.py 10.0.0.0 /30
# Network address:10.0.0.0
# Broadcast address:10.0.0.3
# Subnet mask:/30
# Host range:10.0.0.1 - 10.0.0.2
import sys, re

class takeinput():

    def __init__(self):
       
        if len(sys.argv) < 3:
            print("Usage: (ipaddress) (CIDR Mask)")
            sys.exit(0)
        self.ipaddress = self.checkip(sys.argv[1])
        self.cidr = self.checkcidr(sys.argv[2])
        self.checkipsub(self.ipaddress,self.cidr)


    def checkip(self,ipaddress):
        if not (re.match("""^(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$""",ipaddress)):
            print("You must enter a valid IP address.")
            print(sys.argv[1])
            sys.exit(0)
        else:
            return re.split("\.",ipaddress)


    def checkcidr(self,cidrmask):
        '''
The ^ matches the start of the string. The $ matches the end of the string.
The / is just a forward slash. The [8-9] that follows it is a range of numbers that match.
the | splits up different paternts that all match. 
As long as one of these match the function returns true and the subnet mask is returned.
the \d can be any digit 0-9.
So /[8-9] would match /8 and /9.
and /1\d matches /10-/19
then /2\d matches /20-/29
then /30 just matches /30
        '''
        if not re.match("^(/[8-9]|/1\d|/2\d|/30)$",cidrmask):
            print("Mask must be inbetween 7 and 31.\nFormat: /number")
            sys.exit(0)
        else:
            cidrmask = cidrmask.replace("/","")
            return int(cidrmask)

    def checkipsub(self,ip,sub):
        tip = int(ip[0])
        

        if (tip <= 191 and tip >=128) and sub < 16:
            print("The lowest a class B can have for a mask is /16.")
            sys.exit(0)

        elif (tip <= 223 and tip >=192) and sub < 24:
            print("The lowest a class C can have for a mask is /24.")
            sys.exit(0)



class subnetcalc():

    def __init__(self):
        self.ip = takeinput()
        self.findclass(self.ip.ipaddress)
        self.netadd = self.findnetadd(self.ip.ipaddress,self.ip.cidr)
        self.broadadd = self.findbroadcast(self.ip.ipaddress,self.ip.cidr)
        self.usablehost = self.findhostrange(self.netadd,self.broadadd)
        
        print("The network address is: {0}.{1}.{2}.{3}".format(self.netadd[0],self.netadd[1],self.netadd[2],self.netadd[3]))
        print("The broadcast address is: {0}.{1}.{2}.{3}".format(self.broadadd[0],self.broadadd[1],self.broadadd[2],self.broadadd[3]))
        print("The subnet mask is: /{0}".format(self.ip.cidr))
        print("{0}".format(self.usablehost))
    

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


    def findnetadd(self,addresslist,newmask):
        newlist = []
        listinbinary = ""
        networksec = ""
        hostsec = ""
        finalnet = ""
        for i in range(len(addresslist)):
             listinbinary= listinbinary + str(self.dectobin(addresslist[i]))

        for i in range(newmask):
            networksec = networksec + "1"

        while len(networksec) < 32:
            networksec = networksec + "0"
            
        for net,ip in zip(networksec,listinbinary):
            if net == "0":
                finalnet = finalnet + "0" 
            else:
                finalnet = finalnet + str(ip)
        newlist = [self.bintodec(finalnet[:8]),self.bintodec(finalnet[8:16]),self.bintodec(finalnet[16:24]),self.bintodec(finalnet[24:])]
        return newlist




    def findbroadcast(self,addresslist, newmask):
        newlist = []
        listinbinary = ""
        networksec = ""
        hostsec = ""
        finalnet = ""
        for i in range(len(addresslist)):
             listinbinary= listinbinary + str(self.dectobin(addresslist[i]))

        for i in range(newmask):
            networksec = networksec + "1"

        while len(networksec) < 32:
            networksec = networksec + "0"
            
        for net,ip in zip(networksec,listinbinary):
            if net == "0":
                finalnet = finalnet + "1" 
            else:
                finalnet = finalnet + str(ip)
        newlist = [self.bintodec(finalnet[:8]),self.bintodec(finalnet[8:16]),self.bintodec(finalnet[16:24]),self.bintodec(finalnet[24:])]
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
            for i in list:

                if i != 0 or loop !=0:
                    finalan = finalan + power2
                power2 = power2 * 2
        return finalan


if __name__ == "__main__":
    subnetcalc()
