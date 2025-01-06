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

        # defining IAM role for EC2 instance
        private_web_service_role = iam.Role(
            self, "PrivateWebServiceEC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        private_web_service_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
        )

        # defining the private EC2 instance
        private_web_service_instance = ec2.Instance(
            self, "PrivateWebServiceInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=private_web_service_vpc,
            role=private_web_service_role,
            security_group=private_web_service_sg
        )

        # Adding VPC Endpoints for SSM for Private Web Service
        private_web_service_vpc.add_interface_endpoint(
            "SSMEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SSM
        )
        private_web_service_vpc.add_interface_endpoint(
            "SSMMessagesEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES
        )
        private_web_service_vpc.add_interface_endpoint(
            "EC2MessagesEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES
        )
