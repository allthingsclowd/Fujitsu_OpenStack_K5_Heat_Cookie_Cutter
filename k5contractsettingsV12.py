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

targetProjects = {"k5live-0","k5live-1","k5live-2","k5live-3","k5live-4",
			"k5live-5","k5live-6","k5live-7","k5live-8","k5live-9",
			"k5live-10","k5live-11","k5live-12","k5live-13","k5live-14",
			"k5live-15","k5live-16","k5live-17","k5live-18","k5live-19",
			"k5live-20","k5live-21","k5live-22","k5live-23","k5live-24"}


stackBatch_az1 = [	{"my_ip":"31.53.253.24/32","res_prefix":"k5live-az1","dns_servers":"185.149.225.9,185.149.225.10","net_cidr":"192.168.1.0/24","router_int":"192.168.1.1","server_image":"Ubuntu Server 16.04 LTS (English) CTO","key_pair":"K5Live","tzone_region":"Europe","tzone_city":"Helsinki","deploy_az":"de-1a","ext_net":"73598426-3678-4eb6-8131-9007770d3ccd","ext_router":"REPLACE_ME"}
				]

stackBatch_az2 = [	{"my_ip":"31.53.253.24/32","res_prefix":"k5live-az2","dns_servers":"185.149.227.9,185.149.227.10","net_cidr":"192.168.1.0/24","router_int":"192.168.1.1","server_image":"Ubuntu Server 16.04 LTS (English) CTO","key_pair":"K5Live","tzone_region":"Europe","tzone_city":"Helsinki","deploy_az":"de-1b","ext_net":"58e863e5-7d31-4f32-9178-370a3288db42","ext_router":"REPLACE_ME"}
				]
