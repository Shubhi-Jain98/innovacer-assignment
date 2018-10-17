#Importing necessary libraries
import urllib2																
from bs4 import BeautifulSoup						#for scraping of data
import smtplib										#for sendding mail															
import sqlite3										#for creating database online
 																				


#Function sendEmail will take input as the message to be send and the recipient's email and will send using the smtp library
def sendEmail(msg, email):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login("16ucs110@lnmiit.ac.in", "anju1031999")							#The sender needs to enter his email and password 
	s.sendmail("16ucs110@lnmiit.ac.in", "16ucs110@lnmiit.ac.in", msg)
	s.sendmail("16ucs110@lnmiit", email, msg)
	s.quit() 

	
	
#Function will create a database in the Random access memory of the local system.	
def createDatabase():														# creates a database in RAM 
	con = sqlite3.connect(":memory:") 										# create a connection using connect()
	cur = con.cursor() 														# All the commands will be executed using cursor object only
	cur.execute("create table List_of_series (Email_id, Name_of_series)") 


#user input for email address and list of series taken in form of comma separated single integer
email = raw_input("Email address: ")					
list_series = raw_input("TV Series: ")										

																			
series_list = list_series.split(',')										#input taken in form of comma separated is stored in a list named as series_list
length = len(series_list)													#length of the series_list is the number of series the user has input 

message = ""																# will contain the output message 
																			

months = ["Jan.","Feb.","Mar.","Apr.","May","Jun.","Jul.","Aug.","Sep.","Oct.","Nov.","Dec."]


createDatabase()															#creating the database

for list_iterator in range(0, length):	
																			
	cur.execute("insert into List_of_series values (?, ?)", (email, series_list[list_iterator])) 																			
	cur.execute("select * from List_of_series")	 
		
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found")
    #to search 
    query = series_list[list_iterator] + " imdb"							# searching the "series IMDB" page on Google
  
    for link_iterator in search(query, tld="co.in", num=1, stop=1, pause=2): 
        quote_page = link_iterator											# Link to the IMDb site of the series from where we'll scrap data further

    	
	result = quote_page.find('imdb')										# finding substring IMDb in the fist url string obtained in google search		
	

        if (result == -1): 													#if substring imdb doesn't exist in the url then the series name isn't
        																	#written correctly or such series doesn't exist
	     	message = message + "Tv series name: "+ series_list[list_iterator]+"/n" + "Status: "+" Series not found" + "\n\n"

        else:         	

			page = urllib2.urlopen(quote_page)						
			soup = BeautifulSoup(page, 'html.parser')
			name_box = soup.find('title')									
			series_detail = name_box.string									#in the IMDB site of series we'll find its year of release and end(if ended)
																			#by scrapping							
																			
			if (series_detail[-9] != " "):									#here we'll check weather the series has ended or not(eg (2006 - 2012) has ended)
																			#while (2011- ) this has not ended 
				message = message + "Tv series name: "+ series_list[list_iterator]+"\n" + "Status: " + "The show has finished streaming all its episodes." +"\n\n"

			else:
		
				k = soup.select('a[href^="/title/tt6077448/episodes?season="]')							#Finding tags by attribute value				
				seasonNo = k[0].string
				p = soup.select('a[href^="/title/tt6077448/episodes?year="]')

				next_date = 'https://www.imdb.com' + k[0]['href']										

				page2 = urllib2.urlopen(next_date)														#we'll go to the web page of latest season
				trial = BeautifulSoup(page2, 'html.parser')

				dates_of_latest_season = trial.select(".airdate")										#dates of latest season is an array which contains the release 
																										#dates of latest season on imdb(weather relesed or not)
				
				first_element =  dates_of_latest_season[0].string											#first episode of latest season			
				first_len = len(first_element)				
				first_ele_strip = first_element.lstrip()														#lstrip will remove the left spaces from first_ele_strip
				
				if (len(first_ele_strip)==0):																#we'll check if the first episode of series is released or not
																										# if it isn't released and year is also not mentined
				    message = message + "Tv series name: "+" "+series_list[list_iterator]+"\n" + "Status: " + "The year of release of  season :" + str(seasonNo) + " is unkown" + "\n\n"
				
				elif(first_ele_strip[1] != " " and  first_ele_strip[2] != " "):								# in case the eries is yet to release only the year is mentioned on imdb
				
					message = message + "Tv series name: "+" "+series_list[list_iterator]+"\n" + "Status: " + "The next season begins in "+ str(first_ele_strip) +"\n\n"
				
				else:																					#if dates of release of last episode is mentioned,  then scraping the and appending in mail
				
					iterator = -1;				
					number = dates_of_latest_season[iterator].string
					
					while(len(number.lstrip())==0):														#finding the latest episode					 
						iterator = iterator-1																						
						number = dates_of_latest_season[iterator].string
						
					else:
					
						last_element = dates_of_latest_season[it].string
						last_element_strip = last_element.lstrip()	   										#remove spaces from the string
						lengthDate = len(last_element)   
						
						if (last_element_strip[1] != " " and  last_element_strip[2] != " "):					#checking if only year is mentioned													
																			
							message = message + "Tv series name: "+" "+series_list[list_iterator]+"\n" + "Status: " + "The next season begins in "+ str(last_element_strip) +"\n\n"

						else:	
						
							monthNo = months.index(last_element_strip[3:7])+1
							message = message + "Tv series name: "+" "+series_list[list_iterator]+"\n" + "Status: "+"The next episode airs on "+ str(last_element_strip[8:12])+"-"+str(monthNo)+"-"+str(last_element_strip[0:2])+"\n\n"
	con.commit()                                													#commiting respective changes in the database				

print message
con.close()
sendEmail(message, email)
print "The mail has been sent to :- "+email



