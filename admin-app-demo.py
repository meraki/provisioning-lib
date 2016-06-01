#!/usr/bin/python2.7

import json, cgi, cgitb, requests
cgitb.enable()


#Create instance of FieldStorage:
form = cgi.FieldStorage()
email = form.getvalue('email')

#Basic API connectivity variables:
# SET YOUR ADMIN AUTH KEY here!!!!!!!!!!!!!!!!!!!!
#authkey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
authkey= form.getvalue('APIkey')

orgurl="https://dashboard.meraki.com/api/v0/organizations"

authheader = {"X-Cisco-Meraki-API-Key":authkey,"Content-type":"application/json"}

#Proove Checkboxes to delete/add orgs for an admin
if form.getlist('nonorg'):
        adnonorgs = form.getlist('nonorg')
if form.getlist('org'):
        adorgs = form.getlist('org')


#HTML header and end
myheader = '''
      <html><body><title>Dashboard Admin Mgmt.</title><link rel="shortcut icon" href="http://localhost/pic/M.ico"/>
          <div align="center">
          <br><h1>Admin Management Application</h1><br>
          '''

myend = '''
  </b><br>
  <div align="center">(Copyright Georg Prause - Cisco Meraki- 2015)</div>
  </body></html>
  '''

#Get all admin-emails of an Organization
def getadmins(orgid):
        global authkey,orgurl
        adminnames=[]
        adminurl=orgurl+"/"+str(orgid)+"/admins"
        admins=requests.get(adminurl, headers=authheader).text
        result = json.loads(admins)
        for d in result:
                for key, value in d.iteritems():
                        if key=='email':
                                adminnames.append(value)
        return adminnames

#Get adminid for respective admin-email
def getadminid(orgid,email):
        global authkey,orgurl
        adminurl=orgurl+"/"+str(orgid)+"/admins"
        admins=requests.get(adminurl, headers=authheader).text
        result = json.loads(admins)
        for i in result:
               if i['email']==email:
                        return i['id']
        
#Get all Organization / full json-result for orgs
def getallorgsinfo():
        global authkey, orgurl
        orgs=requests.get(orgurl, headers=authheader).text
        result = json.loads(orgs)
        return result

#Filter IDs of Org Dictionary
def getallorgsid(orgsinfo):
        allorgs=[]
        for d in orgsinfo:
                for key, value in d.iteritems():
                        if key=='id':
                                allorgs.append(value)
        return allorgs

#Get the Org-Name of a specific org-id
def getorgname(id,allorgsinfo):
        for d in allorgsinfo:
                if d["id"]==id:
                        return d["name"]


#Which orgs is the user an admin of
def checkadmin(adminname,allorgsinfo):
        adminorgs=[]
        allorgs=getallorgsid(allorgsinfo)
        for x in allorgs:
                adminnames=getadmins(str(x))
                for y in adminnames:
                        if y==adminname:
                                adminorgs.append(x)
        return adminorgs

#Which orgs is the user NOT and admin of
def checknotadmin(partof,allorgsinfo):
        notadminorgs=[]
        allorgs=getallorgsid(allorgsinfo)
        for x in allorgs:
                z=0
                for y in partof:
                        if x==y:
                                z=z+1
                if z==0:
                        notadminorgs.append(x)
        return notadminorgs


#Which shardnumber is the org running on
def getshard(orgid):
        global authkey, orgurl
        snmpurl=orgurl+"/"+orgid+"/snmp"
        orgs=requests.get(snmpurl, headers=authheader).text
        result = json.loads(orgs)
        return result["hostname"]

#Add user to an org
def adduser(nonorgs,email):
        privilege={"name":"added via API", "email":email,"orgAccess":"full"}
        datajson = json.dumps(privilege)
        for i in nonorgs:
               posturl="https://"+getshard(i)+"/api/v0/organizations/"+i+"/admins"
               newadmin=requests.post(posturl, data = datajson, headers=authheader).text

#Delete user of an org
def deluser(orgs,email):
        global authheader, orgurl
        for i in orgs:
                j=getadminid(i,email)
                posturl="https://"+getshard(i)+"/api/v0/organizations/"+str(i)+"/admins/"+str(j)
                deladmin=requests.delete(posturl,headers=authheader).text
                

#MAIN PART
print
print myheader
if form.getlist('nonorg'):
        adduser(adnonorgs,email)

if form.getlist('org'):
        deluser(adorgs,email)
              

if email and "@" in email:
        allorgsinfo = getallorgsinfo()
        partof=checkadmin(email,allorgsinfo)
        notpartof=checknotadmin(partof,allorgsinfo)
        print '<form action="/cgi-bin/admin-app-demo.py" method="post">'
        print email + ' is part of the following Organizations</br> Check the box if you would like to delete this admin out of some organizations <input type=hidden name="email" value="' + email + '"> <input type=hidden name="APIkey" value="' + authkey + '">'
        print '<table style="width:25%"><tr><td><b>Organization</b></td><td><b>delete??</b></td></tr>'
        for i in partof:
                orgname=getorgname(i,allorgsinfo)
                print '<tr><td>' + orgname + '</td><td><input type="checkbox" name="org" value="'+str(i)+'"></td></tr></br>'
        
        print "</table></br></br>" + email + " is NOT part of the following Organizations</br> Check the box if you would like to ADD this admin to some of these organizations</br></br>"
        print '<table style="width:25%"><tr><td><b>Organization</b></td><td><b>add??</b></td></tr>'
        for i in notpartof:
                orgname=getorgname(i,allorgsinfo)
                print '<tr><td>' + orgname + '</td><td><input type="checkbox" name="nonorg" value="'+str(i)+'"></td></tr></br>'
        print '</table><input type="submit" value="Submit" /> </form>'


else:

        print '''<form action="/cgi-bin/admin-app-demo.py" method="post"> Admin-E-Mail: <input type="text" name="email"> <input type="submit" value="Submit" /> <br><br><br>
        API-Key: <input type="text" name="APIkey"></form>'''

print myend
