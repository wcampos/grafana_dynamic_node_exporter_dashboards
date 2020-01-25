import boto3,json,tabulate,pprint,itertools,os,random,string,pwd,grp
from shutil import copyfile

Instances=[]
TemplateFile="./templates/node_exporter_dashboard.json"
GrafanaDashPath="/var/lib/grafana/dashboards"
GrafanaUID=pwd.getpwnam("grafana").pw_uid
GrafanaGID=grp.getgrnam("grafana").gr_gid
MYDashPath=GrafanaDashPath+"/mydashboards"

def createDirNPermissions(dirin):
    if not os.path.exists(dirin):
       os.makedirs(dirin)
       os.chown(dirin,GrafanaUID,GrafanaGID)

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def replaceInFile(fin,key,val):
    with open(fin, 'r') as f:
        newlines = []
        for line in f.readlines():
            newlines.append(line.replace(key,val))
    with open(fin, 'w') as f:
        for line in newlines:
           f.write(line)

createDirNPermissions(GrafanaDashPath)
createDirNPermissions(MYDashPath)

ec2 = boto3.client('ec2')
filters = [
    {
        'Name': 'tag:MACHINETAGKEY',
        'Values': ['MACHINESTAGVAL']
    }
]
list_instances=json.dumps(ec2.describe_instances(Filters=filters), indent=4, sort_keys=True, default=str)
data = json.loads(list_instances)
idict={}
ilist=[]

for reservations in data['Reservations']:
    for instance in reservations['Instances']:
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
               iName =  tag['Value']
               iName = iName.replace(" ","")
               iPrivateDNS = instance['PrivateDnsName']
               dashUid = randomString(10)
               path=MYDashPath+"/"+iName+"-dashboards.json"
               copyfile(TemplateFile,path)
               os.chown(path,GrafanaUID,GrafanaGID)
               Replacements={'MACHINENAME': iName, 'MACHINEIPADDR': iPrivateDNS, 'DASHBOARDUID': dashUid}
               for k,v in Replacements.items():
                   replaceInFile(path,k,v)
