"""
kimsufichecker - cli
"""
import shlex
import subprocess
from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime
from time import sleep
import requests
from colorama import Fore

URL_API = (
    "https://www.kimsufi.com/fr/js/dedicatedAvailability/availability-data-ca.json"
)


def now():
    """
    return the current date as string
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def execute(command: str, plan: str):
    if command:
        try:
            command = command.format(plan=plan)
            cmd = shlex.split(command)
            process = subprocess.run(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
            )
            message(
                Fore.CYAN,
                f"Command '{command}' exited with {process.returncode}",
                prefix="",
            )
            return process.returncode
        except BaseException as e:  # pylint: disable=broad-except,invalid-name
            message(
                Fore.RED,
                f"Disabling command '{command}'' because of error: {e}",
                prefix="",
            )


def get_data() -> dict:
    """
    get the json payload from kimsufi API
    """
    return requests.get(URL_API).json()


def get_available_zones(data: dict, plan: str, filter_zones: list) -> list:
    """
    find available zones in payload
    """
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
    raise ValueError(f"Cannot find plan: {plan}")


def dot(color):
    """
    print a dot with given color
    """
    print(f"{color}.{Fore.RESET}", flush=True, end="")


def message(color, msg: str, prefix: str = "\n"):
    """
    print a message with a color and the date
    """
    print(
        f"{prefix}{color}[{now()}] {msg}{Fore.RESET}",
        flush=True,
    )


def run():
    """
    entrypoint
    """
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
        help="duration (in seconds) between checks, default: 60",
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
        "-1",
        "--execute-on-init",
        action="store_true",
        help="execute -x/-X action on first check, by default actions are run when plan status change",
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
        for plan in sorted(plans):
            print(" ", plan)
        print("List of zones:")
        for zone in sorted(zones):
            print(" ", zone)
    else:
        availability = None
        while True:
            try:
                if availability is None:
                    # first loop
                    availability = OrderedDict([(p, None) for p in args.plans])
                else:
                    sleep(args.sleep)

                data = get_data()
                for plan, previous_zones in availability.items():
                    current_zones = get_available_zones(data, plan, args.zones or [])
                    availability[plan] = current_zones
                    if previous_zones is None:
                        # No previous data
                        if len(current_zones) == 0:
                            message(
                                Fore.YELLOW,
                                f"Plan {plan} is initially not available",
                                prefix="",
                            )
                            if (
                                args.execute_on_init
                                and execute(args.not_available, plan) is None
                            ):
                                args.not_available = None
                        else:
                            message(
                                Fore.GREEN,
                                f"Plan {plan} is initially available",
                                prefix="",
                            )
                            if (
                                args.execute_on_init
                                and execute(args.available, plan) is None
                            ):
                                args.available = None
                    elif previous_zones == current_zones:
                        # No change
                        dot(Fore.GREEN if len(previous_zones) else Fore.YELLOW)
                    elif len(current_zones) == 0:
                        # Not available anymore
                        message(Fore.YELLOW, f"Plan {plan} is not available anymore")
                        if execute(args.not_available, plan) is None:
                            args.not_available = None
                    else:
                        # Becomes available
                        message(Fore.GREEN, f"Plan {plan} is now available")
                        if execute(args.available, plan) is None:
                            args.available = None
            except KeyboardInterrupt:
                break
            except BaseException as e:  # pylint: disable=broad-except,invalid-name
                message(Fore.RED, f"Error: {e}")
