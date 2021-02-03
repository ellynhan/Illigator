import mysql.connector
import banner

isDbExist = False
isLinkTableExist = False
isSimTableExist = False
isTableEmpty = False

mydb = mysql.connector.connect(
    host="host",
    user="user",
    password="password"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for name in mycursor:
  if name[0] == 'tag_similiar':
      isDbExist = True

if isDbExist == False :
    mycursor.execute("CREATE DATABASE tag_similiar")

mycursor.execute("USE tag_similiar")
mycursor.execute("SHOW TABLES")

for tables in mycursor:
  if tables[0] == 'webinfo':
      isLinkTableExist = True

if isLinkTableExist == False:
    mycursor.execute("CREATE TABLE WebInfo (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255) NOT NULL, tags TEXT, banners TEXT)")

mycursor.execute("SELECT * FROM WebInfo")
cnt = 0
for rows in mycursor:
    cnt+=1

if cnt == 0:
    isTableEmpty = True
#
#
# def updateDB(url, banners):
#     sql = "INSERT INTO WebInfo (url, banners) VALUES (%s, %s)"
#     mycursor.execute()

mycursor.execute("SHOW TABLES")

for tables in mycursor:
  if tables[0] == 'Similiar':
      isSimTableExist = True


if isSimTableExist == False:
    mycursor.execute("CREATE TABLE Similiar (id INT AUTO_INCREMENT PRIMARY KEY, src INT NOT NULL, dest INT NOT NULL, tag FLOAT, banner FLOAT)")

external_links = banner.extract_external_link('url')
mycursor.execute(f"INSERT INTO webinfo (url,banners) VALUES({'url'}, {external_links})")
mydb.commit()

src_link = mycursor.execute(f"SELECT banners FROM webinfo where url == {'url'}")
dest_link = mycursor.execute(f"SELECT banners FROM webinfo where url == {'url'}")
similiar_score = banner.compare_banner_link(src_link, dest_link)
mycursor.execute(f"INSERT INTO similiar (banner) VALUES({similiar_score})")
mydb.commit()
