from datetime import datetime

START_TIME = datetime.strptime('2022-10-05 11:09:55', '%Y-%m-%d %H:%M:%S')
END_TIME = datetime.strptime('2022-10-05 15:19:36', '%Y-%m-%d %H:%M:%S')
duration = END_TIME - START_TIME
durationSecs = duration.total_seconds()
totalHours = divmod(durationSecs, 3600)[0]
totalMinutes = divmod(durationSecs, 60)[0]
with open('duration.txt', 'a') as f:
    f.write('\nTime before blocking: %s' % duration)
    f.write('\nSleep time: %s minute(s)' % 3)
    f.write('\n------------------\n')
