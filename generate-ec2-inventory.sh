#!/bin/bash

echo "Generate EC2 inventory..."
#echo -e "VpcId InstanceId InstanceType ImageId, State.Name, LaunchTime, Placement.AvailabilityZone, Placement.Tenancy, PrivateIpAddress, PrivateDnsName, PublicDnsName, Name, SecurityGroupName, Role, Team, Environment' > instances.tsv
aws ec2 describe-instances \
    --region us-west-2 \
    --output text \
    --query 'Reservations[*].Instances[*].[VpcId, InstanceId, InstanceType, ImageId, State.Name, LaunchTime, Placement.AvailabilityZone, Placement.Tenancy, PrivateIpAddress, PrivateDnsName, PublicDnsName, [Tags[?Key==`Name`].Value] [0][0], [Tags[?Key==`Role`].Value] [0][0], [Tags[?Key==`Team`].Value] [0][0], [Tags[?Key==`Environment`].Value] [0][0] ]' \
    > instances.tsv