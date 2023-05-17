from termcolor import colored

def print_blue(msg):
    print(colored(msg,'blue'))

def print_yellow(msg):
    print(colored(msg,'yellow'))

def print_red(msg):
    print(colored(msg,'light_red'))

def print_green(msg):
    print(colored(msg,'light_green'))

def get_blue(msg):
    return colored(msg,'blue')

def get_yellow(msg):
    return colored(msg,'yellow')

def get_red(msg):
    return colored(msg,'light_red')

def get_green(msg):
    return colored(msg,'light_green')

def check_for_error(instrument,print_error=False):
    err = instrument.query("SYST:ERR?")
    if '+0,"No error"' not in err:
        if print_error:
            print_red(err)
        return True
    else:
        if print_error:
            print_green('\nDevice has no errors.')
        return False

def toggle_preset(instrument):
    instrument.write("SYST:FPR")
    instrument.write("DISP:WIND1:STATE ON")
    return

if __name__ == '__main__':
    msg = 'TESTING'
    print_blue(msg)
    print_yellow(msg)
    print_red(msg)
    print_green(msg)

