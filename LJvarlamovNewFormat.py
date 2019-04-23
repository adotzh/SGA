import json
import shelve

LJ_user_filename = '/home/ubuntu/varlamov-data/lj-user-2017-03-06.json'
LJDataForGraph = shelve.open('LJNewFormat')


#create new format for data
print('Start create new data format')
i = 0
with open(LJ_user_filename, 'r') as data_profile:
   for one_profile_info in data_profile:
       one_profile_info = json.loads(one_profile_info)
       if str(one_profile_info['value']['status']) == 'active':
           if i % 100000 == 0:
               print(i, one_profile_info)
           try:
               LJDataForGraph[str(one_profile_info['value']['login'])] = int(one_profile_info['value']['id'])
           except UnicodeError:
               print('UnicodeError, ', one_profile_info['value']['login'])
           except LookupError:
               print('LookupError, ', one_profile_info)
           i += 1
print('Finish create new data format')