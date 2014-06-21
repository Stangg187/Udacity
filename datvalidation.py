months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
		  
month_abbvs = dict((m[:3].lower(), m) for m in months)
          
def valid_month(month):
	if month:
		short_month = month[:3].lower()
		return month_abbvs.get(short_month)

def valid_day(day):
    if day.isdigit() and 1 <= int(day) <= 31:
        return int(day)


def valid_year(year)
	if year.isdigit() and 1900 <= int(year) <= 31:
		return int(year)