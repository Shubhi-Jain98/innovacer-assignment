import pandas as pd
import smtplib											#library to send mail to user
import csv
import MySQLdb as mdb

#take user input
email = raw_input("Email address: ")					
type(email)
list = raw_input("TV Series: ")
type(series)

##############################refer this link for more understanding of below code....http://zetcode.com/db/mysqlpython/
#DB1__store user input ...columns as [email list]
db = mdb.connect("localhost","root","testing","TESTDB" )
cursor = db.cursor()
cursor.execute("""INSERT INTO staff (FIRST_NAME, LAST_NAME) VALUES (r{0}, r{1})""".format(email, series))

db.commit()
db.close()

#DB2__store list from DB1 to DB2 in form...[series status]



#DB3__actual database...store status of all series...[series status]



#code to send mail to user
s = smtplib.SMTP('smtp.gmail.com', 587) 							# creates SMTP session  
s.starttls() 														# start TLS for security
s.login("sender_email_id", "sender_email_id_password") 				# Authentication 
message = "Message_you_need_to_send"								# message to be sent 
s.sendmail("sender_email_id", "receiver_email_id", message) 		# sending the mail 
s.quit() 															# terminating the session 
