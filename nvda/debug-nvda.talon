os: windows
-

test reader add on:
    user.send_ipc_commands("debug")

test controller client:
    user.test_controller_client()
