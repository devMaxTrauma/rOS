notifications = []

notifications_management_enabled = True
notifications_management_thread = None
sound_engine = None

try:
    import threading
except ImportError:
    raise ImportError("Threading not found or failed to load.")
try:
    import time
except ImportError:
    raise ImportError("Time not found or failed to load.")
try:
    import math
except ImportError:
    raise ImportError("Math not found or failed to load.")


class Notification:
    display_visibility = 0.0
    display_duration = 10.0
    notification_finished = False
    function_x = 0

    def __init__(self, icon, message):
        self.icon = icon
        self.message = message
        self.notification_start_time = time.time()
        self.notification_thread = threading.Thread(target=self.notification_thread_routine).start()

    def notification_thread_routine(self):
        while self.function_x <2.0: self.increase_notification_size()
        self.display_visibility = 1.0
        while time.time() - self.notification_start_time < Notification.display_duration: time.sleep(0.1)
        self.function_x = 0
        while self.function_x < 1.0: self.decrease_notification_size()
        self.display_visibility = 0.0
        self.notification_finished = True
        pass

    def increase_notification_size(self):
        if self.function_x<=1: self.display_visibility = math.sqrt(self.function_x)
        elif self.function_x<=2: self.display_visibility = 1 + 0.3535533906*(2 - self.function_x) * math.sin(self.function_x-1)
        self.function_x += 0.01
        time.sleep(0.005)

    def decrease_notification_size(self):
        self.display_visibility = math.pow(self.function_x-1, 2)
        self.function_x += 0.01
        time.sleep(0.005)


def add_notification(icon, notification):
    global notifications
    notifications.append(Notification(icon, notification))
    if sound_engine is not None: sound_engine.play("boot/res/alert.mp3", volume=2.0)
    return notifications[-1]


def get_notification(icon=None, message=None):
    global notifications
    if icon is None and message is None: return notifications

    candidates = []
    for notification in notifications:
        if icon is not None and notification.icon != icon: continue
        if message is not None and notification.message != message: continue
        candidates.append(notification)

    if len(candidates) == 0: return None
    elif len(candidates) == 1: return candidates[0]
    else: return candidates


def notification_management_routine(notification):
    global notifications
    if notification.notification_finished:
        notifications.remove(notification)
        return
    pass


def notifications_management_routine():
    global notifications
    global notifications_management_enabled
    while notifications_management_enabled:
        for notification in notifications: notification_management_routine(notification)
        time.sleep(0.01)


def close():
    global notifications_management_enabled
    notifications_management_enabled = False
    global notifications_management_thread
    if notifications_management_thread is not None: notifications_management_thread.join
    pass


notifications_management_thread = threading.Thread(target=notifications_management_routine).start()
