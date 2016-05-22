from proxychecker import check_proxy, Proxy

#proxy = Proxy(proto='socks5', host='localhost', port='9050', username='',
#password='')

def makeproxy(hostport):
	return Proxy(proto='http',
		host=hostport.split(":")[0], 
		port=hostport.split(":")[1], 
		username='', password='')

for line in open("proxylist.txt","r"):
	print(line.split())

proxy = Proxy(proto='http', host='190.112.42.131', port='8080',
username='', password='')


print(check_proxy(proxy))
