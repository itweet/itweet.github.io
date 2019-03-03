---
title: linux-monitor
date: 2015-02-01 17:25:22
description: Linux 性能指标监控脚本。
category: Monitoring
tags: monitor
---
# cpu.pyt
```
#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'

"""
@version: 1.0
@author: whoami
@license: Apache Licence 2.0
@contact: skutil@gmail.com
@site: http://www.itweet.cn
@software: PyCharm Community Edition
@file: cpu.py
@time: 2015-11-28 下午1:51
"""
import time

def monitor(frist_invoke=1):

        interval=2

        f = open('/proc/stat')
        cpu_t1 = f.readline().split()
        f.close()

        time.sleep(interval)

        f = open('/proc/stat')
        cpu_t2 = f.readline().split()
        f.close()

        cpu_total_t1 = float(eval(('+'.join(cpu_t1)).split('cpu+')[1]))
        cpu_idle_t1 = float(cpu_t1[4])


        cpu_total_t2 = float(eval(('+'.join(cpu_t2)).split('cpu+')[1]))
        cpu_idle_t2 = float(cpu_t2[4])

        cpu_idle = cpu_idle_t2-cpu_idle_t1
        cpu_total = cpu_total_t2-cpu_total_t1

        cpu_percent = (cpu_total-cpu_idle)/cpu_total

        value_dic = {
            'cpu.user': float(cpu_t1[1])/cpu_total_t1*100,
            'cpu.nice':float(cpu_t1[2])/cpu_total_t1*100,
            'cpu.system':float(cpu_t1[3])/cpu_total_t1*100,
            'cpu.idle':float(cpu_t1[4])/cpu_total_t1*100,
            'cpu.iowait': float(cpu_t1[5])/cpu_total_t1*100,
            'cpu.irq': float(cpu_t1[6])/cpu_total_t1*100,
            'cpu.softirq': float(cpu_t1[7])/cpu_total_t1*100,
            'cpu.stealstolen':float(cpu_t1[8])/cpu_total_t1*100,
            'cpu.guest': float(cpu_t1[9])/cpu_total_t1*100,
            'cpu.percent': cpu_percent*100
        }

        return value_dic

if __name__ == '__main__':
    print monitor()
```

# disk.py
```
#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'

"""
@version: 1.0
@author: whoami
@license: Apache Licence 2.0
@contact: skutil@gmail.com
@site: http://www.itweet.cn
@software: PyCharm Community Edition
@file: disk.py
@time: 2015-11-28 下午1:53
"""
import os

def monitor(frist_invoke=1):
    value_dic = {
        'mount':{}
    }

    f = open('/etc/fstab')
    lines = f.readlines()
    f.close()

    for line in lines:
        if '#' not in line and 'ext' in line:
            mount_dir = line.split()[1]
            type = line.split()[2]

            disk = os.statvfs(mount_dir)
            capacity = float(disk.f_bsize * disk.f_blocks/(1024*1024))
            used = capacity-float(disk.f_bsize * disk.f_bfree/(1024*1024))
            available = float(disk.f_bsize * disk.f_bavail/(1024*1024))

            value_dic['mount'][mount_dir] = {
                'disk.device':mount_dir,
                'disk.capacity':capacity,
                'disk.used':used,
                'disk.available':available,
                'disk.percent': round((float(used/capacity)*100),2),
                'disk.type':type,
            }

    return value_dic

if __name__ == '__main__':
    mount = monitor()
    for m in mount['mount'].keys():
        print m,mount['mount'][m]
```

# iostats.py
```
#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'

"""
@version: 1.0
@author: whoami
@license: Apache Licence 2.0
@contact: skutil@gmail.com
@site: http://www.itweet.cn
@software: PyCharm Community Edition
@file: disk.py
@time: 2015-11-28 下午1:53
"""
import time
import global_settings

def monitor(frist_invoke=2):
    """
    Return (inbytes, outbytes, in_num, out_num, ioms) of disk.
    """
    f1 = open('/proc/diskstats')
    f2 = open('/proc/diskstats')
    content1 = f1.read()
    time.sleep(frist_invoke)
    content2 = f2.read()
    f1.close()
    f2.close()
    ds1 = {}
    for l in content1.splitlines():
        d = l.strip().split()
        if d[2].startswith('loop') or d[2].startswith('ram') or \
           d[2].startswith('dm-') or \
           d[2].startswith('fd') or d[2].startswith('sr'):
           continue
        ds1[d[2]] = [d[3], d[7], d[4], d[8], d[12]]
    ds2 = {}
    for l in content2.splitlines():
        d = l.strip().split()
        if d[2].startswith('loop') or d[2].startswith('ram') or \
           d[2].startswith('fd') or d[2].startswith('sr'):
           continue
        ds2[d[2]] = [d[3], d[7], d[4], d[8], d[12]]
    ds = {}
    for d in ds1.keys():
        rnum = float(int(ds2[d][0]) - int(ds1[d][0])) / frist_invoke
        wnum = float(int(ds2[d][1]) - int(ds1[d][1])) / frist_invoke
        blm_read = float(int(ds2[d][2]) - int(ds1[d][2])) / frist_invoke / 1024
        blm_wrtn = float(int(ds2[d][3]) - int(ds1[d][3])) / frist_invoke / 1024
        util = 100 * (float(int(ds2[d][4]) - int(ds1[d][4]))/(frist_invoke * 1000))

        ds[d] = [blm_read, blm_wrtn, rnum, wnum, util]

    for i in ds.keys():
        blm_read += round(ds.get(i)[0],2)
        blm_wrtn += round(ds.get(i)[1],2)
        rnum += round(ds.get(i)[2],2)
        wnum += round(ds.get(i)[3],2)
        util += round(ds.get(i)[4],2)

    value_dic = {
        'io.mb_read':blm_read,
        'io.mb_wrtn':blm_wrtn,
        'io.mb_read_num': rnum,
        'io.mb_wrtn_num': wnum,
        'io.ioms': util
    }

    return value_dic

if __name__ == '__main__':
    print monitor()

```

