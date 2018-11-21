import sys
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, \
    QApplication
from PyQt5 import QtGui
import design
from pandas import read_csv
from datetime import timedelta as td
from datetime import datetime
import calendar


class WorkOverApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        #globals
        self.default_short_date_mask = "%d\n%m\n%a"
        self.default_long_date_mask = "%Y-%m-%d %H:%M:%S"
        self.file = os.getcwd()+"/stats.log"
        self.current_date = self.calendarWidget.selectedDate().toPyDate()
        self.hours_per_day = 4
        self.days_per_week = 5

        #start session and write down to the stats.log
        self.log('start')

        #read the stats log
        self.data = read_csv(self.file, names = ['ind', 'datetime'])

        #processing self_data to array of unique dates and intervals
        self.data = [(a[0], datetime.strptime(a[1], self.default_long_date_mask))
                     for a in zip(self.data.ind, self.data.datetime)]
        dates = set()
        for a in self.data:
            dates.add(a[1].date())
        self.data.append(("stop", datetime.now()))
        self.data = list(zip(list([a for a in self.data if a[0] == "start"]),
                             list([a for a in self.data if a[0] == "stop"])))
        dates = sorted(list(dates))
        sec_diffs = []
        for a in self.data:
            sec_diffs.append((a[0][1].date(), a[1][1]-a[0][1], a[1][1], a[0][1]))
        dates_and_hours = [[b, sum([a[1].total_seconds()/3600
                                    for a in sec_diffs if a[0] == b]),
                            [(a[2], a[3])
                            for a in sec_diffs if a[0] == b]]
                           for b in dates]

        self.data_to_show = list([[a[0].strftime(self.default_short_date_mask), a[1], a[2]] for a in dates_and_hours])

        self.dates_and_hours = dates_and_hours[:] #copying

        #summarizes and plotting
        today = self.current_date
        start = sorted(self.dates_and_hours, key = lambda date: self.dates_and_hours[0])[0][0]
        end = today
        self.show_summaries(start, end)

        self.plot_data()

        #listeners
        self.calendarWidget.selectionChanged.connect(self.date_changed)
        self.per_all_rb.toggled.connect(self.rb_toggled)
        self.per_month_rb.toggled.connect(self.rb_toggled)
        self.per_week_rb.toggled.connect(self.rb_toggled)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    #listeners' realisation
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.log('stop')

    def date_changed(self):
        self.current_date = self.calendarWidget.selectedDate().toPyDate()
        self.rb_toggled()

    def rb_toggled(self):
        period = ""
        if self.per_all_rb.isChecked():
            period = "all"
        if self.per_month_rb.isChecked():
            period = "month"
        if self.per_week_rb.isChecked():
            period = "week"
        self.plot_data()
        self.data_to_show = self.get_data_to_show(period)

    #utility functions
    def get_data_to_show(self, period = "week"):
        today = self.current_date
        start = sorted(self.dates_and_hours, key = lambda date: self.dates_and_hours[0])[0][0]
        end = today
        if period == "week":
            start = today - td(days = int(today.weekday()))
            end = start + td(days = self.days_per_week-1)
            self.show_summaries(start, end)
            return list([(a[0].strftime(self.default_short_date_mask),
                          a[1], a[2]) for a in self.dates_and_hours if start <= a[0] <= end])
        if period == "month":
            cal = calendar.Calendar().monthdatescalendar(today.year, today.month)
            start = sorted([a for a in cal[0] if a.month == today.month])[0]
            end = sorted([a for a in cal[-1] if a.month == today.month])[-1]
            self.show_summaries(start, end)
            return list([(a[0].strftime(self.default_short_date_mask),
                          a[1], a[2]) for a in self.dates_and_hours if start <= a[0] <= end])
        else:
            self.show_summaries(start, end)
            return list([(a[0].strftime(self.default_short_date_mask),
                          a[1], a[2]) for a in self.dates_and_hours])

    def show_summaries(self, start, end):
        workdays = []
        for a in range((end - start).days+1):
            day = start + td(days = a)
            if day.weekday() not in (5, 6) and day <= self.current_date.today():
                workdays.append(day)
        self.required_label.setText(WorkOverApp.time_from_seconds(len(workdays)*self.hours_per_day*3600))
        seconds = sum([a[1] for a in self.data_to_show])*3600
        self.done_label.setText(str(WorkOverApp.time_from_seconds(seconds)))
        today_sum = [a for a in self.data_to_show if self.current_date.strftime(self.default_short_date_mask) == a[0]]
        today_sum = today_sum[0] if len(today_sum) > 0 else (self.current_date.strftime(self.default_short_date_mask),
                                                             0)
        self.done_label_2.setText(WorkOverApp.time_from_seconds(today_sum[1] * 3600))
        workover = abs(seconds - len(workdays)*self.hours_per_day*3600)
        self.workover_label.setText(WorkOverApp.time_from_seconds(workover) if
                                    seconds - len(workdays)*self.hours_per_day*3600 > 0
                                    else "-"+WorkOverApp.time_from_seconds(workover))

    def get_vlines(self):
        xses = []
        ymins = []
        ymaxs = []
        for a in self.data_to_show:
            mins = list([(b[0]-b[0].replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()/3600
                         for b in a[2]])
            maxs = list([(b[1]-b[1].replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()/3600
                         for b in a[2]])
            ymins.extend(mins)
            ymaxs.extend(maxs)
            xses.extend([a[0]]*len(list(zip(mins, maxs))))

        return xses, ymins, ymaxs

    def log(self, mode):
        with open(self.file, 'a') as f:
            out = mode
            out = out + ','
            out = out + datetime.now().strftime(self.default_long_date_mask)
            out.replace(' ', '')
            print(out, file = f)

    def update_time(self):
        try:
            if self.data_to_show[-1][2][0][0].date() == self.current_date.today():
                self.data_to_show[-1] = list(self.data_to_show[-1])
                self.data_to_show[-1][2][-1] = list(self.data_to_show[-1][2][-1])
                self.data_to_show[-1][2][-1][0] = datetime.now()
                self.data_to_show[-1][1] = sum([(a[0] - a[1]).total_seconds() / 3600 for a in self.data_to_show[-1][2]])
                self.rb_toggled()
        except IndexError:
            pass

    def plot_data(self):
        self.prepare_axes()
        vlines = self.get_vlines()
        d1 = self.data_to_show[0][2][0][1].replace(hour=0, minute=0, second=0, microsecond=0)
        d2 = self.data_to_show[-1][2][0][1].replace(hour=0, minute=0, second=0, microsecond=0)
        ds = []
        for i in range((d2 - d1).days + 1):
            ds.append((d1 + td(i)).strftime(self.default_short_date_mask))
        self.plot.canvas.ax.vlines(x = ds,
                                   ymin = 0,
                                   ymax = 0)
        self.plot.canvas.ax.vlines(x = vlines[0],
                                   ymin = vlines[1],
                                   ymax = vlines[2],
                                   color = 'blue',
                                   linewidth = 5,
                                   alpha = 0.4)

        self.plot.canvas.draw()

    def prepare_axes(self):
        self.plot.canvas.ax.clear()
        self.plot.canvas.ax.set_ylim([7, 20])
        self.plot.canvas.ax.spines['top'].set_visible(False)
        self.plot.canvas.ax.spines['right'].set_visible(False)
        self.plot.canvas.ax.grid(color = 'grey', alpha = 0.55)

    #staticmethods
    @staticmethod
    def time_from_seconds(seconds, forplot = False):
        res = "{0}:{1}".format(int(seconds // 3600),
                               int((seconds // 60) % 60) if int((seconds // 60) % 60) >= 10
                               else "0" + str(int((seconds // 60) % 60)))
        if not forplot:
            res = res+":{0}".format(int((seconds % 3600 % 60)) if int((seconds % 3600 % 60)) >= 10
                                    else "0" + str(int((seconds % 3600 % 60))))
        return res


#app execution
def main():
    app = QApplication(sys.argv)
    window = WorkOverApp()
    window.show()
    app.exec_()


#check for target of execution
if __name__ == "__main__":
    main()
