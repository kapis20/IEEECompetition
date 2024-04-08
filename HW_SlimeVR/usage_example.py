import time

from HW_SlimeVR.hw_tracking import HWTracking


UDP_ADDR = "127.0.0.1"
UDP_PORT = 9000
# TRACKING_POINTS = ["l_ankle", "l_thigh", "r_ankle", "r_thigh", "hip"]
TRACKING_POINTS = None
TRACKING_POINT_FOCUS = "l_shoulder"

INTERVAL = 0.01


def main():
    hw = HWTracking(addr=UDP_ADDR, port=UDP_PORT, track_points=TRACKING_POINTS)   # Create HWTracking object

    t_last = 0
    while 1:
        t_current = time.time()
        if t_current - t_last > INTERVAL:
            position_data = hw.get_position_data(track_point=TRACKING_POINT_FOCUS)  # Get current positional data for a tracking point
            print(f"{TRACKING_POINT_FOCUS}:\nx [m]: {position_data[0]}\ny [m]: {position_data[1]}\nz [m]: {position_data[2]}\n")

            # data_dict = hw.pos
            # for index, data in enumerate(list(data_dict.values())):
            #     print(f"{list(data_dict.keys())[index]}, Tracker_index = {hw._TRACKER_MAP[list(data_dict.keys())[index]]}:\nx: {data[0]}\ny: {data[1]}\nz: {data[2]}\n")

            t_last = t_current


if __name__ == "__main__":
    main()
