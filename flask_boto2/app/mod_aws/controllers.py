from flask import Flask
from flask import flash
from flask import abort
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import make_response
from flask import json
from flask import Response
from jinja2 import TemplateNotFound

from flask_login import login_required

import os
import sys
import config
import boto.ec2.elb
import boto

# Asynchronous tasks
from celery_worker.tasks import get_all_zones
from celery_worker.tasks import get_all_instance_status
from celery_worker.tasks import get_all_volumes
from celery_worker.tasks import get_all_addresses
from celery_worker.tasks import get_all_load_balancers
from celery_worker.tasks import get_only_instances
from celery_worker.tasks import connect_to_aws_region
from celery_worker.tasks import elb_connect_to_aws_region


from app import db
from app import app


route_base = '/'
mod_aws = Blueprint('aws', __name__, url_prefix='/aws')


@mod_aws.route('/aws')
@login_required
def aws():
    list = []

    for region in app.config['REGION_LIST']:
        conn = connect_to_aws_region(region)
        zones = get_all_zones(conn)
        instances = get_all_instance_status(conn)
        instance_count = len(instances)
        ebs = get_all_volumes(conn)
        ebscount = len(ebs)
        unattached_ebs = 0
        unattached_eli = 0
        event_count = 0
        for instance in instances:
            events = instance.events
            if events:
                event_count = event_count + 1

        for vol in ebs:
            state = vol.attachment_state()
            if state is None:
                unattached_ebs = unattached_ebs + 1

        elis = get_all_addresses(conn)
        eli_count = len(elis)

        for eli in elis:
            instance_id = eli.instance_id
            if not instance_id:
                unattached_eli = unattached_eli + 1

        connelb = elb_connect_to_aws_region(region)
        elb = get_all_load_balancers(connelb)
        elb_count = len(elb)
        list.append({
                    'region': region,
                    'zones': zones,
                    'instance_count': instance_count,
                    'ebscount': ebscount,
                    'unattached_ebs': unattached_ebs,
                    'eli_count': eli_count,
                    'unattached_eli': unattached_eli,
                    'elb_count': elb_count,
                    'event_count': event_count
                    })
    return render_template('aws/aws.html', list=list)


@app.route('/ebs/<region>/')
@login_required
def ebs_volumes(region=None):

    conn = connect_to_aws_region(region)
    ebs = get_all_volumes(conn)
    ebs_vol = []
    for vol in ebs:
        state = vol.attachment_state()
        if state is None:
            ebs_info = {'id': vol.id,
                        'size': vol.size,
                        'iops': vol.iops,
                        'status': vol.status
                        }
            ebs_vol.append(ebs_info)
    return render_template('aws/ebs.html', ebs_vol=ebs_vol, region=region)


@app.route('/ebs/<region>/delete/<vol_id>')
@login_required
def delete_ebs_vol(region=None, vol_id=None):

    conn = connect_to_aws_region(region)
    vol_id = vol_id.encode('ascii')
    vol_ids = get_all_volumes(conn, volume_ids=vol_id)
    for vol in vol_ids:
        vol.delete()
    return redirect(url_for('aws/ebs', region=region))


@app.route('/eips/<region>/')
@login_required
def elastic_ips(region=None):

    conn = connect_to_aws_region(region)
    elis = get_all_addresses(conn)
    un_eli = []
    for eli in elis:
        instance_id = eli.instance_id
        if not instance_id:
            eli_info = {'public_ip': eli.public_ip,
                        'domain': eli.domain
                        }
            un_eli.append(eli_info)
    return render_template('aws/eips.html', un_eli=un_eli, region=region)


@app.route('/elbs/<region>/')
@login_required
def elb_list(region=None):

    conn = elb_connect_to_aws_region(region)
    elbs = get_all_load_balancers(conn)
    elb_info = []
    for elb in elbs:
        if elb.name:
            info = {'name': elb.name}
            elb_info.append(info)
    return render_template('aws/elbs.html', region=region)


@app.route('/eips/<region>/delete/<ip>')
@login_required
def delete_elastic_ip(region=None, ip=None):

    conn = connect_to_aws_region(region)
    ip = ip.encode('ascii')
    elis = get_all_addresses(conn, addresses=ip)

    for eli in elis:
        eli.release()
    return redirect(url_for('eips', region=region))


@app.route('/instance_events/<region>/')
@login_required
def instance_events(region=None):

    conn = connect_to_aws_region(region)

    nodes = get_only_instances(conn)
    instance_node_list = []
    for node in nodes:
        if node:
            n_info = {'instance_id': node.id,
                      'private_ip_address': node.private_ip_address,
                      'vpc_id': node.vpc_id,
                      'instance_type': node.instance_type,
                      'state': node.state
                      }
            instance_node_list.append(n_info)

    instances = get_all_instance_status(conn)
    instance_event_list = []
    for instance in instances:
        if instance.events:
            event_info = {'instance_id': instance.id,
                          'event': instance.events[0].code,
                          'description': instance.events[0].description,
                          'event_before': instance.events[0].not_before,
                          'event_after': instance.events[0].not_after
                          }
            instance_event_list.append(event_info)

    return render_template('aws/instance_events.html',
                           instance_node_list=instance_node_list,
                           instance_event_list=instance_event_list)
