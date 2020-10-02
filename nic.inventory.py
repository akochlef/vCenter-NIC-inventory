# NIC inventory
# Anis Kochlef
# 10/02/2020
# akochlef@gmail.com


import json
import requests
import getpass

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

_SESSION = requests.Session()
_SESSION.verify=False
_SESSION_STATUS = 0

vc = input('vCenter IP or FQDN: ')
username = input('Username: ')
password = getpass.getpass()

url = f'https://{vc}/rest/com/vmware/cis/session'
_SESSION.post(url,auth=(username,password))

def nic_info(session,server,vmid):
	url = f'https://{vc}/rest/vcenter/vm/{vmid}'
	r = session.get(url)
	j = json.loads(r.text)
	nics = j['value']['nics']
	name = j['value']['name']
	power_state = j['value']['power_state']
	for nic in nics:
		info = f"{name},{power_state},{nic['value']['label']},{nic['value']['state']},{nic['value']['mac_address']}"
		print(info)
		

def inventory(session,server):
	url = f' https://{server}/rest/vcenter/vm'
	response = session.get(url)
	data = json.loads(response.text)
	vms=data['value']
	for vm in vms:
		vmid = vm['vm']
		nic_info(session,server,vmid)

inventory(_SESSION,vc)

# https://vdc-download.vmware.com/vmwb-repository/dcr-public/423e512d-dda1-496f-9de3-851c28ca0814/0e3f6e0d-8d05-4f0c-887b-3d75d981bae5/VMware-vSphere-Automation-SDK-REST-6.7.0/docs/apidocs/operations/com/vmware/vcenter/vm.get-operation.html

