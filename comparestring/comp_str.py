def compare_string(first_string, second_string):
	try:
		first_string = float(first_string)
		second_string = float(second_string)
	except TypeError as err:
		print(f"Neither {first_string} or {second_string} is a float")

	if first_string > second_string:
		return f"{first_string} is greater than {second_string}"
	elif first_string < second_string:
		return f"{first_string} is less than {second_string}"
	else:
		return f"{first_string} is equal to {second_string}"
 