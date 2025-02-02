from .tool.func import *

def api_recent_edit_request(db_set, num = 1, set_type = 'normal', limit = 50):
    with get_db_connect() as conn:
        other_set = {}
        other_set["num"] = str(num)
        other_set["limit"] = str(limit)
        other_set["set_type"] = set_type
        other_set["ip"] = ip_check()
        other_set = json.dumps(other_set)

        if platform.system() == 'Linux':
            if platform.machine() in ["AMD64", "x86_64"]:
                data = subprocess.Popen([os.path.join(".", "route_go", "bin", "main.amd64.bin"), sys._getframe().f_code.co_name, db_set, other_set], stdout = subprocess.PIPE).communicate()[0]
            else:
                data = subprocess.Popen([os.path.join(".", "route_go", "bin", "main.arm64.bin"), sys._getframe().f_code.co_name, db_set, other_set], stdout = subprocess.PIPE).communicate()[0]
        else:
            if platform.machine() in ["AMD64", "x86_64"]:
                data = subprocess.Popen([os.path.join(".", "route_go", "bin", "main.amd64.exe"), sys._getframe().f_code.co_name, db_set, other_set], stdout = subprocess.PIPE).communicate()[0]
            else:
                data = subprocess.Popen([os.path.join(".", "route_go", "bin", "main.arm64.exe"), sys._getframe().f_code.co_name, db_set, other_set], stdout = subprocess.PIPE).communicate()[0]

        data = data.decode('utf8')

        return flask.Response(response = data, status = 200, mimetype = 'application/json')