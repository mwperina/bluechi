# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Generated file. DO NOT EDIT!
#

from __future__ import annotations

from typing import Callable, Tuple, Dict, List
from dasbus.typing import (
    Bool,
    Double,
    Str,
    Int,
    Byte,
    Int16,
    UInt16,
    Int32,
    UInt32,
    Int64,
    UInt64,
    ObjPath,
    Structure,
)

# File has been renamed to UnixFD in following PR included in v1.7
# https://github.com/rhinstaller/dasbus/pull/70
try:
    from dasbus.typing import File
except ImportError:
    from dasbus.typing import UnixFD

from dasbus.client.proxy import InterfaceProxy, ObjectProxy
from dasbus.connection import MessageBus, SystemMessageBus, SessionMessageBus

import gi

gi.require_version("GLib", "2.0")
from gi.repository.GLib import Variant  # noqa: E402


BC_DEFAULT_PORT = 842
BC_DEFAULT_HOST = "127.0.0.1"

BC_DBUS_INTERFACE = "org.eclipse.bluechi"
BC_OBJECT_PATH = "/org/eclipse/bluechi"
BC_AGENT_DBUS_INTERFACE = "org.eclipse.bluechi.Agent"


class ApiBase:
    def __init__(self, bus: MessageBus = None, use_systembus=True) -> None:
        self.use_systembus = use_systembus

        if bus is not None:
            self.bus = bus
        elif self.use_systembus:
            self.bus = SystemMessageBus()
        else:
            self.bus = SessionMessageBus()

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        raise Exception("Not implemented!")


class Monitor(ApiBase):
    """
    org.eclipse.bluechi.Monitor:
    @short_description: Public interface of BlueChi on the managing node providing monitoring functionality.

    This interface is only available if a monitor has been created before via the Manager interface.
    It provides methods to subscribe to changes in systemd units on managed nodes as well as signals for those changes.
    """

    def __init__(
        self, monitor_path: ObjPath, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.monitor_path = monitor_path
        self.monitor_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.monitor_proxy is None:
            self.monitor_proxy = self.bus.get_proxy(
                BC_DBUS_INTERFACE, self.monitor_path
            )

        return self.monitor_proxy

    def close(self) -> None:
        """
          Close:

        Close the monitor.
        """
        self.get_proxy().Close()

    def subscribe(self, node: str, unit: str) -> UInt32:
        """
            Subscribe:
          @node: The name of the node to subscribe to
          @unit: The name of the unit to subscribe to
          @id: The id of the created subscription.

          Subscribe to changes of a unit on a node. Both fields support a wildcard '*'. A wildcard in the node name will create the subscription for all nodes.
        If the unit name is a wildcard, then the subscription matches changes for all units on the node.
        """
        return self.get_proxy().Subscribe(
            node,
            unit,
        )

    def unsubscribe(self, id: UInt32) -> None:
        """
          Unsubscribe:
        @id: The id of the subscription to cancel

        Cancel the subscription by ID.
        """
        self.get_proxy().Unsubscribe(
            id,
        )

    def subscribe_list(self, node: str, units: List[str]) -> UInt32:
        """
            SubscribeList:
          @node: The name of the node to subscribe to
          @units: A list of unit names to subscribe to
          @id: The id of the created subscription

          Subscribe to changes of a list of units on a node. The node field supports a wildcard '*'. A wildcard in the node name will create the subscription
        for all nodes.
        """
        return self.get_proxy().SubscribeList(
            node,
            units,
        )

    def on_unit_properties_changed(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
                Structure,
            ],
            None,
        ],
    ) -> None:
        """
          UnitPropertiesChanged:
        @node: The node name this signal originated from
        @unit: The unit for which the properties changed
        @interface: The originating interface
        @props: The changed properties as key-value pair with the name of the property as key

        Whenever the properties change for any of the units that are currently subscribed to, this signal is emitted.
        """
        self.get_proxy().UnitPropertiesChanged.connect(callback)

    def on_unit_state_changed(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
                str,
                str,
            ],
            None,
        ],
    ) -> None:
        """
          UnitStateChanged:
        @node: The node name this signal originated from
        @unit: The unit for which the properties changed
        @active_state: The active state of the unit
        @sub_state: The sub state of the unit
        @reason: The reason for the state change, the value is either real or virtual

        Emitted when the active state (and substate) of a monitored unit changes.
        """
        self.get_proxy().UnitStateChanged.connect(callback)

    def on_unit_new(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
            ],
            None,
        ],
    ) -> None:
        """
            UnitNew:
          @node: The node name this signal originated from
          @unit: The unit for which the properties changed
          @reason: The reason for the state change, the value is either real or virtual

          Emitted when a new unit is loaded by systemd, for example when a service is started (reason=real), or if BlueChi learns of an already loaded unit
        (reason=virtual).
        """
        self.get_proxy().UnitNew.connect(callback)

    def on_unit_removed(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
            ],
            None,
        ],
    ) -> None:
        """
            UnitRemoved:
          @node: The node name this signal originated from
          @unit: The unit for which the properties changed
          @reason: The reason for the state change, the value is either real or virtual

          Emitted when a unit is unloaded by systemd (reason=real), or when the agent disconnects and we previously reported the unit as loaded
        (reason=virtual).
        """
        self.get_proxy().UnitRemoved.connect(callback)


