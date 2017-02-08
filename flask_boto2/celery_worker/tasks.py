from __future__ import absolute_import

from celery_worker.celery import app
from config import Config
from boto.ec2 import connect_to_region
from boto.ec2.elb import connect_to_region as elb_connect_to_region

CREDS = {'AWS_ACCESS_KEY_ID': Config.AWS_ACCESS_KEY_ID,
         'AWS_SECRET_ACCESS_KEY': Config.AWS_SECRET_ACCESS_KEY}


@app.task
def get_all_zones(conn):
    return conn.get_all_zones()


@app.task
def get_all_instance_status(conn):
    return conn.get_all_instance_status()


@app.task
def get_all_volumes(conn, volume_ids=None):
    if volume_ids is not None:
        return conn.get_all_volumes(volume_ids)
    else:
        return conn.get_all_volumes()


@app.task
def get_all_addresses(conn, addresses=None):
    if addresses is not None:
        return conn.get_all_addresses(addresses)
    else:
        return conn.get_all_addresses()


@app.task
def get_all_load_balancers(conn):
    return conn.get_all_load_balancers()


@app.task
def get_only_instances(conn):
    return conn.get_only_instances()


@app.task
def connect_to_aws_region(region):
    return connect_to_region(
        region,
        aws_access_key_id=CREDS['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=CREDS['AWS_SECRET_ACCESS_KEY']
    )


@app.task
def elb_connect_to_aws_region(region):
    return elb_connect_to_region(
        region,
        aws_access_key_id=CREDS['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=CREDS['AWS_SECRET_ACCESS_KEY']
    )
