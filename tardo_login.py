#!/usr/bin/env python
#-*- coding:utf-8 -*-


import re, mechanize, cookielib, json, duckduckgo, urllib2
from bs4 import BeautifulSoup

emails_list = "logs/execution1.log"

class colores:
    header = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    alert = '\033[93m'
    fail = '\033[91m'
    normal = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

br = mechanize.Browser()
cj = cookielib.LWPCookieJar() 
br.set_cookiejar(cj) 
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)

def get_user(email):
	email = email.split("@")
	username = email[0]
	return username.replace(".","")

def get_linkedin(email, state):
	try:
		#LINKEDIN-------------------------------------------------
		r = br.open('https://www.linkedin.com/')
		br.select_form(nr=0)
		br.form["session_key"] = email
		br.form["session_password"] = "123456"
		br.submit()
		respuestaURL = br.response().geturl()
		if "captcha" in respuestaURL:
			print "|--[INFO][LinkedIn][Captcha][>] Captcha detect!"
		else:
			pass
		html = br.response().read()
		soup = BeautifulSoup(html, "html.parser")
		for span in soup.findAll("span", {"class", "error"}):
			data = remove_tags(str(span))
			if "password" in data:
				print "INFO:LinkedIn:GET:Account Found!"
				if state == 1:
					print colores.blue + "INFO:LinkedIn:GET:it's only rock and roll but i love it!!!" + colores.normal
			if "recognize" in data:
				print "INFO:LinkedIn:GET:Account not found"
	except:
		print colores.alert + "|--[WARNING][LinkedIn][>] Fuck!" + colores.normal

def get_wordpress(email, state):
	try:
		r = br.open('http://wordpress.com/wp-login.php')
		br.select_form("loginform")
		br.form["log"] = email
		br.form["pwd"] = "123456"
		br.submit()
		respuestaWP = br.response().geturl()
		html =  br.response().read()
		soup = BeautifulSoup(html, "html.parser")
		divError = soup.findAll("div", {"id": "login_error"})
		div = remove_tags(str(divError))
		if "incorrect" in div:
			print "INFO:WordPress:GET:Account Found!"
			if state == 1:
				print colores.blue + "INFO:WordPress:GET:it's only rock and roll but i love it !!!" + colores.normal
		if "Invalid" in div:
			print "INFO:WordPress:GET:Account not found"
	except:
		print colores.alert + "|--[WARNING][LinkedIn][>] Fuck!" + colores.normal

def get_tumblr(email, state):
	r = br.open('https://www.tumblr.com/login')
	br.select_form(nr=0)
	br.form["determine_email"] = email
	br.submit()
	respuestaURL = br.response().geturl()
	#print respuestaURL
	if "yahoo" in respuestaURL and state == 1:
		print colores.blue + "INFO:Tumblr:GET:it's only rock and roll but i love it !!!" + colores.normal
	else:
		print "INFO:Tumblr:GET:Account not found"

def get_pastebin(email):
	url = "http://pastebin.com/search?q=" + email.replace(" ", "+")
	print "INFO:PASTEBIN:SEARCH>" + url + "..."
	html = br.open(url).read()
	soup = BeautifulSoup(html, "html.parser")
	for div in soup.findAll("div", {"class", "gsc-thumbnail-inside"}):
		print "INFO:PASTEBIN:URL>" + str(div)

def get_duckduckgoInfo(email):
	try:
		links = duckduckgo.search(email, max_results=10)
		for link in links:
			if "delsexo.com" in str(link):
				pass
			else:
				print "INFO:DuckDuckGO:SEARCH> " + str(link)
	except:
		print colores.alert + "|--[WARNING][DUCKDUCKGO][>] Fuck!" + colores.normal

def get_duckduckgoSmartInfo(email):
	no_company = ("gmail"," hotmail"," yahoo"," protonmail"," mail")
	split1 = email.split("@")
	name = split1[0].replace("."," ")
	split2 = split1[1].split(".")
	company = split2[0].replace(".", "")
	if company in no_company:
		data = name
	else:
		data = name + " " + company
	links = duckduckgo.search(data, max_results=10)
	for link in links:
		print "INFO:DuckDuckGO:SMART SEARCH> " + str(link)
		if "linkedin.com/in/" in str(link):
			print colores.green + "|----[>][POSSIBLE LINKEDIN DETECT] ----" + colores.normal
		if "twitter.com" in str(link):
			print colores.green + "|----[>][POSSIBLE TWITTER DETECT] ----" + colores.normal
		if "facebook.com" in str(link):
			print colores.green + "|----[>][POSSIBLE FACEBOOK DETECT] ----" + colores.normal
		if "soundcloud.com/" in str(link):
			print colores.green + "|----[>][POSSIBLE SOUNDCLOUD DETECT] ----" + colores.normal

def get_AccountTwitter(email):
	username = get_user(email)
	url = "https://twitter.com/" + username
	try:
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html, "html.parser")
		for text in soup.findAll("h1"):
			text = remove_tags(str(text))
			if "Sorry" in text or "Lo sentimos," in text:
				print "INFO:Twitter:" + colores.blue+ username + colores.normal + ":GET:Account not found"
			else:
				print colores.green + "INFO:Twitter:" + colores.blue+ username + colores.green + ":GET:Account Found!" + colores.normal
	except urllib2.HTTPError:
		print colores.alert + "|--[404 HTTP RESPONSE][Check_AccountTwitter][>] 404 NOT FOUND HTTP Twitter"

