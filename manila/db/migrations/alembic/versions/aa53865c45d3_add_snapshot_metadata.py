# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""add_snapshot_metadata

Revision ID: aa53865c45d3
Revises: fbdfabcba377
Create Date: 2021-07-19 15:22:25.274494

"""

# revision identifiers, used by Alembic.
revision = 'aa53865c45d3'
down_revision = 'fbdfabcba377'

from alembic import op
from manila.db.migrations import utils
from oslo_log import log
import sqlalchemy as sql

LOG = log.getLogger(__name__)

# Existing Tables
# share_metadata_table_name = 'share_metadata'
# share_access_rules_metadata_table_name = 'share_access_rules_metadata'
# share_instance_export_locations_metadata_table_name = (
#     'share_instance_export_locations_metadata')

# New Tables
share_instance_metadata_table_name = 'share_instance_metadata'
share_snapshot_metadata_table_name = 'share_snapshot_metadata'
share_snapshot_instance_export_locations_metadata_table_name = (
    'share_snapshot_instance_export_locations_metadata')
share_snapshot_access_rules_metadata_table_name = (
    'share_snapshot_access_rules_metadata')
share_group_metadata_table_name = 'share_group_metadata'
share_group_snapshots_metadata_table_name = 'share_group_snapshots_metadata'
security_service_metadata_table_name = 'security_service_metadata'
share_networks_metadata_table_name = 'share_networks_metadata'
share_network_subnets_metadata_table_name = 'share_network_subnets_metadata'


def upgrade():
    connection = op.get_bind()
    try:
        op.create_table(
            share_snapshot_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column('share_snapshot_id', sql.String(36),
                       sql.ForeignKey('share_snapshots.id'), nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_snapshot_metadata_table_name)
        raise

    try:
        op.create_table(
            share_snapshot_instance_export_locations_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column(
                'share_snapshot_instance_export_locations_id',
                sql.String(36), sql.ForeignKey(
                    'share_snapshot_instance_export_locations.id'),
                nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_snapshot_instance_export_locations_metadata_table_name)
        raise

    try:
        op.create_table(
            share_instance_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column('share_instance_id', sql.String(36), sql.ForeignKey(
                'share_instances.id'), nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_instance_metadata_table_name)
        raise

    try:
        op.create_table(
            share_snapshot_access_rules_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column(
                'access_id', sql.String(36), sql.ForeignKey(
                    'share_snapshot_access_map.id'),
                nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_snapshot_access_rules_metadata_table_name)
        raise

    try:
        op.create_table(
            share_group_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column(
                'share_group_id',
                sql.String(36), sql.ForeignKey(
                    'share_groups.id'), nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_group_metadata_table_name)
        raise

    try:
        op.create_table(
            share_group_snapshots_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column(
                'share_group_snapshot_id', sql.String(36),
                sql.ForeignKey(
                    'share_group_snapshots.id'), nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_group_snapshots_metadata_table_name)
        raise

    try:
        op.create_table(
            security_service_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column(
                'security_service_id', sql.String(36),
                sql.ForeignKey('security_services.id'), nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  security_service_metadata_table_name)
        raise

    try:
        op.create_table(
            share_networks_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column(
                'share_network_id', sql.String(36),
                sql.ForeignKey('share_networks.id'), nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_networks_metadata_table_name)
        raise

    try:
        op.create_table(
            share_network_subnets_metadata_table_name,
            sql.Column('created_at', sql.DateTime),
            sql.Column('updated_at', sql.DateTime),
            sql.Column('deleted_at', sql.DateTime),
            sql.Column('deleted', sql.Integer, default=0),
            sql.Column(
                'share_network_subnets_id', sql.String(36),
                sql.ForeignKey('share_network_subnets.id'), nullable=False),
            sql.Column('key', sql.String(255), nullable=False),
            sql.Column('value', sql.String(1023), nullable=False),
            sql.Column('id', sql.Integer, primary_key=True, nullable=False),
            sql.Column('user_modifiable', sql.Boolean, default=True,
                       nullable=False),
            mysql_engine='InnoDB',
            mysql_charset='utf8'
        )
    except Exception:
        LOG.error("Table |%s| not created!",
                  share_network_subnets_metadata_table_name)
        raise

    try:
        user_modifiable = sql.Column(
            'user_modifiable', sql.Boolean, default=True, nullable=False)

        op.add_column(
            'share_instance_export_locations_metadata', user_modifiable)

        share_instance_export_locations_metadata_table_name = utils.load_table(
            'share_instance_export_locations_metadata', connection)
        op.execute(
            share_instance_export_locations_metadata_table_name.update(
                ).values({'user_modifiable': True}))

    except Exception:
        LOG.error("Column user_modifiable not created on |%s|!",
                  share_instance_export_locations_metadata_table_name)
        raise

    try:
        user_modifiable = sql.Column(
            'user_modifiable', sql.Boolean, default=True, nullable=False)

        op.add_column('share_access_rules_metadata', user_modifiable)

        share_access_rules_metadata_table_name = utils.load_table(
            'share_access_rules_metadata', connection)
        op.execute(
            share_access_rules_metadata_table_name.update().values({
                'user_modifiable': True,
            }))

    except Exception:
        LOG.error("Column user_modifiable not created on |%s|!",
                  share_access_rules_metadata_table_name)
        raise

    try:
        user_modifiable = sql.Column(
            'user_modifiable', sql.Boolean, default=True, nullable=False)

        op.add_column('share_metadata', user_modifiable)

        share_metadata_table_name = utils.load_table(
            'share_metadata', connection)
        op.execute(
            share_metadata_table_name.update().values({
                'user_modifiable': True,
            }))

    except Exception:
        LOG.error("Column user_modifiable not created on |%s|!",
                  share_metadata_table_name)
        raise


def downgrade():

    try:
        op.drop_column(
            'share_metadata', 'user_modifiable')
    except Exception:
        LOG.error(
            "Column user_modifiable not dropped from %s",
            'share_metadata')
        raise

    try:
        op.drop_column(
            'share_access_rules_metadata', 'user_modifiable')
    except Exception:
        LOG.error(
            "Column user_modifiable not dropped from %s",
            'share_access_rules_metadata')
        raise

    try:
        op.drop_column(
            'share_instance_export_locations_metadata',
            'user_modifiable')
    except Exception:
        LOG.error(
            "Column user_modifiable not dropped from %s",
            'share_instance_export_locations_metadata')
        raise

    try:
        op.drop_table(
            share_network_subnets_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            share_network_subnets_metadata_table_name)
        raise

    try:
        op.drop_table(
            share_networks_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            share_networks_metadata_table_name)
        raise

    try:
        op.drop_table(
            security_service_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            security_service_metadata_table_name)
        raise

    try:
        op.drop_table(
            share_group_snapshots_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            share_group_snapshots_metadata_table_name)
        raise

    try:
        op.drop_table(
            share_group_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            share_group_metadata_table_name)
        raise

    try:
        op.drop_table(share_snapshot_access_rules_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            share_snapshot_access_rules_metadata_table_name)
        raise

    try:
        op.drop_table(share_instance_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            share_instance_metadata_table_name)
        raise

    try:
        op.drop_table(
            share_snapshot_instance_export_locations_metadata_table_name)
    except Exception:
        LOG.error(
            "%s table not dropped",
            share_snapshot_instance_export_locations_metadata_table_name)
        raise

    try:
        op.drop_table(share_snapshot_metadata_table_name)
    except Exception:
        LOG.error("%s table not dropped", share_snapshot_metadata_table_name)
        raise
