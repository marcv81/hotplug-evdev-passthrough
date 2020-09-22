import aionotify
import asyncio
import capabilities
import evdev
import yaml


async def forward_device(name, from_device, to_device):
    """Forward events from one device to another."""

    from_device.grab()
    print("Connected %s" % name)
    try:
        async for event in from_device.async_read_loop():
            to_device.write_event(event)
            to_device.syn()
    except OSError:
        print("Disconnected %s" % name)


def find_devices(query):
    """Find the connected devices matching a query."""

    for path, name in query.items():
        try:
            path = "/dev/input/by-path/" + path
            device = evdev.InputDevice(path)
            yield name, device
        except OSError:
            pass


async def monitor_devices(query):
    """Monitor for new devices matching a query."""

    watcher = aionotify.Watcher()
    watcher.watch("/dev/input/by-path/", aionotify.Flags.CREATE)
    await watcher.setup(asyncio.get_event_loop())
    while True:
        event = await watcher.get_event()
        if event.name in query:
            try:
                name = query[event.name]
                path = "/dev/input/by-path/" + event.name
                device = evdev.InputDevice(path)
                yield name, device
            except OSError:
                pass


async def main():
    """Main loop."""

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    query = dict([path, name] for (name, path) in config["devices"].items())

    virtual_devices = {
        "keyboard": evdev.uinput.UInput(capabilities.keyboard, "virtual-keyboard"),
        "mouse": evdev.uinput.UInput(capabilities.mouse, "virtual-mouse"),
    }

    # First handle the already connected devices.
    for name, device in find_devices(query):
        asyncio.ensure_future(forward_device(name, device, virtual_devices[name]))
    # Then monitor for new devices and handle them.
    async for name, device in monitor_devices(query):
        asyncio.ensure_future(forward_device(name, device, virtual_devices[name]))


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
