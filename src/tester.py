#!/usr/bin/python
'''
Created on 13.09.2011

@author: corwin

вот здесь вот будет временый псевдо тестер... потом заменю на  нормальный 
'''
import json
import os
import parser
import errors

def load_test(path):
	test_text = "" #потом прицеплю что б изфайла считывала
	test_requests = ()
	
	q =0
	start =0
	index = 0
	for ch in test_text:
		if ch == "{":
			q +=1
			if q == 1:
				start = index
		elif ch == "}":
			q -=1
			if q == 0:
				test_requests.append(test_text[start:index])
		index +=1
	return

fails_test =0;
ok_test = 0;

test_num =0

def fail(s):
	global test_num
	test_num +=1  

	global fails_test
	fails_test += 1

	print("test %1: FAIL (%s)", test_num, s)  

def ok():
	global test_num
	test_num +=1

	global ok_test
	ok_test += 1

	print("test %1: OK", test_num)  


def json_enc(dic):
	json.dumps(dic, sort_keys=True)


def test():
	cmd = {
		"cmd": "",
		"foo": "bar"
	}

	try:
		parser.parse_request(json_enc(cmd))
	except errors.BadRequest:
		ok()
	except:
		fail("unknown exp")   

def main():
	test()
    

if __name__ == '__main__':
    main()