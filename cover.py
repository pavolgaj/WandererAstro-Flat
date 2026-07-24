#!/usr/bin/env python3

import sys, os
import tkinter as tk
from tkinter import messagebox, ttk
import serial
import glob
import time

baud=19200

def do_open(port):
    """Handle the 'open' action."""
    result = "opening..."
    
    try: ser = serial.Serial(port,baud,bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.5,)
    except: return
    time.sleep(2)
    ser.write(b'1001')
    ser.flush() 
    time.sleep(2)
    ser.close()
    
    print(result)
    
    time.sleep(20)   
    
    return do_status(port)


def do_close(port):
    """Handle the 'close' action."""
    result = "closing..."
    
    try: ser = serial.Serial(port,baud,bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.5,)
    except: return
    time.sleep(2)
    ser.write(b'1000')
    ser.flush() 
    time.sleep(2)
    ser.close()
    
    print(result)
    
    time.sleep(20)   
    
    return do_status(port)


def do_status(port):
    """Handle the 'status' action."""
    try: ser = serial.Serial(port,baud,bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.5,)
    except: return
    result=ser.readline()
    ser.close()
    
    #b'WandererCoverV4A20250703A20.00A170.00A18.24A4.91A0A0A0A\r\n'
    dat=result.split(b'A')
    
    close0=float(dat[2])
    open0=float(dat[3])
    pos=float(dat[4])
    
    if abs(pos-close0)<10: result='closed'
    elif abs(pos-open0)<10: result='opened'
    else: result='error'    
    
    #result = f"Status: OK"
    print(result)
    return result


def execute(action,port):
    """Dispatch actions."""
    actions = {
        "open": do_open,
        "close": do_close,
        "status": do_status,
    }

    if action not in actions:
        raise ValueError(
            f"Unknown action '{action}'. "
            f"Valid actions: {', '.join(actions)}"
        )

    return actions[action](port)


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def run_gui():
    root = tk.Tk()
    root.title("Telescope Cover")
    
    # Width x Height
    root.geometry("300x100")

    # Prevent resizing
    root.resizable(False, False)

    # Label and input on the same row
    tk.Label(root, text="Port:").grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky="w",
    )
    
    f=open('port.txt','r')
    port=f.readlines()[0].strip()
    f.close()
    
    ports=serial_ports()
    if not port in ports: port=''

    target_var = tk.StringVar(value=port)

    target_select = ttk.Combobox(
        root,
        textvariable=target_var,
        values=ports,
        state="readonly",   # remove this if you also want manual typing
    )

    target_select.grid(
        row=0,
        column=1,
        columnspan=3,
        padx=5,
        pady=5,
        sticky="ew",
    )

    def button_action(action):
        port = target_var.get().strip()
        
        f=open('port.txt','w')
        f.write(port+'\n')
        f.close()

        try:
            result = execute(action, port)
            messagebox.showinfo("Result", result)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    tk.Button(
        root, width=7,
        text="Open",
        command=lambda: button_action("open"),
    ).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(
        root, width=7,
        text="Close",
        command=lambda: button_action("close"),
    ).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(
        root, width=7,
        text="Status",
        command=lambda: button_action("status"),
    ).grid(row=1, column=2, padx=5, pady=5)

    root.mainloop()


def run_cli():
    """
    Usage:
        script.py open [target]
        script.py close [target]
        script.py status [target]
    """
    action = sys.argv[1]
    
    f=open('port.txt','r')
    port=f.readlines()[0].strip()
    f.close()
    
    port = sys.argv[2] if len(sys.argv) > 2 else port
    
    f=open('port.txt','w')
    f.write(port+'\n')
    f.close()
    
    if not action in ['open','close','status']:
        print("Usage:\npython cover.py open (port)\npython cover.py close (port)\npython cover.py status (port)\n")
        sys.exit(1)
    
    try:
        execute(action,port)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("\nUsage:\npython cover.py open (port)\npython cover.py close (port)\npython cover.py status (port)\n")
        sys.exit(1)

if not os.path.isfile('port.txt'): 
    f=open('port.txt','w')
    f.write('\n')
    f.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_gui()
    else:
        run_cli()
        
