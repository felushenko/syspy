import psutil
import time
import curses 
import platform
import cpuinfo
from psutil._common import bytes2human



greetings = f"""
{platform.platform()}
{platform.architecture()}
{platform.node()}
{platform.processor()}


1. OS and CPU resource usage statistics
2. RAM and SWAP usage statistics
3. Disk usage statistics
4. Information about network cards and their connections"""

def main():
    print(greetings)
             
    category = input("Select a category: ")

    try:
        category = int(category)  
        if 1 <= category <= 4:
            if category == 1:
                curses.wrapper(cpu_info)
            if category == 2:
                curses.wrapper(memory_info)
            if category == 3:
                curses.wrapper(net_info)
            if category == 4:
                pass
            if category == 5:
                pass
                
        else:
            print("Введено число, но оно не находится в диапазоне от 1 до 4.")
    except ValueError:
        print("Введенное значение не является числом.")

def cpu_info(stdscr):
    curses.curs_set(0)
    curses.update_lines_cols()
    stdscr.clear()

    try:
        cpu_info = cpuinfo.get_cpu_info()
        while True:
            
            curses.update_lines_cols()
            stdscr.clear()
            cpu_times_user = psutil.cpu_times().user
            cpu_times_system = psutil.cpu_times().system
            cpu_times_idle = psutil.cpu_times().idle

            cpu_percent = psutil.cpu_percent()
            cpu_count_logical = psutil.cpu_count(logical=False)
            cpu_count_physical = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            stdscr.addstr(0, 0, cpu_info['brand_raw'])
            stdscr.addstr(1, 0, cpu_info['vendor_id_raw'])
            stdscr.addstr(2, 0, f"L2 cache size: {cpu_info['l2_cache_size']}")
            stdscr.addstr(3, 0, f"L3 cache size: {cpu_info['l3_cache_size']}")
            stdscr.addstr(4, 0, f"Model: {cpu_info['model']}")
            stdscr.addstr(5, 0, f"Family: {cpu_info['family']}")
            stdscr.addstr(6, 0, f"Stepping: {cpu_info['stepping']}")

            stdscr.addstr(8, 0, f"System processor operating time:")
            stdscr.addstr(9, 3, f"Time spent by normal processes: {format_time(cpu_times_user)}")
            stdscr.addstr(10, 3, f"time spent by processes running in kernel mode: {format_time(cpu_times_system)}")
            stdscr.addstr(11, 3, f"time spent idle: {format_time(cpu_times_idle)}")

            stdscr.addstr(13, 0, f"Current CPU load: {cpu_percent}%")
            stdscr.addstr(14, 0, f"Number of logical and physical processors: {cpu_count_logical} / {cpu_count_physical}")
            stdscr.addstr(15, 0, f"CPU frequency: {cpu_freq}")
            stdscr.refresh()
            

            time.sleep(1)

            
                


    except KeyboardInterrupt:
        pass

def memory_info(stdscr):
    curses.curs_set(0) 
    stdscr.clear()

    try:
        while True:
            
            virtual_memory_total =psutil.virtual_memory().total
            virtual_memory_percent =psutil.virtual_memory().percent
            virtual_memory_used =psutil.virtual_memory().used
            virtual_memory_free =psutil.virtual_memory().free
            virtual_memory_available =psutil.virtual_memory().available

            swap_memory_total = psutil.swap_memory().total
            swap_memory_used = psutil.swap_memory().used 
            swap_memory_free = psutil.swap_memory().free
            swap_memory_percent = psutil.swap_memory().percent 
            swap_memory_sin = psutil.swap_memory().sin 
            swap_memory_sout = psutil.swap_memory().sout 

            disk = psutil.disk_partitions()

            stdscr.addstr(0, 0, f"[+] Virtual memory")
            stdscr.addstr(1, 2, f"Total physical memory:{bytes2human(virtual_memory_total)}")
            stdscr.addstr(2, 2, f"Memory usage percentage:{virtual_memory_percent}%")
            stdscr.addstr(3, 2, f"Used memory:{bytes2human(virtual_memory_used)}")
            stdscr.addstr(4, 2, f"Free memory:{bytes2human(virtual_memory_free)}")
            stdscr.addstr(5, 2, f"Available memory for processes:{bytes2human(virtual_memory_available)}")

            stdscr.addstr(7, 0, f"[+] System swap file")
            stdscr.addstr(8, 2, f"Total paging file size:{bytes2human(swap_memory_total)}")
            stdscr.addstr(9, 2, f"Paging file size used:{bytes2human(swap_memory_used)}")
            stdscr.addstr(10, 2, f"Free size:{bytes2human(swap_memory_free)}")
            stdscr.addstr(11, 2, f"Fill percentage:{swap_memory_percent}%")
            stdscr.addstr(12, 2, f"Number of bytes written to disk:{bytes2human(swap_memory_sin)}")
            stdscr.addstr(13, 2, f"Number of bytes read from disk:{bytes2human(swap_memory_sout)}")

            disk_info = []
            for part in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    disk_info.append([
                        part.device,
                        bytes2human(usage.total),
                        bytes2human(usage.used),
                        bytes2human(usage.free),
                        int(usage.percent),
                        part.fstype,
                    ])
                except PermissionError:
                    disk_info.append([
                        part.device,
                        "N/A",
                        "N/A",
                        "N/A",
                        "N/A",
                        "N/A",
                    ])         

            stdscr.addstr(15, 0, "[+] Disk Information")
            stdscr.addstr(17, 10, "Device")
            stdscr.addstr(17, 20, "Total")
            stdscr.addstr(17, 30, "Used")
            stdscr.addstr(17, 40, "Free")
            stdscr.addstr(17, 50, "Use %")
            stdscr.addstr(17, 60, "Type")

            for i, disk in enumerate(disk_info, start=18):
                for j, info in enumerate(disk, start=1):
                    stdscr.addstr(i, 10 * j, str(info))

            stdscr.refresh()
            time.sleep(1)

    except KeyboardInterrupt:
        pass

def net_info(stdscr):
    curses.curs_set(0) 
    stdscr.clear()

    try:
        while True:
            
            net_info = psutil.net_if_addrs()
            net_info_name = net_info.keys()

            stdscr.addstr(0, 50, f"Netwok")
            stdscr.addstr(1, 0, f"[+] Network interface card (NIC)")
            

            stdscr.refresh()
            time.sleep(1)

    except KeyboardInterrupt:
        pass

def format_time(total_seconds):

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{int(days)}day {int(hours)}hour {int(minutes)}min {int(seconds)}sec"


if __name__ == "__main__":
    main()
