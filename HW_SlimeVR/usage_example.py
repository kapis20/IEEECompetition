import time

from HW_SlimeVR.hw_tracking import HWTracking


UDP_ADDR = "127.0.0.1"
UDP_PORT = 9000
TRACKING_POINTS = ["l_ankle", "l_thigh", "r_ankle", "r_thigh", "hip"]

INTERVAL = 0.01


def main():
    hw = HWTracking(addr=UDP_ADDR, port=UDP_PORT, track_points=TRACKING_POINTS)   # Create HWTracking object

    t_last = 0
    while 1:
        t_current = time.time()
        if t_current - t_last > INTERVAL:
            l_ankle_position = hw.get_position_data(track_point="l_ankle")  # Get current positional data for a tracking point
            print(f"Left Ankle:\nx [m]: {l_ankle_position[0]}\ny [m]: {l_ankle_position[1]}\nz [m]: {l_ankle_position[2]}\n")
            t_last = t_current


if __name__ == "__main__":
    main()
