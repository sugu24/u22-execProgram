import subprocess
import threading
import time
save_dir = "/home/suguru/llvm-project/tempFile/"
txt_name = "aaBfDqC8IP9D.txt"
ll_name = "aaBfDqC8IP9D.ll"
gd_name = "aaBfDqC8IP9D.gd"
with open('{}'.format(save_dir+txt_name), 'r') as fp:
    execute = subprocess.Popen(['lli', '{}'.format(save_dir+ll_name)], encoding='utf-8', stdin=fp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
timer = threading.Timer(2, execute.kill)
try:
    start = time.time()
    timer.start()
    stdout, stderr = execute.communicate()
finally:
    end = time.time() - start
    timer.cancel()
    if end > 2:
        subprocess.Popen(['rm','{}'.format(+gd_name), '{}'.format(save_dir+txt_name), '{}'.format(save_dir+ll_name)])
        print("実行時間が長すぎます。無限ループか入力待ちになっている可能性があります。")
        exit()

    subprocess.Popen(['rm','{}'.format(save_dir+gd_name), '{}'.format(save_dir+txt_name), '{}'.format(save_dir+ll_name)])
    print(stdout)
