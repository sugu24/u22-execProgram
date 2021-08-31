import subprocess
import threading
import sys
import time

file_name = "a"+sys.argv.pop(-1)
save_dir = "/home/suguru/llvm-project/tempFile/"
gd_name = file_name + ".gd"
ll_name = file_name + ".ll"
txt_name = file_name + '.txt'
prog = sys.argv[1]

subprocess.Popen(['touch', '{}'.format(save_dir+gd_name)])
with open('{}'.format(save_dir+gd_name), 'w') as fp:
    fp.write(prog)

subprocess.Popen(['touch', '{}'.format(save_dir+txt_name)])
with open('{}'.format(save_dir+txt_name), 'a') as fp:
    for arg in sys.argv[2:]:
        fp.write(arg)

debug = subprocess.Popen(['/home/suguru/llvm-project/bin/dcc', '{}'.format(save_dir+gd_name),'-o', '{}'.format(save_dir+ll_name)], encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
timer = threading.Timer(1, debug.kill)
try:
    start = time.time()
    timer.start()
    debug_out, debug_error = debug.communicate()
finally:
    end = time.time() - start
    timer.cancel()
    if end > 1:
        print("debug_error")
        exit()

if len(debug_error) != 0:
    subprocess.Popen(['rm', '{}'.format(save_dir+gd_name), '{}'.format(save_dir+txt_name), '{}'.format(save_dir+ll_name)])
    print(debug_error)
else:
    with open('{}'.format(save_dir+txt_name), 'r') as fp:
        execute = subprocess.Popen(['/usr/local/llvm/bin/lli', '{}'.format(save_dir+ll_name)], encoding='utf8', stdin=fp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = threading.Timer(0.2, execute.kill)
    try:
        start = time.time()
        timer.start()
        stdout, stderr = execute.communicate()
    finally:
        end = time.time() - start
        timer.cancel()
        if end > 0.2:
            subprocess.Popen(['rm','{}'.format(save_dir+gd_name), '{}'.format(save_dir+txt_name), '{}'.format(save_dir+ll_name)])
            print("実行時間が長すぎます。ループ回数が大きい可能性があります。")
            exit()
    
    subprocess.Popen(['rm','{}'.format(save_dir+gd_name), '{}'.format(save_dir+txt_name), '{}'.format(save_dir+ll_name)])
    if len(stdout) <= 1000:
        print(stdout)
    else:
        print("実行結果が長すぎるため、送信できません")
