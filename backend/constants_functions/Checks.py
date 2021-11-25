from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def email_check(value):
	try:
		validate_email(value)
	except ValidationError as e:
		return False
	else:
		return True

def min_max_value_check(minvalue,maxvalue,value):
	if(value<minvalue or value>maxvalue):
		return False
	else:
		return True
def min_max_length_check(minlength,maxlength,value):
	if(len(value)<minlength or len(value)>maxlength):
		return False
	else:
		return True

def min_words_in_paragraph(maxlength,value):
	res = len(value.split())
	if(res>maxlength):
		return False
	else:
		return True

def min_max_date(min_date,max_date,value):
	if(value<min_date or value>max_date):
		return False
	else:
		return True

def length_check(length,value):
	if(length != value):
		return False
	else:
		return True




# def convert_amount_to_words(num):
# 	ones = ["", "One ", "Two ", "Three ", "Four ", "Five ", "Six ", "Seven ", "Eight ", "Nine ", "Ten ", "Eleven ", "Twelve ", "Thirteen ", "Fourteen ", "Fifteen ", "Sixteen ", "Seventeen ", "Eighteen ", "Nineteen "]

# 	twenties = ["", "", "Twenty ", "Thirty ", "Forty ", "Fifty ", "Sixty ", "Seventy ", "Eighty ", "Ninety "]

# 	thousands = ["", "Thousand ", "Lac ", "billion ", "trillion ", "quadrillion ", "quintillion ", "sextillion ", "septillion ", "octillion ", "nonillion ", "decillion ", "undecillion ", "duodecillion ", "tredecillion ", "quattuordecillion ", "quindecillion", "sexdecillion ", "septendecillion ", "octodecillion ", "novemdecillion ", "vigintillion "]

# 	def num99(n):
# 		c = int(n % 10)  # singles digit
# 		b = int(((n % 100) - c) / 10)  # tens digit

# 		t = ""
# 		h = ""
# 		if b <= 1:
# 			h = ones[n % 100]
# 		elif b > 1:
# 			h = twenties[b] + ones[c]
# 		st = t + h
# 		return st

# 	def num999(n):
# 		c = int(n % 10)  # singles digit
# 		b = int(((n % 100) - c) / 10)  # tens digit
# 		a = int(((n % 1000) - (b * 10) - c) / 100)  # hundreds digit
# 		t = ""
# 		h = ""
# 		if a != 0 and b == 0 and c == 0:
# 			t = ones[a] + "Hundred "
# 		elif a != 0:
# 			t = ones[a] + "Hundred and "
# 		if b <= 1:
# 			h = ones[n % 100]
# 		elif b > 1:
# 			h = twenties[b] + ones[c]
# 		st = t + h
# 		return st

# 	def num2word(num):
# 		if num == 0:
# 			return 'zero'
# 		if num <= 99:
# 			return num99(num)
# 		if num <= 999:
# 			return num999(num)
# 		else:
# 			n = str(num)
# 			word = num999(int(n[-3:]))
# 			n = n[:-3]
# 			i = 1
# 			while(len(n) > 0):
# 				word = num99(int(n[-2:])) + thousands[i] + word
# 				i = i + 1
# 				n = n[:-2]

# 		return word[:-1]

# 	return num2word(num)


# def Comma_function(number):
# 	number = str(number)
# 	number_len = len(number)
# 	if len(number) > 3:
# 		number = number[:number_len - 3] + "," + number[-3:]

# 	if len(number) > 6:
# 		temp_data = ""
# 		for index, x in enumerate(number[:-4][::-1]):
# 			temp_data = temp_data + x
# 			if index % 2 == 1:
# 				temp_data = temp_data + ","

# 		number = temp_data[::-1] + number[-4:]
# 	if number[0] is ",":
# 		number = number[1:]
# 	return number


# def get_suffix(i):
# 	j = i % 10
# 	k = i % 100
# 	if (j == 1 and k != 11):
# 		return str(i) + "ST"
# 	if (j == 2 and k != 12):
# 		return str(i) + "ND"
# 	if (j == 3 and k != 13):
# 		return str(i) + "RD"

# 	return str(i) + "TH"




