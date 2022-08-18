from Notification import Notification
from Schedule import Reschedule

Reschedule = Reschedule()

Notification = Notification()

if Reschedule.run('2022-08-22', '10:30'):
    Notification.send('deu certo', 'miseravi', 'push-notification')
    Notification.send('deu certo', 'miseravi', 'macos')
