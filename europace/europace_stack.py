from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct


class EuropaceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # defining the VPC
        private_web_service_vpc = ec2.Vpc(
            self, "PrivateWebServiceVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateWebServiceSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        # defining Security Group for Private Web Service
        private_web_service_sg = ec2.SecurityGroup(
            self, "PrivateWebServiceSecurityGroup",
            vpc=private_web_service_vpc,
            description="Allow internal access only for Private Web Service",
            allow_all_outbound=True
        )

        # adding Inbound Rule to Allow Internal VPC Traffic
        private_web_service_sg.add_ingress_rule(
            # Allow traffic from within the VPC CIDR range
            peer=ec2.Peer.ipv4("10.0.0.0/16"),
            connection=ec2.Port.tcp(80),       # Allow HTTP traffic on port 80
            description="Allow HTTP traffic from within the VPC"
        )
