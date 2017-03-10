![openstack heat cookie cutterv2](https://cloud.githubusercontent.com/assets/9472095/23799593/fb63e52c-05a0-11e7-98d1-521e2ee34424.jpg)

# K5_Stack_Deployer - OpenStack Template

Author: Graham Land

Date: 08/03/17

Twitter: @allthingsclowd

Github: https://github.com/allthingscloud

Blog: https://allthingscloud.eu


## deploy_stacks.py

This script demonstrates how to deploy an OpenStack HEAT Template
multiple times with different parameters each time

## k5regionapiv1.py

This file is imported by deploy_stacks.py and contains K5/OpenStack API Function Wrappers

## simple_3_node_stack.py

This file simply contains the YAML HEAT Stack wrapped up as a string for use in python

## simple_3_node_stack.yml

Is the native HEAT template being deployed (Not used just if you wanted to play with separately)

##  k5contractsettingsV12.py

You MUST configure this file to match your environment before deploying.
It contains an environmental section and an application section.
The environmental section is where you enter your K5 details whilst the application section is where the 'batches' of parameters to be fed into the heat template are configured.
Each batch contains list of Heat Template input parameters - each parameter list represents a deployed heat template.


Link to Github
https://github.com/allthingsclowd/Fujitsu_OpenStack_K5_Heat_Cookie_Cutter





