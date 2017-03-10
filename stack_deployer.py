#!/usr/bin/python
"""The following script demonstrates how to deploy an OpenStack HEAT Template
multiple times with different parameters each time


Author: Graham Land
Date: 08/03/17
Twitter: @allthingsclowd
Github: https://github.com/allthingscloud
Blog: https://allthingscloud.eu


"""
from k5regionapiv1 import *
from k5contractsettingsV12 import *
from simple_3_node_stack import *
from time import sleep



def main():
    """Summary

    Returns:
        TYPE: Description
    """
    global demoTemplate
    global stackBatch

    deployedStackIds = {}

    # Get a project scoped token
    k5token = get_scoped_token(adminUser, adminPassword, contract, demoProjectAid, region)

    # Deploy the stacks from the batch list
    for parameters in stackBatch1:
    	stackname = unicode(parameters.get('flavorName')) + unicode("-Perf-Test") 
    	stackId = deploy_heat_stack(k5token, stackname, demoTemplate, parameters).json()['stack'].get('id')
    	deployedStackIds[stackname] = stackId
    	sleep(10)

    deployedStacksOnline = False
    deployedStackFailure = False

    # Loop until all stacks have finished building - either failed or successful
    while not deployedStacksOnline:
    	deployedStacksOnline = True
    	for newStack in list_heat_stacks(k5token).json()['stacks']:
    		print "Stack ID & Status > ", newStack.get('stack_name'), newStack.get('stack_status'), "\n"
    		if ('FAIL' or 'ERROR') in newStack.get('stack_status'):
    			deployedStackFailure = True
    		if 'PROGRESS' in newStack.get('stack_status'):
    			deployedStacksOnline = False
    	sleep(5)


    # List all the stack outputs
    DeploymentResults = ""
    for stackName, stackId in deployedStackIds.iteritems():
		ipList = ""
		try:    	 
			serverips = get_stack_details(k5token, stackName, stackId).json()['stack'].get('outputs')
			for ip in serverips:
				ipList = ipList + unicode(ip.get('output_value')) + "\t"
			stackDetails = stackName + "\t" + ipList
		except:
			stackDetails = stackName + " <<<<<<<<<<<<< Deployment Error\n"

		print stackDetails
		DeploymentResults = DeploymentResults + stackDetails + "\n"

    # Print Error Warnings
    if deployedStackFailure:
    	print "WARNING: There was a stack deployment failure\n"

    # Deployment Complete
    print "Deployment Complete\n"
    print DeploymentResults


if __name__ == "__main__":
    main()
