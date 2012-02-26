'''
Created on 13.09.2011

@author: corwin
'''

global DEBUG
DEBUG = True

PORT = 8080
SERVER = '127.0.0.1'

JSON_DUMPS_FORMAT = {
    "sort_keys": "true",
    "indent": 4,
}

DB_CONFIG = {
    "location": "./db",
    "user": "",
    "password" : ""
}

USERNAME_MIN_LEN = 3
USERNAME_MAX_LEN = 16

PASSWORD_MIN_LEN = 6
PASSWORD_MAX_LEN = 18

usrnameRegexp = r'^[a-z]+[\w_-]{%s,%s}$' % (USERNAME_MIN_LEN- 1, USERNAME_MAX_LEN - 1)
pasRegexp = r'^.{%s,%s}$' % (PASSWORD_MIN_LEN, PASSWORD_MAX_LEN)

DEFAULT_MAPS = [{'mapName': 'defaultMap1', 'playersNum': 2, 'turnsNum': 5}, 
				{'mapName': 'defaultMap2', 'playersNum': 3, 'turnsNum': 5}, 
				{'mapName': 'defaultMap3', 'playersNum': 4, 'turnsNum': 5}, 
				{'mapName': 'defaultMap4', 'playersNum': 5, 'turnsNum': 5},
				{ 'mapName': 'defaultMap5', 'playersNum': 2, 'turnsNum': 5, 
						'regions' : [ 	{ 'population' : 1, 'landDescription' : ['mountain'], 'adjacent' : [3, 4] }, 
										{ 'population' : 1, 'landDescription' : ['sea'], 'adjacent' : [1, 4] }, 
										{ 'population' : 1, 'landDescription' : ['border', 'mountain'], 'adjacent' : [1] }, 
										{ 'population' : 1, 'landDescription' : ['coast'], 'adjacent' : [1, 2] } 
									] 
				}, 
				{ 'mapName': 'defaultMap6', 'playersNum': 2, 'turnsNum': 7, 
						'regions' : [ 	{ 'landDescription' : ['sea', 'border'], 'adjacent' : [2, 17, 18] }, 
										{ 'landDescription' : ['mine', 'border', 'coast', 'forest'],  'adjacent' : [1, 18, 19, 3] }, 
										{ 'landDescription' : ['border', 'mountain'], 'adjacent' : [2, 19, 21, 4] }, 
										{ 'landDescription' : ['farmland', 'border'], 'adjacent' : [3, 21, 22, 5] }, 
										{ 'landDescription' : ['cavern', 'border', 'swamp'],  'adjacent' : [4, 22, 23, 6] }, 
										{ 'population': 1, 'landDescription' : ['forest', 'border'], 'adjacent' : [5, 23, 7] }, 
										{ 'landDescription' : ['mine', 'border', 'swamp'], 'adjacent' : [6, 23, 8, 24, 26] }, 
										{ 'landDescription' : ['border', 'mountain', 'coast'], 'adjacent' : [7, 26, 10, 9, 24] }, 
										{ 'landDescription' : ['border', 'sea'], 'adjacent' : [8, 10, 11] }, 
										{ 'population': 1, 'landDescription' : ['cavern', 'coast'], 'adjacent' : [9, 8, 11, 26] },
										{ 'population': 1, 'landDescription' : ['mine', 'coast', 'forest', 'border'], 'adjacent' : [10, 26, 27, 12] },
										{ 'landDescription' : ['forest', 'border'], 'adjacent' : [11, 27, 30, 13] }, 
										{ 'landDescription' : ['mountain', 'border'], 'adjacent' : [12, 30, 28, 14] },
										{ 'landDescription' : ['mountain', 'border'], 'adjacent' : [13, 28, 16, 15] }, 
										{ 'landDescription' : ['hill', 'border'], 'adjacent' : [14, 16] }, 
										{ 'landDescription' : ['farmland', 'magic', 'border'], 'adjacent' : [15, 20, 28, 17] }, 
										{ 'landDescription' : ['border', 'mountain', 'cavern', 'mine', 'coast'], 'adjacent' : [16, 20, 1, 18] }, 
										{ 'population': 1, 'landDescription' : ['farmland', 'magic', 'coast'], 'adjacent' : [17, 20, 1, 19] }, 
										{ 'landDescription' : ['swamp'],  'adjacent' : [18, 3, 21, 2, 20] }, 
										{ 'population': 1, 'landDescription' : ['swamp'], 'adjacent' : [19, 28, 29, 21] }, 
										{ 'population': 1, 'landDescription' : ['hill', 'magic'], 'adjacent' : [20, 29, 3, 4, 22] },
										{ 'landDescription' : ['mountain', 'mine'], 'adjacent' : [21, 25, 29, 4, 5, 23] }, 
										{ 'landDescription' : ['farmland'], 'adjacent' : [22, 25, 6, 5, 24], 'population': 1},
										{ 'landDescription' : ['hill', 'magic'], 'adjacent' : [23, 26, 7, 25, 8] }, 
										{ 'landDescription' : ['mountain', 'cavern'], 'adjacent' : [24, 22, 23, 26] }, 
										{ 'population': 1, 'landDescription' : ['farmland'], 'adjacent' : [25, 24, 7, 8, 10, 11, 27] }, 
										{ 'population': 1, 'landDescription' : ['swamp', 'magic'], 'adjacent' : [26, 11, 12, 30, 29] }, 
										{ 'population': 1, 'landDescription' : ['forest', 'cavern'], 'adjacent' : [29, 30, 13, 14, 16, 20] },
										{ 'landDescription' : ['sea'], 'adjacent' : [28, 20, 21, 22, 25, 27, 30] }, 
										{ 'landDescription' : ['hill'], 'adjacent' : [29, 28, 13, 12, 27] }, ] }, 
				{ 'mapName': 'defaultMap7', 'playersNum': 2, 'turnsNum': 5, 
						'regions' : [ 	{ 'landDescription' : ['border', 'mountain', 'mine', 'farmland','magic'], 'adjacent' : [2] }, 
										{ 'landDescription' : ['mountain'], 'adjacent' : [1, 3] },
										{ 'landDescription' : ['mountain', 'mine'], 'adjacent' : [2, 4], 'population': 1}, 
										{ 'landDescription' : ['mountain'], 'adjacent' : [3, 5],'population': 1 }, 
										{ 'landDescription' : ['mountain', 'mine'], 'adjacent' : [4] } ] } 

]
