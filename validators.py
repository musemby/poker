import re

def validate_card_code(string):
	return re.match('[a,A,k,K,q,Q,j,J,10]{0,1}[2-9]{0,1}[o,O,c,C,d,D,h,H,s,S]', string)