
def wrap_response_data(ret, msg='', **data):
    if ret == 0:
        data["ret"] = 0
        data["msg"] = "Normal operation."

    elif ret == 1:
        data["ret"] = 1
        data["msg"] = "User is not logged in."

    elif ret == 2:
        data["ret"] = 2
        data["msg"] = "Administrator is not logged in."

    elif ret == 3:
        data["ret"] = 3
        if msg.__len__() == 0:
            data["msg"] = "OE, you need to contact with backend group."
        else:
            data["msg"] = msg

    return data