class Metrics(ApiBase):
    """
    org.eclipse.bluechi.Metrics:
    @short_description: Public interface of BlueChi on the managing node providing signals for performance metrics.

    This interface is only available if the metrics have been enabled before via the Manager interface.
    """

    def __init__(
        self, metrics_path: ObjPath, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.metrics_path = metrics_path
        self.metrics_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.metrics_proxy is None:
            self.metrics_proxy = self.bus.get_proxy(
                BC_DBUS_INTERFACE, self.metrics_path
            )

        return self.metrics_proxy

    def on_start_unit_job_metrics(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
                UInt64,
                UInt64,
            ],
            None,
        ],
    ) -> None:
        """
          StartUnitJobMetrics:
        @node_name: The node name this metrics has been collected for
        @job_id: The id of the job linked to the collected metrics
        @unit: The unit name this metrics has been collected for
        @job_measured_time_micros: The measured time it took starting the unit on the node in microseconds
        @unit_start_prop_time_micros: The systemd time it took starting the unit on the node in microseconds

        Emitted when a start operation processed by BlueChi finishes and the collection of metrics has been enabled previously.
        """
        self.get_proxy().StartUnitJobMetrics.connect(callback)

    def on_agent_job_metrics(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
                UInt64,
            ],
            None,
        ],
    ) -> None:
        """
            AgentJobMetrics:
          @node_name: The node name this metrics has been collected for
          @unit: The unit name this metrics has been collected for
          @method: The lifecycle operation
          @systemd_job_time_micros: The systemd time it took starting the unit on the node in microseconds

          Emitted for all unit lifecycle operations (e.g. Start, Stop, Reload, etc.) processed by BlueChi when these finish and the collection of metrics has
        been enabled previously.
        """
        self.get_proxy().AgentJobMetrics.connect(callback)


