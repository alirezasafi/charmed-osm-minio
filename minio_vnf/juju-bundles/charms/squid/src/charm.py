#!/usr/bin/env python3
import sys
sys.path.append('lib')
import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus

logger = logging.getLogger(__name__)


class SquidTestCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.start, self._on_start)
        # self._stored.set_default(things=[])

    def _on_start(self, event):
        unit = self.model.unit
        unit.status = MaintenanceStatus("Applying pod spec")
        if not self.framework.model.unit.is_leader():
            return
        spec = self._make_pod_spec()
        self.framework.model.pod.set_spec(spec)
        unit.status = ActiveStatus("squid service is ready.")

    # def _on_config_changed(self, _):
    #     current = self.config["thing"]
    #     if current not in self._stored.things:
    #         logger.debug("found a new thing: %r", current)
    #         self._stored.things.append(current)

    def _make_pod_spec(self):
        config = self.framework.model.config
        ports = [
            {
                "name": "squid",
                "containerPort": config["port"],
                "protocol": "TCP"
            }
        ]
        spec = {
            "version": 3,
            "containers": [
                {
                    "name": "squid",
                    "image": config["image"],
                    "imagePullPolicy": "IfNotPresent",
                    "ports": ports
                }
            ]
        }
        return spec


if __name__ == "__main__":
    main(SquidTestCharm)
