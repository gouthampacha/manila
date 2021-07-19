# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import abc

from oslo_log import log
from webob import exc

from manila.api.openstack import wsgi
from manila import db
from manila import exception
from manila.i18n import _
from manila import share
from manila import share_group

LOG = log.getLogger(__name__)


class MetadataController(metaclass=abc.ABCMeta):
    """An abstract metadata controller resource."""

    # From db
    resource_get = {
        "share": "share_get",
        "share_instance": "share_instance_get",
        "share_instance_export_location": "share_export_location_get_by_uuid",
        "share_access_rule": "share_access_get",
        "snapshot_access_list": "share_snapshot_access_get",
        "share_snapshot": "share_snapshot_get",
        "share_snapshot_instance_export_location":
            "share_snapshot_export_locations_get",
        "share_group": "share_group_get",
        "share_group_snapshot": "share_group_snapshot_get",
        "security_service": "security_service_get",
        "share_network": "share_network_get",
        "share_network_subnet": "share_network_subnet_get"
    }

    resource_metadata_get = {
        "share": "share_metadata_get",
        "share_instance": "share_instance_metadata_get",
        "share_instance_export_location":
            "share_instance_EL_metadata_get",
        "share_access_rule": "share_access_metadata_get",
        "snapshot_access_list": "share_snapshot_access_rules_metadata_get",
        "share_snapshot": "share_snapshot_metadata_get",
        "share_snapshot_instance_export_location":
            "share_snapshot_instance_export_location",
        "share_group": "share_group_metadata_get",
        "share_group_snapshot": "share_group_snapshot_metadata_get",
        "security_service": "security_service_metadata_get",
        "share_network": "share_network_metadata_get",
        "share_network_subnet": "share_network_subnet_metadata_get",

    }

    resource_metadata_get_item = {
        "share": "share_metadata_get_item",
        "share_instance": "share_instance_metadata_get_item",
        "share_instance_export_location":
            "share_instance_EL_metadata_get_item",
        "share_access_rule": "share_access_metadata_get_item",
        "snapshot_access_list": "share_snapshot_access_rules_metadata_get_item",
        "share_snapshot": "share_snapshot_metadata_get_item",
        "share_snapshot_instance_export_location":
            "share_snapshot_instance_EL_metadata_get_item",
        "share_group": "share_group_metadata_get_item",
        "share_group_snapshot": "share_group_snapshot_metadata_get_item",
        "security_service": "security_service_metadata_get_item",
        "share_network": "share_network_metadata_get_item",
        "share_network_subnet": "share_network_subnet_metadata_get_item"
    }

    resource_metadata_update = {
        "share": "share_metadata_update",
        "share_instance": "share_instance_metadata_update",
        "share_instance_export_location":
            "share_instance_EL_metadata_update",
        "share_access_rule": "share_access_metadata_update",
        "snapshot_access_list": "share_snapshot_access_rules_metadata_update",
        "share_snapshot": "share_snapshot_metadata_update",
        "share_snapshot_instance_export_location":
            "share_snapshot_instance_EL_metadata_update",
        "share_group": "share_group_metadata_update",
        "share_group_snapshot": "share_group_snapshot_metadata_update",
        "security_service": "security_service_metadata_update",
        "share_network": "share_network_metadata_update",
        "share_network_subnet": "share_network_subnet_metadata_update",
    }

    resource_metadata_delete = {
        "share": "share_metadata_delete",
        "share_access_rule": "share_access_metadata_delete",
        "snapshot_access_list": "share_snapshot_access_rules_metadata_delete",
        "share_snapshot": "share_snapshot_metadata_delete",
        "export_location": "export_location_metadata_delete",
        "share_instance_export_location":
            "share_instance_EL_metadata_delete",
        "share_instance": "share_instance_metadata_delete",
        "share_snapshot_instance_export_location":
            "share_snapshot_instance_EL_metadata_delete",
        "share_group": "share_group_metadata_delete",
        "share_group_snapshot": "share_group_snapshot_metadata_delete",
        "security_service": "security_service_metadata_delete",
        "share_network": "share_network_metadata_delete",
        "share_network_subnet": "share_network_subnet_metadata_delete"
    }

    def __init__(self):
        super(MetadataController, self).__init__()
        self.resource_name = None

    def _check_metadata_properties(self, metadata=None):
        if not metadata:
            metadata = {}

        for k, v in metadata.items():
            if not k:
                msg = _("Metadata property key is blank.")
                LOG.warning(msg)
                raise exception.InvalidMetadata(message=msg)
            if len(k) > 255:
                msg = _("Metadata property key is "
                        "greater than 255 characters.")
                LOG.warning(msg)
                raise exception.InvalidMetadata(message=msg)
            if not v:
                msg = _("Metadata property value is blank.")
                LOG.warning(msg)
                raise exception.InvalidMetadata(message=msg)
            if len(v) > 1023:
                msg = _("Metadata property value is "
                        "greater than 1023 characters.")
                LOG.warning(msg)
                raise exception.InvalidMetadata(message=msg)

    def _get_resource(self, context, resource_id):
        try:
            get_res_method = getattr(
                db, self.resource_get[self.resource_name])
            res = get_res_method(context, resource_id)

        except exception.NotFound as e:
            raise exc.HTTPNotFound(e.message)
        return res

    def _get_metadata(self, context, resource_id):

        self._get_resource(context, resource_id)
        get_metadata_method = getattr(
            db, self.resource_metadata_get[self.resource_name])

        result = get_metadata_method(context, resource_id)

        return result

    @wsgi.response(200)
    def _index_metadata(self, req, resource_id):
        context = req.environ['manila.context']
        metadata = self._get_metadata(context, resource_id)

        return {'metadata': metadata}

    @wsgi.response(200)
    def _create_metadata(self, req, resource_id, body):
        """Returns the new metadata item created."""

        context = req.environ['manila.context']
        try:
            metadata = body['metadata']
        except (KeyError, TypeError):
            msg = _("Malformed request body")
            raise exc.HTTPBadRequest(explanation=msg)

        self._check_metadata_properties(metadata)
        self._get_metadata(context, resource_id)

        create_metadata_method = getattr(
            db, self.resource_metadata_update[self.resource_name])
        result = create_metadata_method(context, resource_id)

        return {'metadata': result}

    @wsgi.response(200)
    def _update_metadata(self, req, resource_id, body):
        """Returns the updated metadata items."""

        context = req.environ['manila.context']
        try:
            metadata = body['metadata']
        except (TypeError, KeyError):
            expl = _('Malformed request body')
            raise exc.HTTPBadRequest(explanation=expl)

        self._check_metadata_properties(metadata)
        self._get_metadata(context, resource_id)

        update_metadata_method = getattr(
            db, self.resource_metadata_update[self.resource_name])
        result = update_metadata_method(context, resource_id, metadata)

        return {'metadata': result}

    def _update_metadata_item(self, req, resource_id, body):
        """Updates the specified metadata item."""

        context = req.environ['manila.context']
        try:
            meta_item = body['metadata']
        except (TypeError, KeyError):
            expl = _('Malformed request body')
            raise exc.HTTPBadRequest(explanation=expl)

        self._check_metadata_properties(meta_item)
        if len(meta_item) > 1:
            expl = _('Request body contains too many items')
            raise exc.HTTPBadRequest(explanation=expl)
        self._get_metadata(context, resource_id)

        update_metadata_method = getattr(
            db, self.resource_metadata_update[self.resource_name])
        result = update_metadata_method(context, resource_id, meta_item)

        return {'metadata': result}

    @wsgi.response(200)
    def _update_all_metadata(self, req, resource_id, body):
        """Deletes existing metadata, and returns the updated metadata."""

        context = req.environ['manila.context']
        try:
            metadata = body['metadata']
        except (TypeError, KeyError):
            expl = _('Malformed request body')
            raise exc.HTTPBadRequest(explanation=expl)

        self._check_metadata_properties(metadata)
        metaref = self._get_metadata(context, resource_id)

        for key in metaref:
            delete_metadata_method = getattr(
                db, self.resource_metadata_delete[self.resource_name])
            delete_metadata_method(context, resource_id, key)

        update_metadata_method = getattr(
            db, self.resource_metadata_update[self.resource_name])
        new_metadata = update_metadata_method(context, resource_id, metadata)
        return {'metadata': new_metadata}

    @wsgi.response(200)
    def _show_metadata(self, req, resource_id, key):
        """Return metadata item."""

        context = req.environ['manila.context']

        get_metadata_item_method = getattr(
            db, self.resource_metadata_get_item[self.resource_name])
        item = get_metadata_item_method(context, resource_id, key)

        return {'metadata': {key: item}}

    @wsgi.response(200)
    def _delete_metadata(self, req, resource_id, key):
        """Deletes existing metadata item."""

        context = req.environ['manila.context']
        self._get_metadata(context, resource_id)

        delete_metadata_method = getattr(
            db, self.resource_metadata_delete[self.resource_name])
        delete_metadata_method(context, resource_id, key)


def create_resource():
    return wsgi.Resource(MetadataController())
