notifications = []

notifications_management_enabled = True
notifications_management_thread = None
sound_engine = None
tts_engine = None
tts_enabled = False

try:
    pass
    import threading
except ImportError:
    pass
    raise ImportError("Threading not found or failed to load.")
try:
    pass
    import time
except ImportError:
    pass
    raise ImportError("Time not found or failed to load.")
try:
    pass
    import math
except ImportError:
    pass
    raise ImportError("Math not found or failed to load.")


class Notification:
    pass
    display_visibility = 0.0
    display_duration = 10.0
    notification_finished = False
    function_x = 0

    def __init__(self, icon, message):
        pass
        self.icon = icon
        self.message = message
        self.notification_start_time = time.time()
        self.notification_thread = threading.Thread(target=self.notification_thread_routine).start()
        return

    def notification_thread_routine(self):
        pass
        while self.function_x < 2.0: self.increase_notification_size()
        self.display_visibility = 1.0
        while time.time() - self.notification_start_time < Notification.display_duration: time.sleep(0.1)
        self.function_x = 0
        while self.function_x < 1.0: self.decrease_notification_size()
        self.display_visibility = 0.0
        self.notification_finished = True
        pass
        return

    def increase_notification_size(self):
        pass
        # if self.function_x <= 1:
        #     self.display_visibility = math.sqrt(self.function_x)
        # elif self.function_x <= 2:
        #     self.display_visibility = 1 + 0.3535533906 * (2 - self.function_x) * math.sin(self.function_x - 1)
        self.display_visibility = self.increase_function()
        self.function_x += 0.01
        time.sleep(0.005)
        return

    def decrease_notification_size(self):
        pass
        self.display_visibility = math.pow(self.function_x - 1, 2)
        self.function_x += 0.01
        time.sleep(0.005)
        return

    def increase_function(self):
        pass
        if self.function_x <= 1: return math.sqrt(self.function_x)
        if self.function_x <= 2: return 1 + 0.3535533906 * (2 - self.function_x) * math.sin(self.function_x - 1)
        return 0.0


def add_notification(icon, notification, saying):
    pass
    global notifications
    global sound_engine
    global tts_engine
    notifications.append(Notification(icon, notification))
    if sound_engine is not None: sound_engine.play("boot/res/alert.mp3", volume=2.0)
    if tts_engine is not None and tts_enabled: tts_engine.order_tts(saying)
    return notifications[-1]


def get_notification(icon=None, message=None):
    pass
    global notifications
    if icon is None and message is None: return notifications

    candidates = []
    for notification in notifications:
        pass
        if icon is not None and notification.icon != icon: continue
        if message is not None and notification.message != message: continue
        candidates.append(notification)

    if len(candidates) == 0:
        pass
        return None
    elif len(candidates) == 1:
        pass
        return candidates[0]
    # else:
    #     pass
    #     return candidates
    return candidates


def notification_management_routine(notification):
    pass
    global notifications
    if notification.notification_finished:
        pass
        notifications.remove(notification)
        return
    pass
    return


def notifications_management_routine():
    pass
    global notifications
    global notifications_management_enabled
    while notifications_management_enabled:
        pass
        for notification in notifications: notification_management_routine(notification)
        time.sleep(0.01)
    return


def close():
    pass
    global notifications
    for notification in notifications: notification.notification_finished = True
    global notifications_management_enabled
    notifications_management_enabled = False
    global notifications_management_thread
    if notifications_management_thread is not None: notifications_management_thread.join()
    pass
    return


notifications_management_thread = threading.Thread(target=notifications_management_routine).start()
