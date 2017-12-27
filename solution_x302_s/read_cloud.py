import requests

r = requests.session()
datas = {'sdate': '2017-12-27','edate': '2017-12-27', 'uid': 3}
# datas = {}
response = r.post('http://172.16.5.11/form/Download',data=datas, stream=True)
block = response.text.split('\n')
print(block[0].split('\t')[0])
for elmt in range(len(block)):
    print(elmt+1, block[elmt])
