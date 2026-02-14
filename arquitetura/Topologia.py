from diagrams import Diagram, Cluster
from diagrams.aws.network import VPC, InternetGateway, RouteTable, ELB
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.general import User

with Diagram(
    "Arquitetura AWS - Aplicação Web",
    show=True,
    direction="LR"
):

    user = User("Usuário")

    with Cluster("AWS Cloud"):
        with Cluster("VPC 10.0.0.0/24"):

            igw = InternetGateway("Internet Gateway")
            route_public = RouteTable("Route Table - Public")
            route_private = RouteTable("Route Table - Private")

            alb = ELB("Application Load Balancer")

            with Cluster("Availability Zone 1"):

                with Cluster("Public Subnet 10.0.0.0/25"):
                    
                    with Cluster("Security Group - Frontend"):
                        ec2_front = EC2("Frontend")
                        ec2_front_res = EC2("Frontend (Reserva)")

                with Cluster("Private Subnet 10.0.0.128/26"):
                    
                    with Cluster("Security Group - Backend"):
                        ec2_backend = EC2("Backend")
                        ec2_db = EC2("Banco de Dados")

            with Cluster("Data Processing Layer"):
                s3_raw = S3("S3 - Raw")
                lambda_process = Lambda("Lambda - Tratamento")
                s3_trusted = S3("S3 - Trusted")
                lambda_send = Lambda("Lambda - Envio")

                s3_raw >> lambda_process >> s3_trusted >> lambda_send


    user >> igw >> route_public >> alb
    alb >> ec2_front
    alb >> ec2_front_res

    ec2_front >> route_private >> ec2_backend
    ec2_backend >> ec2_db

    ec2_backend >> s3_raw
