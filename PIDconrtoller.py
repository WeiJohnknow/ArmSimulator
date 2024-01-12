import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

"""
kp:與當前誤差有關, 值越大，穩態誤差越小，響應越快，但有可能造成系統震盪與不穩定。
ki:與過去誤差的累積有關，可用於消除長期的穩態誤差，但可能造成震盪，且對雜訊敏感度回提升。
kd:與未來誤差趨勢有關，用於抑制系統反應，可防震盪，提高穩定性，但調高可能會造成系統對雜訊敏感度提升
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0

    def update(self, current_value):
        error = self.setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error

        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        self.prev_error = error
        return output

# Example usage
pid = PIDController(kp=0.1, ki=0.01, kd=0.05, setpoint=50.0)
pid_ = PIDController(kp=0.5, ki=0.05, kd=0.005, setpoint=50.0)

# 現在位置
NowPos = 0.0
NowPos_ = 0.0

# 系統迭代次數
iter = 100

# Data buffer
posBuffer = np.zeros((iter))
posBuffer_ = np.zeros((iter))
t = np.linspace(0, iter, iter)

# 繪圖設定
fig, (ax, ax_) = plt.subplots(2, 1)

# Initialize lines
line,  = ax.plot([], [], label='Curve 1')
line_, = ax_.plot([], [], label='Curve 2')

# Set legend for the first time
ax.legend()
ax_.legend()



for i in range(iter):
    control_output = pid.update(NowPos)
    control_output_ = pid_.update(NowPos_)

    NowPos += control_output
    NowPos_ += control_output_

    posBuffer[i] = NowPos
    posBuffer_[i] = NowPos_

    # # ax.cla()
    # # ax.plot(t[:i], posBuffer[:i])
    # # plt.pause(0.03)
    
    # ax.cla()
    # ax.plot(t[:i], posBuffer[:i], label='Curve 1')
    # ax.set_title('Dynamic Curve 1')
    # ax.legend()

    # ax_.cla()
    # ax_.plot(t[:i], posBuffer_[:i], label='Curve 2')
    # ax_.set_title('Dynamic Curve 2')
    # ax_.legend()
    
    # 增量式繪圖(速度較快)
    line.set_data(t[:i+1], posBuffer[:i+1])
    line_.set_data(t[:i+1], posBuffer_[:i+1])

    # Update plot without clearing
    ax.set_xlim(0, iter)  # Ensure correct x-axis range
    ax.set_ylim(min(posBuffer) - 5, max(posBuffer) + 5)  # Adjust y-axis range
    ax_.set_xlim(0, iter)
    ax_.set_ylim(min(posBuffer_) - 5, max(posBuffer_) + 5)

    # Update plot without clearing
    ax.set_title('Dynamic Curve 1')
    ax_.set_title('Dynamic Curve 2')

    
    # 調整圖間距
    fig.subplots_adjust(hspace=0.4)

    plt.draw()
    plt.pause(0.03)


    # print(f"NowPos: {NowPos:.2f}, Control Output: {control_output:.2f}")

plt.show()



class FeedforwardController:
    def __init__(self, feedforward_gain):
        self.feedforward_gain = feedforward_gain

    def compute_feedforward(self, reference):
        # Simple feedforward control law
        feedforward_output = self.feedforward_gain * reference
        return feedforward_output

class FeedbackController:
    def __init__(self, feedback_gain):
        self.feedback_gain = feedback_gain

    def compute_feedback(self, error):
        # Simple proportional feedback control law
        feedback_output = self.feedback_gain * error
        return feedback_output
    
# # Main control loop
# def main_control_loop(reference):
#     # Constants for the controllers
#     feedforward_gain = 0.1
#     feedback_gain = 0.05

#     # Create instances of the controllers
#     feedforward_controller = FeedforwardController(feedforward_gain)
#     feedback_controller = FeedbackController(feedback_gain)

#     # System's current state (position in this example)
#     current_state = 0.0

#     # Data buffer
#     feedforwardData = np.zeros((10))
#     feedbackData = np.zeros((10))
#     totalData = np.zeros((10))


#     # Loop through time steps
#     for _ in range(10):
#         # Compute feedforward control output
#         feedforward_output = feedforward_controller.compute_feedforward(reference)

#         # Compute feedback error
#         error = reference - current_state

#         # Compute feedback control output
#         feedback_output = feedback_controller.compute_feedback(error)

#         # Combined control output
#         total_output = feedforward_output + feedback_output

#         # Update the system state (in this simple example, just adding the control output)
#         current_state += total_output

#         feedforwardData[_] = feedforward_output
#         feedbackData[_] = feedback_output
#         totalData[_] = total_output
#         # Print results
#         print(f"Reference: {reference}, Current State: {current_state}, Control Output: {total_output}")

    
#     t = np.linspace(0, 10, num=10)
#     plt.plot(t, feedforwardData)
#     plt.plot(t, feedbackData)
#     plt.plot(t, totalData)
#     plt.show()

# # Example: Set a reference position and run the control loop
# main_control_loop(reference=10.0)



