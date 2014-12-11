import pyodbc

def connectToDB():
	conn = pyodbc.connect("DRIVER={MySQL ODBC 5.3 Unicode Driver}; SERVER=pma.iwiserver.com; PORT=3306; DATABASE=uni06; UID=XXX; PASSWORD=XXX;")
	cursor = conn.cursor()

def insertInto(x, score):

	user_name = str(x['user']['screen_name'])
	created_at = x['created_at']
	text = str(x['text'])
	score = float(score)

	cursor.execute("INSERT INTO tweets (user_name, created_at, text, score) VALUES (" + "'" + user_name + "'" + ", " + "'" + created_at + "'" + ", " + "'" + text + "'" + "," + "'" + score + "'" + ")")
	
	cursor.commit()

def closeDB():
	cursor.close()