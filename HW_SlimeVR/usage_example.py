from HW_SlimeVR.hw_tracking import HWTracking


UDP_ADDR = "127.0.0.1"
UDP_PORT = 9000
TRACKING_POINTS = ["l_ankle", "l_thigh", "r_ankle", "r_thigh", "hip"]


def main():
    hw = HWTracking(addr=UDP_ADDR, port=UDP_PORT, track_points=TRACKING_POINTS)   # Create HWTracking object

    while 1:
        l_ankle_position = hw.get_position_data(track_point="l_ankle")  # Get current positional data for a tracking point
        print(f"Left Ankle:\nx [m]: {l_ankle_position[0]}\ny [m]: {l_ankle_position[1]}\nz [m]: {l_ankle_position[2]}\n")


if __name__ == "__main__":
    main()