def get_netflix(email):
	try:
		r = br.open('https://www.netflix.com/es/login')
		br.select_form(nr=0)
		br.form["email"] = email
		br.form["password"] = "123456"
		br.submit()
		respuestaURL = br.response().geturl()
		html =  br.response().read()
		soup = BeautifulSoup(html, "html.parser")
		div = soup.find("div",{"class":"ui-message-contents"})
		if "ninguna" in remove_tags(str(div)):
			print "INFO:NETFLIX:GET:Account not found "
		else:
			print "INFO:NETFLIX:GET:Account found! " +colores.blue+ email
	except:
		print colores.alert + "|--[ERROR][Check_Netflix][>] Fuck!"

def get_amazon(email):
	r = br.open('https://www.amazon.es/ap/signin?_encoding=UTF8&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2Fgp%2Fdeal%2FclaimDeal.html%3F_encoding%3DUTF8%26marketplaceID%3DA1RKKUPIHCS9HS%26dealID%3D14424ac4%26hmac%3DkvqwMiujZ5YmyR2LUbR40v0CTc0%253D%26asin%3DB01LZI6WP6%26dest%3D%252Fdp%252FB01LZI6WP6&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
	br.select_form(nr=0)
	br.form["email"] = email
	br.form["password"] = "123456"
	br.submit()
	html = br.response().read()
	soup = BeautifulSoup(html, "html.parser")
	div = soup.find("div", {"class":"a-alert-content"})

	if "ninguna cuenta" in remove_tags(str(div)):
		print "INFO:AMAZON:GET:Account not found " +colores.blue+ email
	else:
		print "INFO:AMAZON:GET:Account found! "+colores.blue+ email

def get_haveibeenpwned(email):
	url = "https://haveibeenpwned.com/account/" + email
	html = br.open(url)
	soup = BeautifulSoup(html, "html.parser")
	if soup.find("div", {"class": "pwnedSearchResult pwnTypeDefinition pwnedWebsite panel-collapse in"}):
		print "INFO:HAVEIBEENPWNED:GET:Email appears in leaks " +colores.blue+ email
	else:
		print "INFO:HAVEIBEENPWNED:GET:Email doesn't appear in leaks"

# Email spoofing generator php
def generate_php(fromm, to, title, messaje):
	php = """<?php
$from      = '""" + fromm + """';
$titulo    = '""" + title + """';
$mensaje   = '""" + messaje + """';
$cabeceras = 'From: """ + to + """' . "\r\n" .
    'Reply-To: nice@eo-ripper.py' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();
mail($from, $titulo, $mensaje, $cabeceras);
echo "Todo OK!";
?>"""
	f = open("evilmail.php", "a");
	f.write(php)
	f.close()



def menu():
#x=1 means we will only run social networks of this email address
	x = 1
	if type(x) != int:
		print "[Warning][Menu][>] Fuck!"
		menu()
	else:
		return x

def attack(email):
	email = email.replace("\n", "")
	url = "http://www.verifyemailaddress.org/es/"
	try:
		html = br.open(url)
		br.select_form(nr=0)
		br.form['email'] = email
		br.submit()
		resp = br.response().read()
		soup = BeautifulSoup(resp, "html.parser")
		state = 0
		for li in soup.find_all('li', {'class':"success valid"}):
			verif = remove_tags(str(li))
			print verif
			if len(verif)>5:
				print "[INFO][TARGET][>] " + email
				print "|--[INFO][EMAIL][>] Email validated..."
			else:
				state = 1
				print "[INFO][TARGET][>] " + email
				print "|--[INFO][EMAIL][>] It's not created..."
	except:
		print "[INFO][TARGET][>] " + email
		print "|--[INFO][EMAIL] No verification possible... "

	#CALL THE ACTION
	get_linkedin(email, state)
	get_wordpress(email, state)
	get_netflix(email)
	get_tumblr(email, state)
	get_pastebin(email)
	get_AccountTwitter(email)
	get_duckduckgoInfo(email)
	#get_duckduckgoSmartInfo(email)
	get_amazon(email)
	get_haveibeenpwned(email)
def main():
	global emails_list
	
	m = menu()
	if m == 1:
		print "[INFO][TARDO mails][>] By default 'logs/execution1.log'..."
		file = open(emails_list, 'r')
		for email in file.readlines():
			attack(email.replace("\n", ""))
	if m == 2:
		print "This option is not available yet. Sorry"
	if m == 3:
		print "This option is not available yet. Sorry"

	if m <0 or m > 3:
		print "|--[TARDO][SAY][>] Are you stupid?"
		print "|--[TARDO][SAY][>] 1 or 2 or 3."
	if type(m) == str:
		print "|--[TARDO][SAY][>] Are you stupid?"
		print "|--[TARDO][SAY][>] 1 or 2 or 3."

if __name__ == "__main__":
	main()