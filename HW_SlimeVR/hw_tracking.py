import json
import sys
import threading
import argparse

import numpy as np

from typing import List, Any
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


class HWTracking:

    def __init__(self, addr: str = "127.0.0.1", port: int = 9000, track_points: list = None):
        self._addr = addr
        self._port = port

        with open(r"C:\Dev\MoveCritic_HW\tracker_map.json") as json_file:
            self._TRACKER_MAP = json.load(json_file)["tracker_map"]

        if track_points is None:
            self._track_points = ["l_ankle", "l_thigh", "hip"]
        else:
            if set(track_points).issubset(list(self._TRACKER_MAP.keys())):
                self._track_points = track_points
            else:
                print(f"ERROR: Invalid HW tracking point passed during HWTracking class instantiation.")
                sys.exit()

        self._pos = dict()
        for track_point in self._track_points:
            self._pos[track_point] = np.zeros(3)

        self._osc_server_thread = threading.Thread(target=self.osc_server)
        self._osc_server_thread.start()

    @property
    def track_points(self) -> list:
        return self._track_points

    @property
    def pos(self) -> np.array:
        return self._pos

    def get_position_data(self, track_point: str) -> np.array:
        if track_point in self._TRACKER_MAP.keys():
            return self._pos[track_point]
        else:
            print(f"ERROR: '{track_point}' is an invalid HW tracking point.")

    def position_handler(self, address: str, fixed_args: List[Any], *osc_args: List[Any]) -> None:
        self._pos[fixed_args[0]] = np.array(osc_args)

    def osc_server(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=self._addr, help="The ip to listen on")
        parser.add_argument("--port", type=int, default=self._port, help="The port to listen on")
        args = parser.parse_args()

        dispatcher = Dispatcher()
        for track_point in self._track_points:
            tracker_id = self._TRACKER_MAP[track_point]
            dispatcher.map(f"/tracking/trackers/{tracker_id}/position", self.position_handler, *[track_point])

        server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()
