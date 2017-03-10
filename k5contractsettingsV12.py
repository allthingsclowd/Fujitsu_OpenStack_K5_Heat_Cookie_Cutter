#!/usr/bin/python

# Enter K5 Contract details
adminUser = 'enter username' # k5/openstack user login name
adminPassword = 'enter password' # k5/openstack user password
contract = 'enter contract name' # k5 contract name or openstack domain name
contractid = 'enter contract id'
defaultid = 'enter default project id'
defaultProject = 'enter default project name' # default project id - on k5 it's the project name that starts with contract name and ends with -prj
region = 'uk-1' # target region
az1 = 'uk-1a'
az2 = 'uk-1b'

# K5 external network details
extaz1 = 'df8d3f21-75f2-412a-8fd9-29de9b4a4fa8' # K5 availability zone b external network id
extaz2 = 'd730db50-0e0c-4790-9972-1f6e2b8c4915' # K5 availability zone b external network id

# K5 target Project
demoProjectA = 'enter target project' # k5/openstack demo target project name
demoProjectAid = 'enter target project id' # k5/openstack demo target project id

# APPLICATION DETAILS
# Each row below represents the list of input parameters that will be supplied to an instance of an OpenStack heat template

stackBatch = [	{"flavorName":"P-1","kpName": "k5-loadtest-az1", "cidr": "192.168.200.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"T-1","kpName": "k5-loadtest-az1", "cidr": "192.168.201.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C-1","kpName": "k5-loadtest-az1", "cidr": "192.168.202.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C-2","kpName": "k5-loadtest-az1", "cidr": "192.168.203.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C-4","kpName": "k5-loadtest-az1", "cidr": "192.168.205.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C-8","kpName": "k5-loadtest-az1", "cidr": "192.168.206.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C-16","kpName": "k5-loadtest-az1", "cidr": "192.168.207.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S-1","kpName": "k5-loadtest-az1", "cidr": "192.168.208.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S-2","kpName": "k5-loadtest-az1", "cidr": "192.168.209.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S-4","kpName": "k5-loadtest-az1", "cidr": "192.168.210.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S-8","kpName": "k5-loadtest-az1", "cidr": "192.168.211.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S-16","kpName": "k5-loadtest-az1", "cidr": "192.168.212.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},				
				{"flavorName":"P2-1","kpName": "k5-loadtest-az1", "cidr": "192.168.213.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"T2-1","kpName": "k5-loadtest-az1", "cidr": "192.168.214.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C2-1","kpName": "k5-loadtest-az1", "cidr": "192.168.215.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C2-2","kpName": "k5-loadtest-az1", "cidr": "192.168.216.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C2-4","kpName": "k5-loadtest-az1", "cidr": "192.168.218.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"C2-8","kpName": "k5-loadtest-az1", "cidr": "192.168.219.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},				
				{"flavorName":"S2-1","kpName": "k5-loadtest-az1", "cidr": "192.168.220.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S2-2","kpName": "k5-loadtest-az1", "cidr": "192.168.221.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S2-4","kpName": "k5-loadtest-az1", "cidr": "192.168.222.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"S2-8","kpName": "k5-loadtest-az1", "cidr": "192.168.223.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},				
				{"flavorName":"M2-1","kpName": "k5-loadtest-az1", "cidr": "192.168.224.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"M2-2","kpName": "k5-loadtest-az1", "cidr": "192.168.225.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"},
				{"flavorName":"M2-4","kpName": "k5-loadtest-az1", "cidr": "192.168.226.0/24", "dataVolume": "128", "routerId": "211f42b5-6603-43c5-8abc-2af0839acf3c"}
				]
