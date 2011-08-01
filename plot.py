#!/usr/bin/python
# wentong@taobao.com
# 11-1-21
#

NAME = 0
DONE = 1
FAILED = 2
RT = 3

def load_log(file_name):
    import re
    import datetime

    log_file = open(file_name)
    pattern = re.compile(r'<(.*?)>')
    times = []
    records = {}
    totals = []
    while True:
        line = log_file.readline()
        if line == "":
            break
        elems = line.split()
        if len(elems) >= 4:
            total = 0
            time = datetime.datetime.strptime(elems[0] + " " + elems[1].split(",")[0], "%Y-%m-%d %H:%M:%S")
            times.append(time)

            match = pattern.findall(elems[3])
            once_record={}
            for record in map(lambda x:x.split("|"), match):
                name = record[NAME]
                done = record[DONE]
                failed = record[FAILED]
                rt = record[RT]
                if not once_record.has_key(name):
                    once_record[name] = [[], [], [], []]
                once_record[name][0].append(int(done))
                once_record[name][1].append(int(failed))
                total_count = int(done) + int(failed)
                once_record[name][2].append(total_count)
                once_record[name][3].append(float(rt))
            for record_key in once_record.keys():
                if not records.has_key(record_key):
                    records[record_key] = [[], [], [], []]
                records[record_key][0].append(reduce(lambda a,b:a+b,once_record[record_key][0]))
                records[record_key][1].append(reduce(lambda a,b:a+b,once_record[record_key][1]))
                total_count = reduce(lambda a, b:a + b, once_record[record_key][2])
                records[record_key][2].append(total_count)
                total+=total_count
                if total_count > 0:
                    records[record_key][3].append(reduce(lambda a, b:a + b, once_record[record_key][3])/total_count*1000)
                else:
                    records[record_key][3].append(0)
            totals.append(total)
    log_file.close()
    return times, records, totals

def do_plot(x_axis, y_axis,title,xlabel,ylable):
    import pylab,setting
    pylab.plot_date(x_axis, y_axis, linestyle='dashed')
    pylab.xlabel(xlabel)
    pylab.ylabel(ylable)
    pylab.title(title)
    pylab.grid(True)
    if setting.PIC_SAVE_PATH_AND_PREFIX:
        title__png_ = setting.PIC_SAVE_PATH_AND_PREFIX + title + ".png"
        pylab.savefig(title__png_)
        print "draw:",title__png_
        pylab.figure()
    else:
        pylab.show()


def draw(times, records ,totals):
    import pylab
    if len(times) > 0 and len(records.keys()) > 0:
        x_axis = pylab.array(times)
        pylab.xlabel('time')

        for key in records.keys():
            done = records[key][0]
            y_axis = pylab.array(done)
            do_plot(x_axis,y_axis,key + " done QPS",'time',"QPS")

            failed = records[key][1]
            y_axis = pylab.array(failed)
            do_plot(x_axis,y_axis,key + " failed QPS",'time',"QPS")

            total = records[key][2]
            y_axis = pylab.array(total)
            do_plot(x_axis,y_axis,key + " total QPS",'time',"QPS")

            rt = records[key][3]
            y_axis = pylab.array(rt)
            do_plot(x_axis,y_axis,key + " response time",'time',"RT(ms)")

        do_plot(x_axis,pylab.array(totals), "Total QPS",'time',"QPS")



if __name__ == "__main__":
    import setting
    times, records,totals = load_log(setting.LOG_PATH_AND_FILE_NAME)
    draw(times, records,totals)

  