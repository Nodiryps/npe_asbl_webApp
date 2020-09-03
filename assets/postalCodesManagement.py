# import json


# def get_belgium_postal_codes_FR():
#     print(':::get_belgium_postal_codes_FR:::')
#     data = json.loads(POSTAL_CODES_BEL_FR)
#     fields = []
#     localities = []
#     codes = []
#     # print(data['postalCodes'])

#     for postalCode in data['postalCodes']:
#         fields.append(postalCode['fields'])

#     for field in fields:
#         localities.append(field['localite'])
#         codes.append(field['code_postal'])

#     with open('assets/myPostalCodes.json', 'w') as myFile:
#         myFile.write(str(dict(zip(localities, codes))))