# loadavg.py
```
#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'

"""
@version: 1.0
@author: whoami
@license: Apache Licence 2.0
@contact: skutil@gmail.com
@site: http://www.itweet.cn
@software: PyCharm Community Edition
@file: loadavg.py
@time: 2015-11-28 下午1:51
"""
import os

def monitor(frist_invoke=1):
    f = open('/proc/loadavg')
    load = f.read().split()
    f.close()

    value_dic = {
        'load.1min':load[0],
        'load.5min':load[1],
        'load.15min':load[2],
    }

    return value_dic

if __name__ == '__main__':
   print monitor()

```

# meminfo.py
```
#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'

"""
@version: 1.0
@author: whoami
@license: Apache Licence 2.0
@contact: skutil@gmail.com
@site: http://www.itweet.cn
@software: PyCharm Community Edition
@file: memory.py
@time: 2015-11-28 下午1:51
"""

def monitor(frist_invoke=1):
    mem = {}

    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = long(var) / (1024.0)

    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']

    value_dic = {
        'mem.total':round(mem['MemTotal'],2),
        'mem.free':round(mem['MemFree'],2),
        'mem.buffers':round(mem['Buffers'],2),
        'mem.cache':round(mem['Cached'],2),
        'mem.used':round((mem['MemTotal'] - mem['MemFree']),2),
        'mem.percent': round((mem['MemUsed'])/(mem['MemTotal']),2)*100
    }

    return value_dic

if __name__ == '__main__':
    print monitor()
```

# netstat.py
```
#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'

"""
@version: 1.0
@author: whoami
@license: Apache Licence 2.0
@contact: skutil@gmail.com
@site: http://www.itweet.cn
@software: PyCharm Community Edition
@file: netstats.py
@time: 2015-11-28 下午2:49
"""
import time

def monitor(frist_invoke=2):
    # net rx/tx stat
    f1 = open('/proc/net/dev')
    f2 = open('/proc/net/dev')
    content1 = f1.read()
    time.sleep(frist_invoke)
    content2 = f2.read()
    f1.close()
    f2.close()

    sep = ':'
    stats1 = {}
    for line in content1.splitlines():
        if sep in line:
            i = line.split(':')[0].strip()
            data = line.split(':')[1].split()
            rx_bytes1, tx_bytes1 = (int(data[0]), int(data[8]))
            rx_pack1, tx_pack1 = (int(data[1]), int(data[9]))
            stats1[i] = [rx_bytes1, tx_bytes1, rx_pack1, tx_pack1]

    stats2 = {}
    for line in content2.splitlines():
        if sep in line:
            i = line.split(':')[0].strip()
            data = line.split(':')[1].split()
            rx_bytes2, tx_bytes2 = (int(data[0]), int(data[8]))
            rx_pack2, tx_pack2 = (int(data[1]), int(data[9]))
            stats2[i] = [rx_bytes2, tx_bytes2, rx_pack2, tx_pack2]

    value_dic = {'face':{}}

    for i in stats1.keys():
        rx_bytes_ps = (stats2[i][0] - stats1[i][0]) / frist_invoke
        tx_bytes_ps = (stats2[i][1] - stats1[i][1]) / frist_invoke
        rx_pps = (stats2[i][2] - stats1[i][2]) / frist_invoke
        tx_pps = (stats2[i][3] - stats1[i][3]) / frist_invoke

        if i.strip()!='lo':
            value_dic['face'][i] = {
                'network.nic':i,
                'network.rx_mb':rx_bytes_ps/(1024*1024),
                'network.tx_mb':tx_bytes_ps/(1024*1024),
                'network.rx_pck':rx_pps,
                'network.tx_pck':tx_pps,
            }

    return value_dic

if __name__ == '__main__':

    m = monitor()
    print m
```

# swap.py
```
#!/usr/bin/env python
# coding: utf-8
__author__ = 'whoami'

"""
@version: 1.0
@author: whoami
@license: Apache Licence 2.0
@contact: skutil@gmail.com
@site: http://www.itweet.cn
@software: PyCharm Community Edition
@file: swap.py
@time: 2015-12-03 下午3:16
"""

def monitor(frist_invoke=1):
    mem = {}
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = long(var) / (1024.0)

    value_dic = {
        'swap.total':mem['SwapTotal'],
        'swap.cached':mem['SwapCached'],
        'swap.free':mem['SwapFree'],
        'swap.used':mem['SwapTotal']-mem['SwapFree'],
    }

    return value_dic

if __name__ == '__main__':
    print monitor()
```


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/