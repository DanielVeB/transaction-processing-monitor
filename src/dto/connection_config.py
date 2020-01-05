# DB credentials
DATABASE_URI = "localhost"
PORT = ":3306"
DATABASE_NAME = "test"
USERNAME = "root"
PASSWORD = "root"

# TODO: takie przechowywanie URI jest slabe ale to na koncu sie zajme zeby to do jakiegos slownika wrzucic czy cos
MYSQL_URI = "mysql://" + USERNAME + ":" + PASSWORD + "@" + DATABASE_URI + PORT + "/" + DATABASE_NAME
POSTGRES_URI = "postgresql://" + USERNAME + ":" + PASSWORD + "@" + DATABASE_URI + PORT + "/" + DATABASE_NAME
ORACLE_URI = "oracle://" + USERNAME + ":" + PASSWORD + "@" + DATABASE_URI + PORT + "/" + DATABASE_NAME
