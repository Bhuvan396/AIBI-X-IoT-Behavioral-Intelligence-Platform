"""
Intake Controller
=================
Global toggle to block/unblock telemetry intake from IoT devices.
When blocked, the /telemetry endpoint returns HTTP 403.
"""


class IntakeController:
    def __init__(self):
        self.blocked = False

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False

    def is_blocked(self) -> bool:
        return self.blocked


intake_controller = IntakeController()
