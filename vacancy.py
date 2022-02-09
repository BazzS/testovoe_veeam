import subprocess,shlex
import psutil
import platform
import time
import csv


def get_user_info():

    """Получает путь до файла и время интервала"""

    file_path = str(input('Enter file path:'))
    time_interval = int(input('Enter time interval:'))
    return file_path,time_interval

def get_process_data(file_path,time_interval):

    """Запускаем файл и собираемся статистику данного процесса"""

    file_path_call_command = f'python3 {file_path}'
    start_proc = subprocess.call(file_path_call_command, shell=True)
    proc = psutil.Process(start_proc)
    proc.cpu_percent()
    check_time = time.strftime("%m-%d-%Y_%H-%M-%S",time.gmtime(proc.create_time()))
    name_file_data = f'{file_path}_{check_time}.csv'
    metrics_result = ["Resident set size","Virtual memory size","File descriptors","Loading CPU"]
    save_metrics_in_file(metrics_result,name_file_data)


    if platform.system() == "Linux" or "Darwin":
        while True:
            try:
                resident_set_size = proc.memory_info()[0]
                virtual_memory_size = proc.memory_info()[1]
                file_descriptors = proc.num_fds()
                loading_cpu = round(proc.cpu_percent()/psutil.cpu_count())
                metrics_result = [resident_set_size,virtual_memory_size,file_descriptors,loading_cpu]
                save_metrics_in_file(metrics_result,name_file_data)
                print("Linux system")
                time.sleep(time_interval)
            except (psutil.NoSuchProcess, psutil.AccessDenied) as Exc:
                print(Exc)
                break
    elif platform.system() == "Windows":
        working_set = proc.memory_info()[0]
        private_bytes = proc.memory_info()[-1]
        number_of_handles = proc.num_handles()
        loading_cpu = round(proc.cpu_percent()/psutil.cpu_count())
        print("Windows system")
    else:
        pass

def save_metrics_in_file(data,data_file):

    """Сохранением данных в файл"""

    with open(data_file,'a') as table:
        writer = csv.writer(table)
        writer.writerow(data)

if __name__ == '__main__':
    get_process_data(*get_user_info())
