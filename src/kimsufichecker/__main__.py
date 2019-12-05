import shlex
import subprocess
from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime
from time import sleep

import requests
from pytput import print_color

URL_API = (
    "https://www.kimsufi.com/fr/js/dedicatedAvailability/availability-data-ca.json"
)


def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def execute(command: str, plan: str):
    if command:
        try:
            command = command.format(plan=plan)
            cmd = shlex.split(command)
            p = subprocess.run(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            print_color(
                "yellow",
                "[{date}] Command {cmd} exited with {p.returncode}".format(
                    date=now(), cmd=command, p=p
                ),
                flush=True,
            )
            return p.returncode
        except BaseException as e:
            print_color(
                "red",
                "[{date}] Disabling command {cmd} because of error: {txt}".format(
                    date=now(), cmd=command, txt=str(e)
                ),
                flush=True,
            )


def get_data() -> dict:
    return requests.get(URL_API).json()


def get_available_zones(data: dict, plan: str, filter_zones: list) -> list:
    for item in data["availability"]:
        if item["reference"] == plan:
            return sorted(
                filter(
                    lambda z: len(filter_zones) == 0
                    or z.lower() in map(str.lower, filter_zones),
                    [
                        z["zone"]
                        for z in item["zones"]
                        if z["availability"] != "unavailable"
                    ],
                )
            )
    raise ValueError("Cannot find plan: " + plan)


def main():
    parser = ArgumentParser(
        "kimsufi-checker",
        description="tool to perform actions when Kimsufi availabilty changes",
    )
    parser.add_argument(
        "-s",
        "--sleep",
        metavar="SECONDS",
        type=int,
        default=60,
        help="Duration (in seconds) between checks, default: 60",
    )
    parser.add_argument(
        "-z",
        "--zone",
        dest="zones",
        action="append",
        metavar="ZONE",
        help="check availability in specific zones (example: rbx or gra)",
    )
    parser.add_argument(
        "-x",
        "--available",
        metavar="COMMAND",
        help="command to execute when plan becomes available",
    )
    parser.add_argument(
        "-X",
        "--not-available",
        metavar="COMMAND",
        help="command to execute when plan is not available anymore",
    )
    parser.add_argument(
        "plans", nargs="*", help="plans to check, example 1801sk13 or 1801sk14"
    )
    args = parser.parse_args()
    if len(args.plans) == 0:
        data = get_data()
        plans = set()
        zones = set()
        for pref in data["availability"]:
            plans.add(pref["reference"])
            for zref in pref["zones"]:
                zones.add(zref["zone"])
        print("List of plans:")
        for p in sorted(plans):
            print(" ", p)
        print("List of zones:")
        for z in sorted(zones):
            print(" ", z)
    else:
        availability = None
        while True:
            try:
                if availability is None:
                    availability = OrderedDict([(p, None) for p in args.plans])
                else:
                    sleep(args.sleep)

                data = get_data()
                for plan, previous_zones in availability.items():
                    current_zones = get_available_zones(data, plan, args.zones or [])
                    availability[plan] = current_zones
                    if previous_zones is None:
                        # No previous data
                        print_color("cyan", ".", flush=True, end="")
                    elif previous_zones == current_zones:
                        # No change
                        print_color("green", ".", flush=True, end="")
                    elif len(current_zones) == 0:
                        # Not available anymore
                        print_color(
                            "purple",
                            "\n[{date}] Plan {plan} is not available anymore".format(
                                date=now(), plan=plan
                            ),
                            flush=True,
                        )
                        if execute(args.not_available, plan) is None:
                            args.not_available = None
                    else:
                        # Becomes available
                        print_color(
                            "green",
                            "\n[{date}] Plan {plan} is available".format(
                                date=now(), plan=plan
                            ),
                            flush=True,
                        )
                        if execute(args.available, plan) is None:
                            args.available = None
            except KeyboardInterrupt:
                break
            except BaseException as e:
                print_color(
                    "red",
                    "\n[{date}] Error: {txt}".format(date=now(), txt=str(e)),
                    flush=True,
                )


if __name__ == "__main__":
    main()
