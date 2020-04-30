import boto3
import botocore
import click

## botocore is for exception handling

session = boto3.Session(profile_name = 'admin')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':["project"]}]
        instances = ec2.instances.filter(Filters = filters)
    else:
        instances = ec2.instances.all()

    return instances

## Next groups for volumes and Instances

@click.group()
def cli():
    """ Manage snapshots """

## Add a group of commands for snapshots

@cli.group('snapshots')
def snapshots():
    """ Commands for snapshots """

@snapshots.command('list')
@click.option('--project', default = None,
    help="Only snapshots for project (tag project:<name>)")

def list_snapshots(project):

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print( ', '.join((
                    s.id,
                    s.volume_id,
                    str(s.volume_size) + "GiB",
                    s.snapshot_id,
                    s.state
                )))

                if s.state == 'completed':break
    return
## Add a group for commands for volumes and give it a Name

@cli.group('volumes')
def volumes():
    """ commands for volumes """

@volumes.command('list')
@click.option('--project', default=None,
     help="Only volumes for project (tag project:<name>)")

def list_volumes(project):
    "List Volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
                )))

        return

## Add a group for commands for volumes and give it a Name

@cli.group('instances')
def instances():
    """ commands for instances """

@instances.command('snapshot',
        help="Create snapshots for all volumes")
@click.option('--project', default=None,
     help="Only instances for project (tag project:<name>)")

def create_snapshots(project):
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            i.stop()
            i.wait_until_stopped()
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by shotty")
            print("Starting...{0}".format(i.id))
            i.start()
            i.wait_until_running()
    return


@instances.command('list')
@click.option('--project', default=None,
     help="Only instances for project (tag project:<name>)")

def list_instances(project):
    "List attributes of EC2 instances"

    instances = filter_instances(project)

    if project:
        filters = [{'Name':'tag:Project', 'Values':["project"]}]
        instances = ec2.instances.filter(Filters = filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Project', '<no project')
        )))
    return

@instances.command('start')
@click.option('--project', default = None,
    help="Only instances for project (tag project:<name>)")

def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:      ##handle error when start comand us issued on a
                                                          ## stopping instance
            print("Could not start {0} ".format(i.id) + str(e))
            continue

    return

@instances.command('stop')
@click.option('--project', default = None,
    help="Only instances for project (tag project:<name>)")

def stop_instance(project):# XXX: # XXX:
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:      ##handle error when start comand us issued on a
                                                          ## stopping instance
            print("Could not stop {0} ".format(i.id) + str(e))
            continue
    return

@instances.command('terminate')
@click.option('--project', default = None,
    help="Only instances for project (tag project:<name>)")

def terminate_instance(project):
    "Terminate EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Terminating {} ....".format(i.id))
        i.terminate()
    return

if __name__ == '__main__':
    cli()
