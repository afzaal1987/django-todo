import subprocess

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


DEFAULT_VM_CONTROL_COMMANDS = {
    "vm1": {
        "name": "Virtual Machine 1",
        "power_on": ["echo", "Power ON command executed for VM 1"],
        "power_off": ["echo", "Power OFF command executed for VM 1"],
    },
    "vm2": {
        "name": "Virtual Machine 2",
        "power_on": ["echo", "Power ON command executed for VM 2"],
        "power_off": ["echo", "Power OFF command executed for VM 2"],
    },
    "vm3": {
        "name": "Virtual Machine 3",
        "power_on": ["echo", "Power ON command executed for VM 3"],
        "power_off": ["echo", "Power OFF command executed for VM 3"],
    },
    "vm4": {
        "name": "Virtual Machine 4",
        "power_on": ["echo", "Power ON command executed for VM 4"],
        "power_off": ["echo", "Power OFF command executed for VM 4"],
    },
    "vm5": {
        "name": "Virtual Machine 5",
        "power_on": ["echo", "Power ON command executed for VM 5"],
        "power_off": ["echo", "Power OFF command executed for VM 5"],
    },
}


def _vm_commands():
    return getattr(settings, "VM_CONTROL_COMMANDS", DEFAULT_VM_CONTROL_COMMANDS)


def index(request):
    vm_list = [
        {"id": vm_id, "name": config.get("name", vm_id.upper())}
        for vm_id, config in _vm_commands().items()
    ]
    return render(request, "todos/index.html", {"vm_list": vm_list})


@require_POST
def control_vm(request, vm_id):
    action = request.POST.get("action")
    if action not in ("power_on", "power_off"):
        messages.error(request, "Invalid VM action.")
        return redirect("todos:index")

    vm_config = _vm_commands().get(vm_id)
    if vm_config is None:
        messages.error(request, "Unknown VM selected.")
        return redirect("todos:index")

    command = vm_config.get(action)
    if not command:
        messages.error(request, "Command is not configured for this VM action.")
        return redirect("todos:index")

    try:
        shell_mode = isinstance(command, str)
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            shell=shell_mode,
        )
        output = (result.stdout or "").strip()
        state = "ON" if action == "power_on" else "OFF"
        if output:
            messages.success(request, "%s switched %s. %s" % (vm_config.get("name", vm_id), state, output))
        else:
            messages.success(request, "%s switched %s." % (vm_config.get("name", vm_id), state))
    except (subprocess.CalledProcessError, OSError, TypeError, ValueError) as exc:
        messages.error(request, "Failed to control %s: %s" % (vm_config.get("name", vm_id), exc))

    return redirect("todos:index")