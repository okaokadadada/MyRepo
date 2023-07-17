import numpy as np
import time
import board
import busio
import adafruit_gps
import csv

#GPS取得（緯度、経度）
def getGps():
	i2c = busio.I2C(board.SCL, board.SDA)
	gps = adafruit_gps.GPS_GtopI2C(i2c) # Use I2C interface
	gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
	gps.send_command(b"PMTK220,1000")
	timestamp = time.monotonic()

	while True:
		time.sleep(0.1)
		gps.update()
		data = gps.read(32) # read up to 32 bytes
		latitude_list = []
		longitude_list = []
		n = 0
		while n < 5:
			# convert bytearray to string
			# data_string = "".join([chr(b) for b in data])
			gps.update()
			data = gps.read(32)
			if gps.latitude is not None and gps.longitude is not None:
				# data_string = "".join([chr(b) for b in data])
				# gps.update()
				latitude_list.append(gps.latitude)
				longitude_list.append(gps.longitude)
				n += 1
			if n ==4:
				return(latitude_list, longitude_list)
		if time.monotonic() - timestamp > 5:
			# every 5 seconds...
			gps.send_command(b"PMTK605") # request firmware version
			timestamp = time.monotonic()

# gpsからゴール基準で自己位置を求める関数(国土地理院より)
def getXY(gps_latitude, gps_longitude, goal_latitude, goal_longitude):
	
	""" 緯度経度を平面直角座標に変換する
	- input:
	(gps_latitude, gps_longitude): 変換したい緯度・経度[度]（分・秒でなく小数であることに注意）
	(goal_latitude, goal_longitude): 平面直角座標系原点の緯度・経度[度]（分・秒でなく小数であることに注意）
	- output:
	x: 変換後の平面直角座標[m]
	y: 変換後の平面直角座標[m]
	"""
	# 緯度経度・平面直角座標系原点をラジアンに直す
	phi_rad = np.deg2rad(gps_latitude)
	lambda_rad = np.deg2rad(gps_longitude)
	phi0_rad = np.deg2rad(goal_latitude)
	lambda0_rad = np.deg2rad(goal_longitude)
	
	# 補助関数
	def A_array(n):
		A0 = 1 + (n**2)/4. + (n**4)/64.
		A1 = -     (3./2)*( n - (n**3)/8. - (n**5)/64. )
		A2 =     (15./16)*( n**2 - (n**4)/4. )
		A3 = -   (35./48)*( n**3 - (5./16)*(n**5) )
		A4 =   (315./512)*( n**4 )
		A5 = -(693./1280)*( n**5 )
		return np.array([A0, A1, A2, A3, A4, A5])

	def alpha_array(n):
		a0 = np.nan # dummy
		a1 = (1./2)*n - (2./3)*(n**2) + (5./16)*(n**3) + (41./180)*(n**4) - (127./288)*(n**5)
		a2 = (13./48)*(n**2) - (3./5)*(n**3) + (557./1440)*(n**4) + (281./630)*(n**5)
		a3 = (61./240)*(n**3) - (103./140)*(n**4) + (15061./26880)*(n**5)
		a4 = (49561./161280)*(n**4) - (179./168)*(n**5)
		a5 = (34729./80640)*(n**5)
		return np.array([a0, a1, a2, a3, a4, a5])

	# 定数 (a, F: 世界測地系-測地基準系1980（GRS80）楕円体)
	m0 = 0.9999 
	a = 6378137.
	F = 298.257222101

	# (1) n, A_i, alpha_iの計算
	n = 1. / (2*F - 1)
	A_array = A_array(n)
	alpha_array = alpha_array(n)

	# (2), S, Aの計算
	A_ = ( (m0*a)/(1.+n) )*A_array[0] # [m]
	S_ = ( (m0*a)/(1.+n) )*( A_array[0]*phi0_rad + np.dot(A_array[1:], np.sin(2*phi0_rad*np.arange(1,6))) ) # [m]

	# ここまで定数．今後はA_，　S_，　alpha_arrayのみを利用

	# (3) lambda_c, lambda_sの計算
	lambda_c = np.cos(lambda_rad - lambda0_rad)
	lambda_s = np.sin(lambda_rad - lambda0_rad)

	# (4) t, t_の計算
	t = np.sinh( np.arctanh(np.sin(phi_rad)) - ((2*np.sqrt(n)) / (1+n))*np.arctanh(((2*np.sqrt(n)) / (1+n)) * np.sin(phi_rad)) )
	t_ = np.sqrt(1 + t*t)

	# (5) xi', eta'の計算
	xi2  = np.arctan(t / lambda_c) # [rad]
	eta2 = np.arctanh(lambda_s / t_)

	# (6) x, yの計算
	X = A_ * (xi2 + np.sum(np.multiply(alpha_array[1:],
				       np.multiply(np.sin(2*xi2*np.arange(1,6)),
						   np.cosh(2*eta2*np.arange(1,6)))))) - S_ # [m]
	Y = A_ * (eta2 + np.sum(np.multiply(alpha_array[1:],
					np.multiply(np.cos(2*xi2*np.arange(1,6)),
						    np.sinh(2*eta2*np.arange(1,6)))))) # [m]

	return (Y, X) # [m]，(x_now, y_now)で，軸が反転している．


def write_csv(latitude, longitude, x, y):
	data_csv = [latitude, longitude, x, y]
	dat = 1
	folder_name = "goal"
# 	file_name = "gps.csv"
# 	file_name = "goal.csv"
	
	if (x is not None) and (y is not None):
		with open(file_name, 'a') as f:
			writer = csv.writer(f)
			writer.writerow(data_csv)


if __name__ == "__main__":

	goal_latitude = 36.1124
	goal_longitude = 140.0988
	x = 0.0
	y = 0.0
	
	
	while True:
		i = 0
		# 緯度，経度の取得		
		latitude_list, longitude_list = getGps()
		latitude = np.average(latitude_list)
		longitude = np.average(longitude_list)
		# 緯度，経度からxy座標に変換
		x, y = getXY(latitude, longitude, goal_latitude, goal_longitude)
		write_csv(latitude, longitude, x, y)

		# 出力 		
		print(f"latitude={latitude}, longitude={longitude}")
		print(f"x={x}, y={y}")
		time.sleep(0.5)