class Job(ApiBase):
    """
    org.eclipse.bluechi.Job:
    @short_description: Public interface of BlueChi on the managing node for all job objects.

    This interface is used to either cancel a job, get its properties and monitor its state.
    """

    def __init__(
        self, job_path: ObjPath, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.job_path = job_path
        self.job_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.job_proxy is None:
            self.job_proxy = self.bus.get_proxy(BC_DBUS_INTERFACE, self.job_path)

        return self.job_proxy

    def cancel(self) -> None:
        """
          Cancel:

        Cancels the job.
        It cancels the corresponding systemd job if it was already started. Otherwise it cancels the BlueChi job.
        """
        self.get_proxy().Cancel()

    @property
    def id(self) -> UInt32:
        """
          Id:

        An integer giving the id of the job.
        """
        return self.get_proxy().Id

    @property
    def node(self) -> str:
        """
          Node:

        The name of the node the job is on.
        """
        return self.get_proxy().Node

    @property
    def unit(self) -> str:
        """
          Unit:

        The name of the unit the job works on.
        """
        return self.get_proxy().Unit

    @property
    def job_type(self) -> str:
        """
          JobType:

        Type of the job, either Start or Stop.
        """
        return self.get_proxy().JobType

    @property
    def state(self) -> str:
        """
          State:

        The current state of the job, one of: waiting (queued jobs) or running.
        On any change, a signal is emitted on the org.freedesktop.DBus.Properties interface.
        """
        return self.get_proxy().State


class Manager(ApiBase):
    """
    org.eclipse.bluechi.Manager:
    @short_description: Public interface of BlueChi on the managing node providing methods and signals for all nodes.

    This interface can be used to get information about all nodes and their units, create monitors and listen for job signals.
    """

    def __init__(self, bus: MessageBus = None, use_systembus=True) -> None:
        super().__init__(bus, use_systembus)

        self.manager_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.manager_proxy is None:
            self.manager_proxy = self.bus.get_proxy(BC_DBUS_INTERFACE, BC_OBJECT_PATH)

        return self.manager_proxy

    def list_units(
        self,
    ) -> List[Tuple[str, str, str, str, str, str, str, ObjPath, UInt32, str, ObjPath]]:
        """
          ListUnits:
        @units: A list of all units on each node:
          - The node name
          - The primary unit name as string
          - The human readable description string
          - The load state (i.e. whether the unit file has been loaded successfully)
          - The active state (i.e. whether the unit is currently started or not)
          - The sub state (a more fine-grained version of the active state that is specific to the unit type, which the active state is not)
          - A unit that is being followed in its state by this unit, if there is any, otherwise the empty string.
          - The unit object path
          - If there is a job queued for the job unit the numeric job id, 0 otherwise
          - The job type as string
          - The job object path

        List all loaded systemd units on all nodes which are online.
        """
        return self.get_proxy().ListUnits()

    def list_nodes(self) -> List[Tuple[str, ObjPath, str]]:
        """
          ListNodes:
        @nodes: A list of all nodes:
          - The node name
          - The object path of the node
          - the current state of that node, either online or offline

        List all nodes managed by BlueChi regardless if they are offline or online.
        """
        return self.get_proxy().ListNodes()

    def get_node(self, name: str) -> ObjPath:
        """
          GetNode:
        @name: Name of the node
        @path: The path of the requested node

        Get the object path of the named node.
        """
        return self.get_proxy().GetNode(
            name,
        )

    def create_monitor(self) -> ObjPath:
        """
          CreateMonitor:
        @monitor: The path of the created monitor.

        Create a new monitor on which subscriptions can be added. It will automatically be closed as soon as the connection is closed.
        """
        return self.get_proxy().CreateMonitor()

    def enable_metrics(self) -> None:
        """
          EnableMetrics:

        Enable collecting performance metrics.
        """
        self.get_proxy().EnableMetrics()

    def disable_metrics(self) -> None:
        """
          DisableMetrics:

        Disable collecting performance metrics.
        """
        self.get_proxy().DisableMetrics()

    def set_log_level(self, loglevel: str) -> None:
        """
          SetLogLevel:
        @loglevel: The new loglevel to use.

        Change the loglevel of the manager.
        """
        self.get_proxy().SetLogLevel(
            loglevel,
        )

    def on_job_new(
        self,
        callback: Callable[
            [
                UInt32,
                ObjPath,
            ],
            None,
        ],
    ) -> None:
        """
          JobNew:
        @id: The id of the new job
        @job: The path of the job

        Emitted each time a new BlueChi job is queued.
        """
        self.get_proxy().JobNew.connect(callback)

    def on_job_removed(
        self,
        callback: Callable[
            [
                UInt32,
                ObjPath,
                str,
                str,
                str,
            ],
            None,
        ],
    ) -> None:
        """
            JobRemoved:
          @id: The id of the new job
          @job: The path of the job
          @node: The name of the node the job has been completed on
          @unit: The name of the unit the job has been completed on
          @result: The result of the job

          Emitted each time a new job is dequeued or the underlying systemd job finished. result is one of: done, failed, cancelled, timeout, dependency,
        skipped. This is either the result from systemd on the node, or cancelled if the job was cancelled in BlueChi before any systemd job was started
        for it.
        """
        self.get_proxy().JobRemoved.connect(callback)

    def on_node_connection_state_changed(
        self,
        callback: Callable[
            [
                str,
                str,
            ],
            None,
        ],
    ) -> None:
        """ """
        self.get_proxy().NodeConnectionStateChanged.connect(callback)


class Node(ApiBase):
    """
    org.eclipse.bluechi.Node:
    @short_description: Public interface of BlueChi on the managing node providing methods, signals and  for a specific node.

    This interface can be used to get information about a specific node and its units as well as control them, e.g. by starting or stopping them.
    """

    def __init__(
        self, node_name: str, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.node_name = node_name
        self.node_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.node_proxy is None:
            manager = self.bus.get_proxy(BC_DBUS_INTERFACE, BC_OBJECT_PATH)

            node_path = manager.GetNode(self.node_name)
            self.node_proxy = self.bus.get_proxy(BC_DBUS_INTERFACE, node_path)

        return self.node_proxy

    def start_unit(self, name: str, mode: str) -> ObjPath:
        """
            StartUnit:
          @name: The name of the unit to start
          @mode: The mode used to start the unit
          @job: The path for the job associated with the start operation

          Queues a unit activate job for the named unit on this node. The queue is per-unit name, which means there is only ever one active job per unit. Mode
        can be one of replace or fail. If there is an outstanding queued (but not running) job, that is replaced if mode is replace, or the job
        fails if mode is fail.

          The job returned is an object path for an object implementing org.eclipse.bluechi.Job, and which be monitored for the progress of the job, or used
        to cancel the job. To track the result of the job, follow the JobRemoved signal on the Manager.
        """
        return self.get_proxy().StartUnit(
            name,
            mode,
        )

    def stop_unit(self, name: str, mode: str) -> ObjPath:
        """
          StopUnit:
        @name: The name of the unit to stop
        @mode: The mode used to stop the unit
        @job: The path for the job associated with the stop operation

        StopUnit() is similar to StartUnit() but stops the specified unit rather than starting it.
        """
        return self.get_proxy().StopUnit(
            name,
            mode,
        )

    def freeze_unit(self, name: str) -> None:
        """
            FreezeUnit:
          @name: The name of the unit to freeze

          Freezing the unit will cause all processes contained within the cgroup corresponding to the unit to be suspended. Being suspended means that unit's
        processes won't be scheduled to run on CPU until thawed.
        """
        self.get_proxy().FreezeUnit(
            name,
        )

    def thaw_unit(self, name: str) -> None:
        """
          ThawUnit:
        @name: The name of the unit to thaw

        This is the inverse operation to the freeze command and resumes the execution of processes in the unit's cgroup.
        """
        self.get_proxy().ThawUnit(
            name,
        )

    def reload_unit(self, name: str, mode: str) -> ObjPath:
        """
          ReloadUnit:
        @name: The name of the unit to reload
        @mode: The mode used to reload the unit
        @job: The path for the job associated with the reload operation

        ReloadUnit() is similar to StartUnit() but can be used to reload a unit instead. See equivalent systemd methods for details.
        """
        return self.get_proxy().ReloadUnit(
            name,
            mode,
        )

    def restart_unit(self, name: str, mode: str) -> ObjPath:
        """
          RestartUnit:
        @name: The name of the unit to restart
        @mode: The mode used to restart the unit
        @job: The path for the job associated with the restart operation

        RestartUnit() is similar to StartUnit() but can be used to restart a unit instead. See equivalent systemd methods for details.
        """
        return self.get_proxy().RestartUnit(
            name,
            mode,
        )

    def get_unit_properties(self, name: str, interface: str) -> Structure:
        """
          GetUnitProperties:
        @name: The name of unit
        @interface: The interface name
        @props: The  as key-value pair with the name of the property as key

        Returns the current  for a named unit on the node. The returned  are the same as you would get in the systemd  apis.
        """
        return self.get_proxy().GetUnitProperties(
            name,
            interface,
        )

    def get_unit_property(self, name: str, interface: str, property: str) -> Variant:
        """
          GetUnitProperty:
        @name: The name of unit
        @interface: The interface name
        @property: The property name
        @value: The value of the property

        Get one named property, otherwise similar to GetUnit.
        """
        return self.get_proxy().GetUnitProperty(
            name,
            interface,
            property,
        )

    def set_unit_properties(
        self, name: str, runtime: bool, keyvalues: List[Tuple[str, Variant]]
    ) -> None:
        """
          SetUnitProperties:
        @name: The name of the unit
        @runtime: Specify if the changes should persist after reboot or not
        @keyvalues: A list of the new values as key-value pair with the key being the name of the property

        Set named . If runtime is true the property changes do not persist across reboots.
        """
        self.get_proxy().SetUnitProperties(
            name,
            runtime,
            keyvalues,
        )

    def enable_unit_files(
        self, files: List[str], runtime: bool, force: bool
    ) -> Tuple[bool, List[Tuple[str, str, str]],]:
        """
          EnableUnitFiles:
        @files: A list of units to enable
        @runtime: Specify if the changes should persist after reboot or not
        @force: Specify if replacing the symlinks pointing to other units should be enforced
        @carries_install_info: True if the units contained enablement information
        @changes: The changes made
          - type of change (one of: symlink, unlink)
          - file name of the symlink
          - destination of the symlink

        EnableUnitFiles() may be used to enable one or more units in the system (by creating symlinks to them in /etc/ or /run/).
        """
        return self.get_proxy().EnableUnitFiles(
            files,
            runtime,
            force,
        )

    def disable_unit_files(
        self, files: List[str], runtime: bool
    ) -> List[Tuple[str, str, str]]:
        """
          DisableUnitFiles:
        @files: A list of units to enable
        @runtime: Specify if the changes should persist after reboot or not
        @changes: The changes made
          - type of change (one of: symlink, unlink)
          - file name of the symlink
          - destination of the symlink

        DisableUnitFiles() is similar to EnableUnitFiles() but disables the specified units by removing all symlinks to them in /etc/ and /run/
        """
        return self.get_proxy().DisableUnitFiles(
            files,
            runtime,
        )

    def list_units(
        self,
    ) -> List[Tuple[str, str, str, str, str, str, ObjPath, UInt32, str, ObjPath]]:
        """
          ListUnits:
        @units: A list of all units on the node:
          - The primary unit name as string
          - The human readable description string
          - The load state (i.e. whether the unit file has been loaded successfully)
          - The active state (i.e. whether the unit is currently started or not)
          - The sub state (a more fine-grained version of the active state that is specific to the unit type, which the active state is not)
          - A unit that is being followed in its state by this unit, if there is any, otherwise the empty string.
          - The unit object path
          - If there is a job queued for the job unit the numeric job id, 0 otherwise
          - The job type as string
          - The job object path

        List all loaded systemd units.
        """
        return self.get_proxy().ListUnits()

    def reload(self) -> None:
        """
          Reload:

        Reload() may be invoked to reload all unit files.
        """
        self.get_proxy().Reload()

    def set_log_level(self, level: str) -> None:
        """
          SetLogLevel:
        @loglevel: The new loglevel to use.

        Change the loglevel of the manager.
        """
        self.get_proxy().SetLogLevel(
            level,
        )

    @property
    def name(self) -> str:
        """
          Name:

        The name of the node.
        """
        return self.get_proxy().Name

    @property
    def status(self) -> str:
        """
          Status:

        The connection status of the node with the BlueChi controller.
        On any change, a signal is emitted on the org.freedesktop.DBus.Properties interface.
        """
        return self.get_proxy().Status

    @property
    def last_seen_timestamp(self) -> UInt64:
        """
          LastSeenTimestamp:

        A timestamp indicating when the last connection test (e.g. via heartbeat) was successful.
        """
        return self.get_proxy().LastSeenTimestamp


class Agent(ApiBase):
    """
    org.eclipse.bluechi.Agent:
    @short_description: Public interface of BlueChi on the managed node providing methods and signals for the respective node.

    This interface is used to create proxy services resolving dependencies on services of other managed nodes.
    """

    def __init__(self, bus: MessageBus = None, use_systembus=True) -> None:
        super().__init__(bus, use_systembus)

        self.agent_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.agent_proxy is None:
            self.agent_proxy = self.bus.get_proxy(
                BC_AGENT_DBUS_INTERFACE, BC_OBJECT_PATH
            )

        return self.agent_proxy

    def create_proxy(self, local_service_name: str, node: str, unit: str) -> None:
        """
          CreateProxy:
        @local_service_name: The service name which requests the external dependency
        @node: The requested node to provide the service
        @unit: The external unit requested from the local service

        BlueChi internal usage only.
        CreateProxy() creates a new proxy service. It is part in the chain of resolving dependencies on services running on other managed nodes.
        """
        self.get_proxy().CreateProxy(
            local_service_name,
            node,
            unit,
        )

    def remove_proxy(self, local_service_name: str, node: str, unit: str) -> None:
        """
          RemoveProxy:
        @local_service_name: The service name which requests the external dependency
        @node: The requested node to provide the service
        @unit: The external unit requested from the local service

        BlueChi internal usage only.
        RemoveProxy() removes a new proxy service. It is part in the chain of resolving dependencies on services running on other managed nodes.
        """
        self.get_proxy().RemoveProxy(
            local_service_name,
            node,
            unit,
        )
