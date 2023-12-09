# from talon import cron, actions
import platform, os, subprocess, json

os_type = platform.system()
# Get the architecture (32-bit or 64-bit)
arch, _ = platform.architecture()

current_directory = os.path.dirname(os.path.abspath(__file__))
bin_directory = os.path.join(current_directory, 'bin')
match os_type, arch:
    case 'Linux', '64bit':
        log_path = os.path.join(bin_directory, 'log_parser_linux_amd64')
    case 'Linux', '32bit':
        log_path = os.path.join(bin_directory, 'log_parser_linux_386')
    case 'Windows', '64bit':
        log_path = os.path.join(bin_directory, 'log_parser_windows_amd64.exe')
    case 'Windows', '32bit':
        log_path = os.path.join(bin_directory, 'log_parser_windows_386.exe')
    case 'Darwin', '64bit':
        log_path = os.path.join(bin_directory, 'log_parser_macos_amd64')
    
cache = dict.fromkeys(["last_io_line", "last_debug_line", "last_warning_line", 
                       "first_error_line", "last_error_line"], 
                    "")

def check_log_updates():
    output = subprocess.Popen(log_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = output.communicate()
    jsonOutput = json.loads(stdout)
    for key in cache:
        cache[key] = jsonOutput[key]


    