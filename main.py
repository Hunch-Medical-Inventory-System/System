import classTypes as CT
import datetime

data = CT.parseJSON('connect.json')

dbConnect = CT.dbConnection(
        data['connectioninfo'][0]['host'],
        data['connectioninfo'][0]['user'],
        data['connectioninfo'][0]['password'],
        data['connectioninfo'][0]['database'],
        data['connectioninfo'][0]['port']
    )
dbConnect.initiate()
print(CT.userManage(dbConnect).historyRetrieve("78b3833f-a0b3-423c-a03f-8633b4187420"))
dbConnect.close()  