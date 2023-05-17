import pyvisa
import support_functions as sf
import time

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
#  
#   ██╗   ██╗███████╗███████╗██████╗     ██████╗  █████╗ ██████╗  █████╗ ███╗   ███╗███████╗████████╗███████╗██████╗ ███████╗   
#   ██║   ██║██╔════╝██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗ ████║██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝  ██╗
#   ██║   ██║███████╗█████╗  ██████╔╝    ██████╔╝███████║██████╔╝███████║██╔████╔██║█████╗     ██║   █████╗  ██████╔╝███████╗  ╚═╝
#   ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝     ██║   ██╔══╝  ██╔══██╗╚════██║  ██╗
#   ╚██████╔╝███████║███████╗██║  ██║    ██║     ██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║███████╗   ██║   ███████╗██║  ██║███████║  ╚═╝
#    ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝      
# 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
addr = 'TCPIP0::Owner-Desktop::hislip3,4880::INSTR' # Device VISA address
VNA_model = 'N5231B'

low_freq = 300e6    # 300 kHz
upper_freq = 6e9    # 6 GHz

s_params_list = ['11','12','21','22'] # List of S-Parameters to measure:

reset_to_instrument_preset = True # True = Set instrument to preset before running script. False = Do not go to preset.

manual_step_size = False # True = Manually set step size. False = Let VNA set step size.
step_freq = 1e6     # 1 MHz step size

file_path_save_csv = r'C:/Users/Owner/Documents/KeysightVNA_Challenge/S_parameter_data/'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# END OF USER PARAMETERS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

print('\nAttemping to connect to: '+sf.get_yellow(addr))

# Opening VISA resource manager:
rm = pyvisa.ResourceManager()

# Connect to equipment at my address 'addr' above
VNA = rm.open_resource(addr)

# Check what the device at this VISA address responds as:
resp = VNA.query('*IDN?')

if VNA_model in resp:
    sf.print_green('Successfully connected to Keysight VNA simulator!\n')
else:
    sf.print_red('Unable to connect to Keysight VNA simulator! Check that correct VNA model is chosen.\n')

# SCPI automation:
if reset_to_instrument_preset:
    sf.toggle_preset(VNA)

for s_param in s_params_list:
    idx = str(s_params_list.index(s_param)+1)
    
    # Step 1: Set active trace and assign ref_name as the S_param
    VNA.write("CALC:PAR:DEF:EXT 'S"+s_param+"',S"+s_param)
    VNA.write("DISP:WIND1:TRAC"+idx+":FEED 'S"+s_param+"'")

    # Step 2: Set frequency stimulus correctly:
    VNA.write("SENS1:FREQ:STAR "+str(low_freq))
    VNA.write("SENS1:FREQ:STOP "+str(upper_freq))
    if manual_step_size:
        VNA.write("SENS1:FREQ:CENT:STEP:SIZE "+str(step_freq))

    # Step 3: Set scale:
    VNA.write("DISP:WIND:Y:AUTO") # Won't do much in 4x iteration loop

    # Step 4: Trigger single shot capture:
    VNA.write("SENS:SWE:MODE SING")
    time.sleep(0.1) 

    # Step 5: Save data as CSV
    VNA.write('MMEMory:STORe:DATA "'+file_path_save_csv+'S'+s_param+'_data.csv","CSV Formatted Data","displayed","RI",-1')
    sf.print_green('Saved S'+s_param+' data as CSV.')

# Step 6: After for loop, toggle as continuous
VNA.write("SENS:SWE:MODE CONT")
time.sleep(1)
VNA.write("DISP:WIND:Y:AUTO")

err = sf.check_for_error(VNA,print_error=1)