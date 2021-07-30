from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns,
    aws_logs as logs,
    core,
)
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationProtocol
from aws_cdk.aws_ecr_assets import DockerImageAsset


class CdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cpu = 1024
        mem = 2048
        count = 1

        vpc = ec2.Vpc(
            self,
            "NeuraInkVPC",
            max_azs=2,
        )

        cluster = ecs.Cluster(self, "NeuraInkCluster", vpc=vpc)

        cluster.add_default_cloud_map_namespace(name="service.local")

        backend_role = iam.Role(scope=self, id='cdk-backend-role',
                                assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
                                role_name='cdk-backend-role',
                                managed_policies=[
                                    iam.ManagedPolicy.from_aws_managed_policy_name('AmazonECS_FullAccess'),
                                    iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
                                ])

        backend_asset = DockerImageAsset(self,
                                         "backend",
                                         directory=".",
                                         file="Dockerfile")
        backend_task = ecs.FargateTaskDefinition(
            self,
            "backend-task",
            cpu=cpu,
            memory_limit_mib=mem,
            task_role=backend_role.without_policy_updates(),
        )

        backend_task.add_container(
            "backend",
            image=ecs.ContainerImage.from_docker_image_asset(backend_asset),
            essential=True,
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="BackendContainer",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
        ).add_port_mappings(
            ecs.PortMapping(container_port=8000, host_port=8000))

        backend_service = ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            id="backend-service",
            service_name="backend",
            cluster=cluster,
            cloud_map_options=ecs.CloudMapOptions(name="backend"),
            cpu=cpu,
            desired_count=count,
            task_definition=backend_task,
            memory_limit_mib=mem,
            listener_port=8000,
            public_load_balancer=False,
        )

        backend_service.service.connections.allow_from(ec2.Port.tcp(8000))

app = core.App()
ecs = CdkStack(app, "CdkStack")
app.synth()
