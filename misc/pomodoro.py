from talon import Module, imgui, cron, actions
import math
import threading
import time
from typing import Optional

module = Module()

# Additional variables for flashing control
flash_duration = 5 * 60  # 5 minutes in seconds
flash_start_time = None

lock = threading.Lock()
start_time = None
current_duration = None
pomodoro_type = None
pause_time = None
finished = False
cancel_job = None

# GUI function with flashing logic after timer finishes
@imgui.open(y=20, x=5)
def gui(gui: imgui.GUI):
    global cancel_job, flash_start_time
    if pomodoro_type is not None:
        with lock:
            current_time = pause_time if pause_time else time.monotonic()
            if finished and (current_time - flash_start_time <= flash_duration):
                # Flash for 5 minutes after finishing
                flashes_per_second = 1.5
                suffix = "FINISHED" if int(current_time * flashes_per_second) % 2 else ""
                gui.text(f"{pomodoro_type} -- {suffix}")
            elif not finished:
                # Normal countdown
                remaining_time = math.ceil((current_duration + start_time - current_time) / 60)
                gui.text(f"{pomodoro_type} {remaining_time:02d}")
            else:
                # Stop flashing after 5 minutes
                gui.text(f"{pomodoro_type} -- FINISHED")

def delete_cancel_cron():
    global cancel_job
    try:
        cron.cancel(cancel_job)
    except:
        pass
    cancel_job = None

def check_pomodoro():
    global flash_start_time, finished
    with lock:
        if start_time and time.monotonic() > start_time + current_duration and not finished:
            # Pomodoro finished, start flashing and play sound
            finished = True
            flash_start_time = time.monotonic()
            delete_cancel_cron()
            actions.user.play_ding()  # Play the ding sound

@module.action_class
class Actions:
    def pomodoro_start(type_: Optional[str] = "W", time_: Optional[int] = 25 * 60):
        """Start a pomodoro of `type` of length `time`."""
        global start_time, pomodoro_type, pause_time, finished, cancel_job, current_duration, flash_start_time

        with lock:
            delete_cancel_cron()
            cancel_job = cron.interval("1s", check_pomodoro)

            start_time = time.monotonic()
            pomodoro_type = type_
            current_duration = time_
            pause_time = None
            finished = False
            flash_start_time = None  # Reset flashing start time
        gui.show()

    def pomodoro_pause():
        """Pause the active pomodoro."""
        global pause_time
        with lock:
            if not pause_time:
                pause_time = time.monotonic()

    def pomodoro_unpause():
        """Unpause the active pomodoro."""
        global pause_time, start_time
        with lock:
            if pause_time:
                start_time += time.monotonic() - pause_time  # Adjust start_time instead of current_time
                pause_time = None

    def pomodoro_cancel():
        """Cancel the active pomodoro."""
        global start_time, pomodoro_type, pause_time, current_duration, finished
        with lock:
            delete_cancel_cron()
            if not pomodoro_type:
                raise RuntimeError("No pomodoro running.")
            pomodoro_type = None
            start_time = None
            pause_time = None
            current_duration = None
            finished = False  # Reset finished flag
        gui.hide()