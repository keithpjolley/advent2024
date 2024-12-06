#!/usr/bin/env python3

import asyncio
import sys


async def main(args):
    """Run the "command" given as the first arg, pass all other args to the command.
    "dump" is run if no command/args given.
    """
    if len(args) > 0:
        cmd = args.pop(0)
        # Not sure why this doesn't follow convention...
        if cmd == "delete":
            cmd = "delete_node"
    else:
        cmd = "dump"

    command = getattr(SiteClient, cmd, None)
    if command is None:
        print(f"Unknown command: '{cmd}'", file=sys.stderr)
        return 1

    await command(args)


class SiteClient:
    async def list(self):
        print("List")

    async def dump(self):
        print("Dump")

    async def set_z(self, args):
        print("Set Z")

    async def set_min(self, args):
        print("Set Min")

    async def set_bounds(self, args):
        print("Set Bounds")

    async def set_z_params(self, args):
        print("Set Z Params")

    async def gen_config(self, args):
        print("Gen Config")

    async def gen_anchor_list(self, args):
        print("Gen Anchor List")

    async def create_hub(self, args):
        print("Create Hub")

    async def create_anchor(self, args):
        print("Create Anchor")

    async def create_tracker(self, args):
        print("Create Tracker")

    async def delete_node(self, args):
        print("Delete Node")

    async def import_hubs(self, args):
        print("Import Hubs")

    async def import_anchors(self, args):
        print("Import Anchors")

    async def import_trackers(self, args):
        print("Import Trackers")

    async def replace_tracker(self, args):
        print("Replace Tracker")

    async def download(self, args):
        print("Download")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main(sys.argv[1:]))
