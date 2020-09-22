# Intro

QEMU evdev passthrough stops if the physical keyboard and mouse are disconnected, but does not restart when they are reconnected. This can be a problem when using a KVM switch.

This project dynamically attaches physical devices to virtual devices. The physical devices can be disconnected and reconnected, but the virtual devices remain connected. This provides a workaround to the problem described above.

# Setup

Find the physical devices to handle with `ls -alh /dev/input/by-id/`. Find their associated path with `ls -alh /dev/input/by-path/`. Configure `config.yaml` with the devices paths.

Add the user to the `input` group.

    sudo usermod -a -G input user

Add the following udev rules, for instance in `/etc/udev/rules.d/80-virtual-input.rules`.

    ACTION=="add", SUBSYSTEM=="input", ATTRS{phys}=="py-evdev-uinput", ATTRS{name}=="virtual-keyboard", SYMLINK+="input/by-id/virtual-keyboard"
    ACTION=="add", SUBSYSTEM=="input", ATTRS{phys}=="py-evdev-uinput", ATTRS{name}=="virtual-mouse", SYMLINK+="input/by-id/virtual-mouse"

Set up the environment.

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

Start the program.

    python3 start.py

The following input devices should be available.
- `/dev/input/by-id/virtual-mouse`
- `/dev/input/by-id/virtual-keyboard`

The program should capture events on the pysical devices, and re-emit from the virtual devices. You can verify with `evtest`.
