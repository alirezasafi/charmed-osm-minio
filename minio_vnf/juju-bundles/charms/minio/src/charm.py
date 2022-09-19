#!/usr/bin/env python3
import sys
sys.path.append('lib')
import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus

logger = logging.getLogger(__name__)


class MinioCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.start, self._on_start)
        # self._stored.set_default(things=[])

    def _make_pod_spec(self):
        config = self.framework.model.config
        ports = [
            {
                "name": "minio",
                "containerPort": config["main-port"]
            },
            {
                "name": "minio-console",
                "containerPort": config["console-port"]
            }
        ]
        env_config = {
            "MINIO_ROOT_USER": config["root-user"],
            "MINIO_ROOT_PASSWORD": config["root-pass"],
            "MINIO_ACCESS_KEY": config["access-key"],
            "MINIO_SECRET_KEY": config["secret-key"],
            "HTTP_PROXY": "http://squid:3128",
            "HTTPS_PROXY": "http://squid:3128"
        }
        volume_config = [
            {
                "name": "minio-volume",
                "mountPath": "/opt/bitnami/minio-client/minio-volume",
                "hostPath": {
                    "path": "/home/ubuntu/docker/minio-volume",
                    "type": "DirectoryOrCreate"
                }
            }
        ]
        spec = {
            "version": 3,
            "containers": [
                {
                    "name": "minio",
                    "image": config["image"],
                    "imagePullPolicy": "IfNotPresent",
                    "ports": ports,
                    "envConfig": env_config,
                    "volumeConfig": volume_config
                }
            ]
        }
        return spec

    def _on_start(self, event):
        unit = self.model.unit
        unit.status = MaintenanceStatus("Applying pod spec")
        if not self.framework.model.unit.is_leader():
            return
        spec = self._make_pod_spec()
        self.framework.model.pod.set_spec(spec)
        unit.status = ActiveStatus("service is ready.")

    # def _on_config_changed(self, _):
    #     current = self.config["thing"]
    #     if current not in self._stored.things:
    #         logger.debug("found a new thing: %r", current)
    #         self._stored.things.append(current)


if __name__ == "__main__":
    main(MinioCharm)
