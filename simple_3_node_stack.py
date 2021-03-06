#!/usr/bin/python
"""The following script simply wraps 
  an OpenStack YAML HEAT Template in a string for deployment through
  the OpenStack Orchestration API


Author: Graham Land
Date: 08/03/17
Twitter: @allthingsclowd
Github: https://github.com/allthingscloud
Blog: https://allthingscloud.eu


"""

demoTemplate = """
---
heat_template_version: 2013-05-23
# Author: Graham Land
# Date: 08/03/2017
# Purpose: Fujitsu K5 OpenStack IaaS Heat Template that deploys 3 servers on a new network and attaches the network to a given router.
#          Input parameters -
#               routerId - unique id of the router that the network should be attached to
#               imageName - the image OS that will be deployed
#               flavorName - the vcpu and ram size of the servers
#               dataVolume - the size of the data volume to be attached to the servers
#               cidr - private network ip address details
#               azName - the availability zone to deploy the servers in - obviously this need to be the same as the router location
#               kpName - the name of an existing ssh key pair to use in the availability zone
#
#
#          Output parameters - the ip addresses of the 3 servers
#
# Twitter: @allthingsclowd
# Blog: https://allthingscloud.eu
#

description: Fujitsu K5 OpenStack IaaS Heat Template that deploys 3 servers on a new network and attaches the network to a given router.

# Input parameters
parameters:
  imageName:
    type: string
    label: Image name or ID
    description: Image to be used for compute instance
    default: "Ubuntu Server 14.04 LTS (English) 02"    
  flavorName:
    type: string
    label: Flavor
    description: X vCPU and XXXXMB RAM
    default: "T-1"
  kpName:
    type: string
    label: Key name
    description: Name of key-pair to be used for compute instance
    default: "k5-loadtest-az1"
  cidr:
    type: string
    label: ip address details
    description: network address range
    default: "10.99.99.0/24"
  dataVolume:
    type: string
    label: volume size
    description: size in GB of datavolume to attach to server
    default: "3"
  osVolume:
    type: string
    label: volume size
    description: size in GB of OS volume to attach to server
    default: "20"
  azName:
    type: string
    label: Availability Zone
    description: Region AZ to use
    default: "uk-1a"
  securityGroup:
    type: string
    label: Existing K5 security group name
    description: Project Security Group
    default: "demosecuritygroup"
  routerId:
    type: string
    label: External Router
    description: Router with external access for global ip allocation
    default: "fcb1dddc-e0c8-4dd5-8a3f-4eee3b042912"

# K5 Infrastructure resources to be built
resources:

############################ Network Resources ####################

  # Create a private network in availability
  demostack_private_net :
    type: OS::Neutron::Net
    properties:
      name: "private"
      availability_zone: { get_param: azName}
      
  # Create a new subnet on the private network
  demostack_private_subnet :
    type: OS::Neutron::Subnet
    depends_on: demostack_private_net 
    properties:
      availability_zone: { get_param: azName}
      network_id: { get_resource: demostack_private_net  }
      cidr: { get_param: cidr}
      dns_nameservers: ["62.60.39.9", "62.60.39.10"]

  # Connect an interface on the demostacks network's subnet to the router
  router_interface:
    type: OS::Neutron::RouterInterface
    depends_on: [demostack_private_subnet ]
    properties:
      router_id: { get_param: routerId }
      subnet_id: { get_resource: demostack_private_subnet  }


  ################## Servers  Resources ###########################

  ################################ create server demo-mgmt1-server ##############################

  # Create a data volume for use with the server
  demo-mgmt1-server-data-vol:
    type: OS::Cinder::Volume
    properties:
      availability_zone: { get_param: azName}
      description: data Storage
      size: { get_param: dataVolume}
      volume_type: "M1"

  # Create a system volume for use with the server
  demo-mgmt1-server-sys-vol:
    type: OS::Cinder::Volume
    properties:
      availability_zone: { get_param: azName}
      size: { get_param: osVolume}
      volume_type: "M1"
      image : { get_param: imageName }

  # Build a server using the system volume defined above
  demo-mgmt1-server:
    type: OS::Nova::Server
    depends_on: [ demostack_private_subnet ]
    properties:
      key_name: { get_param: kpName }
      image: { get_param: imageName }
      flavor: { get_param: flavorName }
      security_groups: [{get_param: securityGroup}]
      block_device_mapping: [{"volume_size": { get_param: osVolume}, "volume_id": {get_resource: demo-mgmt1-server-sys-vol}, "delete_on_termination": True, "device_name": "/dev/vda"}]
      admin_user: "ubuntu"
      metadata: { "fcx.autofailover": True, "Example Custom Tag": "Multiple Server Build" }
      user_data:
        str_replace:
          template: |
            #cloud-config
            write_files:
              - content: |
                  #!/bin/bash
                  voldata_id=%voldata_id%
                  voldata_dev="/dev/disk/by-id/virtio-$(echo ${voldata_id} | cut -c -20)"
                  mkfs.ext4 ${voldata_dev}
                  mkdir -pv /mnt/appdata
                  echo "${voldata_dev} /mnt/appdata ext4 defaults 1 2" >> /etc/fstab
                  mount /mnt/appdata
                  chmod 0777 /mnt/appdata
                path: /tmp/format-disks
                permissions: '0700'
            runcmd:
              - /tmp/format-disks
          params:
            "%voldata_id%": { get_resource: demo-mgmt1-server-data-vol }
      user_data_format: RAW
      networks: ["uuid": {get_resource: demostack_private_net} ]

  # Attach previously defined data-vol to the server
  attach-demo-mgmt1-server-data-vol:
    type: OS::Cinder::VolumeAttachment
    depends_on: [ demo-mgmt1-server-data-vol, demo-mgmt1-server ]
    properties:
      instance_uuid: {get_resource: demo-mgmt1-server}
      mountpoint: "/dev/vdb"
      volume_id: {get_resource: demo-mgmt1-server-data-vol}
  ################################ create server demo-mgmt2-server ##############################

  # Create a data volume for use with the server
  demo-mgmt2-server-data-vol:
    type: OS::Cinder::Volume
    properties:
      availability_zone: { get_param: azName}
      description: data Storage
      size: { get_param: dataVolume}
      volume_type: "M1"

  # Create a system volume for use with the server
  demo-mgmt2-server-sys-vol:
    type: OS::Cinder::Volume
    properties:
      availability_zone: { get_param: azName}
      size: { get_param: osVolume}
      volume_type: "M1"
      image : { get_param: imageName }

  # Build a server using the system volume defined above
  demo-mgmt2-server:
    type: OS::Nova::Server
    depends_on: [ demostack_private_subnet ]
    properties:
      key_name: { get_param: kpName }
      image: { get_param: imageName }
      flavor: { get_param: flavorName }
      block_device_mapping: [{"volume_size": { get_param: osVolume}, "volume_id": {get_resource: demo-mgmt2-server-sys-vol}, "delete_on_termination": True, "device_name": "/dev/vda"}]
      admin_user: "ubuntu"
      security_groups: [{get_param: securityGroup}]
      metadata: { "fcx.autofailover": True, "Example Custom Tag": "Multiple Server Build" }
      user_data:
        str_replace:
          template: |
            #cloud-config
            write_files:
              - content: |
                  #!/bin/bash
                  voldata_id=%voldata_id%
                  voldata_dev="/dev/disk/by-id/virtio-$(echo ${voldata_id} | cut -c -20)"
                  mkfs.ext4 ${voldata_dev}
                  mkdir -pv /mnt/appdata
                  echo "${voldata_dev} /mnt/appdata ext4 defaults 1 2" >> /etc/fstab
                  mount /mnt/appdata
                  chmod 0777 /mnt/appdata
                path: /tmp/format-disks
                permissions: '0700'
            runcmd:
              - /tmp/format-disks
          params:
            "%voldata_id%": { get_resource: demo-mgmt2-server-data-vol }
      user_data_format: RAW
      networks: ["uuid": {get_resource: demostack_private_net} ]

  # Attach previously defined data-vol to the server
  attach-demo-mgmt2-server-data-vol:
    type: OS::Cinder::VolumeAttachment
    depends_on: [ demo-mgmt2-server-data-vol, demo-mgmt2-server ]
    properties:
      instance_uuid: {get_resource: demo-mgmt2-server}
      mountpoint: "/dev/vdb"
      volume_id: {get_resource: demo-mgmt2-server-data-vol}

  ################################ create server demo-mgmt3-server ##############################

  # Create a data volume for use with the server
  demo-mgmt3-server-data-vol:
    type: OS::Cinder::Volume
    properties:
      availability_zone: { get_param: azName}
      description: data Storage
      size: { get_param: dataVolume}
      volume_type: "M1"

  # Create a system volume for use with the server
  demo-mgmt3-server-sys-vol:
    type: OS::Cinder::Volume
    properties:
      availability_zone: { get_param: azName}
      size: { get_param: osVolume}
      volume_type: "M1"
      image : { get_param: imageName }

  # Build a server using the system volume defined above
  demo-mgmt3-server:
    type: OS::Nova::Server
    depends_on: [ demostack_private_subnet ]
    properties:
      key_name: { get_param: kpName }
      image: { get_param: imageName }
      flavor: { get_param: flavorName }
      block_device_mapping: [{"volume_size": { get_param: osVolume}, "volume_id": {get_resource: demo-mgmt3-server-sys-vol}, "delete_on_termination": True, "device_name": "/dev/vda"}]
      admin_user: "ubuntu"
      security_groups: [{get_param: securityGroup}]
      metadata: { "fcx.autofailover": True, "Example Custom Tag": "Multiple Server Build" }
      user_data:
        str_replace:
          template: |
            #cloud-config
            write_files:
              - content: |
                  #!/bin/bash
                  voldata_id=%voldata_id%
                  voldata_dev="/dev/disk/by-id/virtio-$(echo ${voldata_id} | cut -c -20)"
                  mkfs.ext4 ${voldata_dev}
                  mkdir -pv /mnt/appdata
                  echo "${voldata_dev} /mnt/appdata ext4 defaults 1 2" >> /etc/fstab
                  mount /mnt/appdata
                  chmod 0777 /mnt/appdata
                path: /tmp/format-disks
                permissions: '0700'
            runcmd:
              - /tmp/format-disks
          params:
            "%voldata_id%": { get_resource: demo-mgmt3-server-data-vol }
      user_data_format: RAW
      networks: ["uuid": {get_resource: demostack_private_net} ]

  # Attach previously defined data-vol to the server
  attach-demo-mgmt3-server-data-vol:
    type: OS::Cinder::VolumeAttachment
    depends_on: [ demo-mgmt3-server-data-vol, demo-mgmt3-server ]
    properties:
      instance_uuid: {get_resource: demo-mgmt3-server}
      mountpoint: "/dev/vdb"
      volume_id: {get_resource: demo-mgmt3-server-data-vol}

outputs:
  server1_ip:
    description: fixed ip assigned to the server 1
    value: { get_attr: [demo-mgmt1-server, networks, "private", 0]}
  server2_ip:
    description: fixed ip assigned to the server 2
    value: { get_attr: [demo-mgmt2-server, networks, "private", 0]}
  server3_ip:
    description: fixed ip assigned to the server 3
    value: { get_attr: [demo-mgmt3-server, networks, "private", 0]}

...
"""
