def Calculation(AxisValues, joystick_que, OldAxisValues, magazyn):
    try:    # Right Joystick
        if int(magazyn.clients_table[magazyn.wybor_HUV].parameter_magazyn[5]) == 1:
            Krokowy_calculation(AxisValues, joystick_que, OldAxisValues)
        elif int(magazyn.clients_table[magazyn.wybor_HUV].parameter_magazyn[5]) == 0:
            Thruster_calculation(AxisValues, joystick_que, OldAxisValues)
    except:
        pass
    try:    # Left Joystick
        if OldAxisValues[1] != AxisValues[1]:
            Command = str("{}:{:>2}:{:>2}".format(20, AxisValues[1], AxisValues[1]))
            joystick_que.put(Command)
    except:
        pass


def Krokowy_calculation(AxisValues, joystick_que, OldAxisValues):
    if OldAxisValues[3] != AxisValues[3]:
        Command = str("{}:{:>2}:{:>2}".format(20 + 2, 8*AxisValues[3], 8*AxisValues[3]))
        joystick_que.put(Command)


def Thruster_calculation(AxisValues, joystick_que, OldAxisValues):
    if OldAxisValues[2] != AxisValues[2] or OldAxisValues[3] != AxisValues[3]:
        if AxisValues[3] == 0 and AxisValues[2] == 0:
            valueleft = 0
            valueright = 0
            Command = str("{}:{:>2}:{:>2}".format(20 + 1, valueleft, valueright))
            joystick_que.put(Command)
        elif AxisValues[2] >= 0 and AxisValues[3] <= 0:  # prawy przód
            valueleft = AxisValues[2] - AxisValues[3]
            if valueleft > 100:
                valueleft = 100
            valueright = -AxisValues[2] - AxisValues[3]
            Command = str("{}:{:>2}:{:>2}".format(20 + 1, -valueleft, -valueright))
            joystick_que.put(Command)
        elif AxisValues[2] <= 0 and AxisValues[3] <= 0:  # lewy przód
            valueleft = -AxisValues[3] + AxisValues[2]
            valueright = -AxisValues[3] - AxisValues[2]
            if valueright > 100:
                valueright = 100
            Command = str("{}:{:>2}:{:>2}".format(20 + 1, -valueleft, -valueright))
            joystick_que.put(Command)
        elif AxisValues[2] <= 0 and AxisValues[3] >= 0:
            valueleft = AxisValues[3] + AxisValues[2]
            valueright = AxisValues[3]
            Command = str("{}:{:>2}:{:>2}".format(20 + 1, valueleft, valueright))
            joystick_que.put(Command)
        elif AxisValues[2] >= 0 and AxisValues[3] >= 0:
            valueleft = AxisValues[3]
            valueright = AxisValues[3] - AxisValues[2]
            Command = str("{}:{:>2}:{:>2}".format(20 + 1, valueleft, valueright))
            joystick_que.put(Command)