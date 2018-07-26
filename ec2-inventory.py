#!/usr/bin/env python

import click
import boto3
import pprint
import csv
from botocore.exceptions import ClientError


@click.command()
@click.option('--region', default='us-west-2', help='AWS Region to query')
def main(region):
    ec = boto3.client('ec2', region_name=region)

    try:
        report_data = []
        report_data.append(
            ['VpcId', 'Team', 'InstanceId', 'InstanceName', 'Role', 'PrivateIpAddress', 'State', 'Placement', 'SecurityGroups', 'All Ingress Rules', 'All Egress Rules'])

        reservations = ec.describe_instances(
            Filters=[
            ]
        ).get(
            'Reservations', []
        )

        instances = sum(
            [
                [i for i in r['Instances']]
                for r in reservations
            ], [])
        # getting all SGs names of EC2 instances
        ec2_sgs_names = {}
        for i in instances:
            if 'VpcId' not in i:
                break
            if i['VpcId'] not in ec2_sgs_names:
                ec2_sgs_names[i['VpcId']] = []
            else:
                for sg in i['SecurityGroups']:
                    if sg['GroupName'] not in ec2_sgs_names[i['VpcId']]:
                        ec2_sgs_names[i['VpcId']].append(sg['GroupName'])

        # Getting all SGs
        sgs = ec.describe_security_groups()

        # Get all security groups names
        sgs_names = {}
        unused_sgs = {}

        for i in sgs['SecurityGroups']:
            if 'VpcId' not in i:
                break
            if i['VpcId'] not in sgs_names:
                sgs_names[i['VpcId']] = []
            else:
                sgs_names[i['VpcId']].append(i['GroupName'])
                each_ec2_sgs = []
                if i['VpcId'] in ec2_sgs_names:
                    if i['GroupName'] not in ec2_sgs_names[i['VpcId']]:
                        if i['VpcId'] not in unused_sgs:
                            unused_sgs[i['VpcId']] = []
                        else:
                            unused_sgs[i['VpcId']].append(i['GroupName'])

        # Get security groups rules for each EC2
        for vpc_id in ec2_sgs_names:
            for i in instances:
                if 'VpcId' not in i:
                    break
                if i['VpcId'] == vpc_id:
                    ec2_sg_str = ""
                    all_ingress = ""
                    all_egress = ""
                    for ec2_sg in i['SecurityGroups']:
                        # loop through each one in sgs_names
                        for sg in sgs['SecurityGroups']:
                            if sg['VpcId'] == vpc_id and sg['GroupId'] == ec2_sg['GroupId']:
                                ec2_sg_str += "=========================\nGroupName: {}\nDescription: {}\nGroupId: {}\n".format(
                                    sg['GroupName'], sg['Description'], sg['GroupId'])
                                for key in ['IpPermissions', 'IpPermissionsEgress']:
                                    if key == 'IpPermissions':
                                        ec2_sg_str += "Ingress:\n"
                                    else:
                                        ec2_sg_str += "Egress:\n"
                                    for rule in sg[key]:
                                        if rule['IpProtocol'] == '-1':
                                            rules_str = "\tProtocol: all\n"
                                        else:
                                            rules_str = "\tProtocol: {}\n".format(
                                                rule['IpProtocol'])
                                        # Get ports
                                        if 'FromPort' in rule:
                                            rules_str += "\t  PortRange: {}-{}\n".format(
                                                rule['FromPort'], rule['ToPort'])

                                        # Get CIDRs
                                        cidrs = [cidr['CidrIp']
                                                 for cidr in rule['IpRanges']]
                                        if len(cidrs) > 0:
                                            rules_str += "\t  CIDRs: {}\n".format(
                                                ','.join(cidrs))

                                        # Get source SGs
                                        source_sgs = []
                                        if 'UserIdGroupPairs' in rule:
                                            if len(rule['UserIdGroupPairs']) > 0:
                                                rules_str += "\t  SourceSecurityGroups:\n"
                                                for source_sg in rule['UserIdGroupPairs']:
                                                    fields = [
                                                        f for f in source_sg]
                                                    fields.sort()
                                                    dash = '- '
                                                    for field in fields:
                                                        rules_str += "\t  {}{}: {}\n".format(
                                                            dash, field, source_sg[field])
                                                        dash = '  '

                                        ec2_sg_str += rules_str
                                        if key == 'IpPermissions':
                                            all_ingress += rules_str
                                        else:
                                            all_egress += rules_str

                                ec2_sg_str += "\n"

                    # print rules_str
                    instance_name = ""
                    team_name = ""
                    instance_role = ""
                    if 'Tags' in i:
                        for tag in i['Tags']:
                            if tag['Key'] == 'Name':
                                instance_name = tag['Value']
                            elif tag['Key'] == 'Team':
                                team_name = tag['Value']
                            elif tag['Key'] == 'Role':
                                instance_role = tag['Value']
                    report_data.append(
                        [vpc_id, team_name, i['InstanceId'], instance_name, instance_role, i['PrivateIpAddress'], i['State']['Name'], i['Placement']['AvailabilityZone'], ec2_sg_str, all_ingress, all_egress])

        # pprint.pprint(report_data)
        # pprint.pprint(unused_sgs)
        with open("security-groups.csv", 'wb') as resultFile:
            wr = csv.writer(resultFile, dialect='excel')
            wr.writerows(report_data)

        unused_sgs_report = []
        unused_sgs_report.append(
            ['VpcId', 'GroupName', 'GroupId', 'Description', 'Rules'])
        for vpc_id in unused_sgs:
            for sg_name in unused_sgs[vpc_id]:
                for sg in sgs['SecurityGroups']:
                    if sg['VpcId'] == vpc_id and sg['GroupName'] == sg_name:
                        rules_str = ""
                        for key in ['IpPermissions', 'IpPermissionsEgress']:
                            if key == 'IpPermissions':
                                rules_str += "Ingress:\n"
                            else:
                                rules_str += "Egress:\n"
                            for rule in sg[key]:
                                if rule['IpProtocol'] == '-1':
                                    rules_str += "\tProtocol: all\n"
                                else:
                                    rules_str += "\tProtocol: {}\n".format(
                                        rule['IpProtocol'])
                                # Get ports
                                if 'FromPort' in rule:
                                    rules_str += "\t  PortRange: {}-{}\n".format(
                                        rule['FromPort'], rule['ToPort'])

                                # Get CIDRs
                                cidrs = [cidr['CidrIp']
                                         for cidr in rule['IpRanges']]
                                if len(cidrs) > 0:
                                    rules_str += "\t  CIDRs: {}\n".format(
                                        ','.join(cidrs))

                                # Get source SGs
                                source_sgs = []
                                if 'UserIdGroupPairs' in rule:
                                    if len(rule['UserIdGroupPairs']) > 0:
                                        rules_str += "\t  SourceSecurityGroups:\n"
                                        for source_sg in rule['UserIdGroupPairs']:
                                            fields = [f for f in source_sg]
                                            fields.sort()
                                            dash = '- '
                                            for field in fields:
                                                rules_str += "\t  {}{}: {}\n".format(
                                                    dash, field, source_sg[field])
                                                dash = '  '

                        unused_sgs_report.append(
                            [vpc_id, sg['GroupName'], sg['GroupId'], sg['Description'], rules_str])

        with open("unused-security-groups.csv", 'wb') as resultFile:
            wr = csv.writer(resultFile, dialect='excel')
            wr.writerows(unused_sgs_report)

    except ClientError as e:
        print(e)


if __name__ == '__main__':
    main()
