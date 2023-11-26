from motoman_robotraconteur_driver.motoplus_rr_driver_feedback_client \
    import MotoPlusRRDriverFeedbackSyncClient
from motoman_robotraconteur_driver.motoplus_rr_driver_command_client \
    import MotoPlusRRDriverCommandClient
import asyncio
import time, pickle

robot_ip = '192.168.1.31'

async def _read_controller_info():
    c = MotoPlusRRDriverCommandClient()
    c.start(robot_ip)
    await c.wait_ready(10)
    controller_info = await c.get_controller_info() 
    return controller_info

def read_controller_info():
    controller_info = asyncio.run(_read_controller_info())
    return controller_info

controller_info = read_controller_info()
pickle.dump(controller_info, open('controller_info.pkl', 'wb'))

fb = MotoPlusRRDriverFeedbackSyncClient()
fb.start(robot_ip)

# Set the feedback timeout to desired time to wait for incoming packet
fb_timeout = 0.001

while True:
    res, fb_data = fb.try_receive_state_sync(controller_info, fb_timeout)
    if res:
        print(fb_data)
    time.sleep(0.004)

# ControllerState(version=256, time=1694022904.916, seqno=6234591, controller_flags=66, group_state=[GroupState(axes_count=6, group_flags=6, command_position=array([-0.42922152,  0.40734967,  0.05257171,  0.210082  , -0.7508247 ,
#        -0.5194298 ]), feedback_position=array([-0.42920851,  0.40735881,  0.05256076,  0.210082  , -0.7508247 ,
#        -0.5194298 ]), command_speed=array([0., 0., 0., 0., 0., 0.]), feedback_speed=array([ 0.        , -0.00113447,  0.        ,  0.        ,  0.        ,
#         0.        ]), torque=array([0., 0., 0., 0., 0., 0.])), GroupState(axes_count=6, group_flags=6, command_position=array([-0.3138029 ,  0.84990206, -0.22216951, -1.19479559, -1.44052438,
#         2.74517918]), feedback_position=array([-0.3138029 ,  0.8499289 , -0.22216951, -1.1947776 , -1.44050657,
#         2.74517918]), command_speed=array([0., 0., 0., 0., 0., 0.]), feedback_speed=array([0., 0., 0., 0., 0., 0.]), torque=array([0., 0., 0., 0., 0., 0.])), GroupState(axes_count=2, group_flags=2, command_position=array([1.57065000e-01, 2.52915577e+02]), feedback_position=array([1.57065000e-01, 2.52915577e+02]), command_speed=array([0., 0.]), feedback_speed=array([0., 0.]), torque=array([0., 0.]))], task_state=[TaskState(task_flags=0, queued_cmd_num=0, completed_cmd_num=0, current_buffer_num=0, current_buffer_seqno=0, last_completed_buffer_seqno=0), TaskState(task_flags=0, queued_cmd_num=0, completed_cmd_num=0, current_buffer_num=0, current_buffer_seqno=0, last_completed_buffer_seqno=0), TaskState(task_flags=0, queued_cmd_num=0, completed_cmd_num=0, current_buffer_num=0, current_buffer_seqno=0, last_completed_buffer_seqno=0)], motion_streaming_state=MotionStreamingState(streaming_flags=129, streaming_error=1), job_state=[JobState(job_flags=1, job_line_number=2, job_step=0), JobState(job_flags=0, job_line_number=0, job_step=0), JobState(job_flags=0, job_line_number=0, job_step=0)])
