import time, pickle
import base64
import numpy as np
from typing import NamedTuple, List, Tuple

class ControllerInfo(NamedTuple):
    version: Tuple = None
    control_group_count: int = 0
    interpolation_period: int = 0
    control_groups: List = []

class ControlGroupInfo(NamedTuple):
    group_number: int = 0
    group_id: int = 0
    axes_count: int = 0
    joint_type: np.array = None
    pulse_to_radians: np.array = None
    pulse_to_meters: np.array = None
    joint_limits_low: np.array = None
    joint_limits_high: np.array = None
    joint_angular_velocity: np.array = None
    max_increment: np.array = None
    dh_parameters: np.array = None

class ControllerState(NamedTuple):
    version: int
    time: float
    seqno: int
    controller_flags: int
    group_state: List
    task_state: List
    motion_streaming_state: "MotionStreamingState"


s='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'
controller_info=pickle.loads(base64.b64decode(s))

# file = open('controller_info.pkl', 'rb')
# print(file)
# controller_info = pickle.load(file)
# print(type(controller_info))
# # print(controller_info.control_group_count)
# # print(controller_info.interpolation_period)


# control_group1=
# control_group2=
# control_group3=
# print(controller_info.control_groups[0])