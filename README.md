# Tardo

Watch tardo_video.webm to see the PoC

# Dependencies

pip3 install -r requirements.txt

You will need too the software below to execute the tool with no issues:<br>
  -mysql-server (You should create a database named "mails")<br>
  -theharvester<br>
  -Exiftool<br>
  
  
  # Usage
  bash Tardo
  OR
  ./Tardo
  
  Then, you will see a shell. Use "Help" command to see all the commands available.
  
  # About Tardo
  
  Tardo is a bash tool designed to looking ffor mails of a organization. Then, Tardo will use a Python script to do a brute force attacke against some websites. If it find the account it means the account with this mail exists. This kind of information is very important to start a pentesting.
  
  # Tested
  
  At the moment (2018/12/25) the tool has been tested in Kali Linux distro and it works.
  
  # Common Errrors
  
  1. If you try many times the execution of Tardo, Python script will be blocked and you should interrumpt the execution with Ctrl+X and Tardo will continue with the information obtained before the interrumption.
  2. If you don't have mails database the execution will be wrong...create before the execution the mail database and nevermind for the table, it should be created with
  
  mysql -u $db_user -p$db_pwd -e "CREATE TABLE mails.$project (id int NOT NULL  auto_increment, mail VARCHAR(100), twitter VARCHAR (1), amazon VARCHAR(1), netflix VARCHAR(1),  PRIMARY KEY(id))"
  
  But if the script doesn't create the table, you can do it manually.
  
  3. Error importing. You should do the import by hand. Sorry, mate :(
  
  # Extra Information
  
  If you want extra and deeper information regarding Tardo, you could visit a non-Windows site (Github before be a Windows prisioner was cool)
  
  My hub (ES): https://manuhub.wordpress.com/2018/12/25/tardo-tool/
  
  # Contact Me
  
  Name: Manuel Alén Sánchez<br>
  Twitter: @hippi3c0w<br>
  Quitter: @hippi3C0w<br>
  Mastodon: @hippi3c0w<br>
  Telegram: @hippi3c0w<br>
  
