# Intro

QEMU evdev passthrough does not support disconnecting and reconnecting the keyboard and the mouse. This can be a problem when using a KVM switch. As a workaround, this project dynamically attaches physical devices to long-lived virtual devices.

# Setup

Configure `config.yaml` with the devices from `/dev/input/by-path`.

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
