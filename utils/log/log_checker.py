import platform, os, subprocess, json
try:
    from talon import cron, actions, Module
except:
    pass

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
    
log_cache = dict.fromkeys(["last_io_line", "last_debug_line", "last_warning_line", 
                       "first_error_line", "last_error_line"], 
                    "")

updated = False

def get_log_updates() -> dict[str, str]:
    output = subprocess.Popen(log_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    stdout, _ = output.communicate()
    jsonOutput = json.loads(stdout)
    updated_values = {}
    global updated
    updated = False
    for key in log_cache:
        if jsonOutput.get(key) != log_cache[key]:
            updated = True
            log_cache[key] = jsonOutput[key]
            updated_values[key] = jsonOutput[key]
        log_cache[key] = jsonOutput[key]
    return updated_values
    
def updates_as_dict(updated_vals: dict[str, str]):
    key_to_label = {
        "last_io_line": "IO",
        "last_debug_line": "Debug",
        "last_warning_line": "Warning",
        "first_error_line": "Start Error",
        "last_error_line": "Last Error"
    }

    output = {}
    for key, value in updated_vals.items():
        label = key_to_label.get(key)
        if label:
            output[label] = value

    return output



mod = Module()
@mod.action_class
class Actions:
    def echo_last_error():
        """Echo the last error"""
        get_log_updates()
        actions.user.tts(log_cache.get("last_error_line"))

    def echo_last_warning():
        """Echo the last warning"""
        get_log_updates()
        actions.user.tts(log_cache.get("last_warning_line"))

    def echo_last_debug():
        """Echo the last debug"""
        get_log_updates()
        actions.user.tts(log_cache.get("last_debug_line"))

    def echo_last_print():
        """Echo the last IO"""
        get_log_updates()
        actions.user.tts(log_cache.get("last_io_line"))


# updated_vals = get_log_updates()
# output = updates_as_dict(updated_vals)
#     # if updated:
# actions.user.tts(json.dumps(output))