'''
Author: daoyi
'''
import akshare as ak
import datetime


class AKData():
	def suntime(self):
		today = datetime.datetime.today().strftime("%Y%m%d")
		today2 = datetime.datetime.today().strftime("%Y-%m-%d")
		sun = ak.sunrise_daily(date=today, city='北京')
		sunrise = sun["Sunrise"].values[0].split(" ")[0]
		sunset = sun["Sunset"].values[0].split(" ")[0]
		length = sun["Length"].values[0].split(" ")[0]

		msg = [f'[{today2} suntime]', f'sunris: {sunrise}; sunset: {sunset}', f'suntotal: {length}']
		return msg

if __name__ == '__main__':
	AKData().suntime()