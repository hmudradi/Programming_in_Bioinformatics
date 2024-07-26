#!usr/bin/env python3
#shebang line
def insert_sting_middle(str, word):
	return str[:2] + word + str[2:]
	
print(insert_sting_middle('****', 'Bold move, Cotton'))
