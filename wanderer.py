#! /usr/bin/env python3

import sys, os
import serial
import glob
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox 
import time


DEBUG=False

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

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("700x420")
        top.resizable(0, 0)
        top.title("Wanderer Cover Settings")

        self.top = top

        self.firmware = tk.StringVar()
        self.openPos = tk.StringVar()
        self.closePos = tk.StringVar()
        self.curPos = tk.StringVar()
        self.volt = tk.StringVar()
        self.flatVal = tk.StringVar()
        self.dew = tk.StringVar()
        self.asiair = tk.StringVar()
        self.openSet = tk.StringVar()
        self.closeSet = tk.StringVar()
        self.flat = tk.StringVar()

        ports=serial_ports()
        f=open('port.txt','r')
        port=f.readlines()[0].strip()
        f.close()
        if not port in ports: port=''

        self.port = tk.StringVar(value=port)


        self.lbl_port = tk.Label(self.top, text="Port")
        self.lbl_port.place(relx=0.03, rely=0.025)

        self.cmb_port = ttk.Combobox(self.top,state="readonly",values=ports,textvariable=self.port)
        self.cmb_port.place(relx=0.09, rely=0.02, relwidth=0.2, height=28)

        self.btn_connect = tk.Button(self.top,text="Connect",command=self.connect,width=10)
        self.btn_connect.place(relx=0.32, rely=0.02, width=80, height=30)

        self.btn_disconnect = tk.Button(self.top,text="Disconnect",command=self.disconnect, width=10, state=tk.DISABLED)
        self.btn_disconnect.place(relx=0.44, rely=0.02, width=80, height=30)


        self.btn_open_cover = tk.Button(self.top,text="Open Cover",command=self.openCover, state=tk.DISABLED)
        self.btn_open_cover.place(relx=0.6,rely=0.025,width=120,height=30)


        self.btn_close_cover = tk.Button(self.top,text="Close Cover",command=self.closeCover, state=tk.DISABLED)
        self.btn_close_cover.place(relx=0.8,rely=0.025,width=120,height=30)


        self.frm_current = tk.LabelFrame(self.top,text="Current values",padx=5,pady=5)
        self.frm_current.place(relx=0.03,rely=0.12,relwidth=0.45,relheight=0.85)

        self.frm_config = tk.LabelFrame(self.top,text="Configuration",padx=5,pady=5)
        self.frm_config.place( relx=0.51,rely=0.12,relwidth=0.46,relheight=0.4)

        self.frm_flat = tk.LabelFrame(self.top,text="Flat panel",padx=5,pady=5)
        self.frm_flat.place(relx=0.51,rely=0.55,relwidth=0.46,relheight=0.2)

        self.frm_dew = tk.LabelFrame(self.top,text="Dew heater",padx=5,pady=5)
        self.frm_dew.place(relx=0.51,rely=0.77,relwidth=0.46,relheight=0.2)

        #############
        # current values
        #############
        self.lbl_firmware = tk.Label(self.frm_current, text="Firmware")
        self.lbl_firmware.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.ent_firmware = tk.Entry(self.frm_current,state="readonly",textvariable=self.firmware)
        self.ent_firmware.grid(row=0, column=1, sticky="ew", padx=10, pady=5)


        self.lbl_open_position = tk.Label(self.frm_current, text="Open Position")
        self.lbl_open_position.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.ent_open_position = tk.Entry(self.frm_current,state="readonly", textvariable=self.openPos)
        self.ent_open_position.grid(row=1, column=1, sticky="ew", padx=10, pady=5)


        self.lbl_close_position = tk.Label(self.frm_current, text="Close Position")
        self.lbl_close_position.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.ent_close_position = tk.Entry(self.frm_current,state="readonly", textvariable=self.closePos)
        self.ent_close_position.grid(row=2, column=1, sticky="ew", padx=10, pady=5)


        self.lbl_current_position = tk.Label(self.frm_current, text="Current Position")
        self.lbl_current_position.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.ent_current_position = tk.Entry(self.frm_current,state="readonly", textvariable=self.curPos)
        self.ent_current_position.grid(row=3, column=1, sticky="ew", padx=10, pady=5)


        self.lbl_voltage = tk.Label(self.frm_current, text="Input Voltage")
        self.lbl_voltage.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.ent_voltage = tk.Entry(self.frm_current,state="readonly",textvariable=self.volt)
        self.ent_voltage.grid(row=4, column=1, sticky="ew", padx=10, pady=5)


        self.lbl_flat = tk.Label(self.frm_current, text="Flat panel")
        self.lbl_flat.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        self.ent_flat = tk.Entry(self.frm_current,state="readonly",textvariable=self.flatVal)
        self.ent_flat.grid(row=5, column=1, sticky="ew", padx=10, pady=5)


        self.lbl_dew = tk.Label(self.frm_current, text="Dew heater")
        self.lbl_dew.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        self.ent_dew = tk.Entry(self.frm_current,state="readonly",textvariable=self.dew)
        self.ent_dew.grid(row=6, column=1, sticky="ew", padx=10, pady=5)


        self.lbl_asiair = tk.Label(self.frm_current, text="AsiAir")
        self.lbl_asiair.grid(row=7, column=0, sticky="w", padx=10, pady=5)

        self.ent_asiair = tk.Entry(self.frm_current,state="readonly",textvariable=self.asiair)
        self.ent_asiair.grid(row=7, column=1, sticky="ew", padx=10, pady=5)


        self.btn_get_values = tk.Button(self.frm_current,text="Get",command=self.readVal, state=tk.DISABLED)
        self.btn_get_values.grid(row=8,column=1,pady=10)

        # Make the entry column expand
        self.frm_current.columnconfigure(1, weight=1)

        ############
        # set positions
        ############
        self.lbl_open_set = tk.Label(self.frm_config,text="Open Position")
        self.lbl_open_set.grid(row=0,column=0,sticky="w",padx=10,pady=10)

        self.spn_open_set = tk.Spinbox(self.frm_config,from_=0.0,to=360.0, textvariable=self.openSet, state=tk.DISABLED)
        self.spn_open_set.grid(row=0,column=1,sticky="ew",padx=10,pady=10)

        self.lbl_close_set = tk.Label(self.frm_config,text="Close Position")
        self.lbl_close_set.grid(row=1,column=0,sticky="w",padx=10,pady=10)

        self.spn_close_set = tk.Spinbox(self.frm_config,from_=0.0,to=299.9, textvariable=self.closeSet, state=tk.DISABLED)
        self.spn_close_set.grid(row=1,column=1,sticky="ew",padx=10,pady=10)

        self.btn_set_config = tk.Button(self.frm_config,text="Set",command=self.setConfig, state=tk.DISABLED)
        self.btn_set_config.grid(row=2,column=1,pady=10)

        # allow spinboxes to expand
        self.frm_config.columnconfigure(1, weight=1)

        ############
        # flat panel
        ############
        self.spn_flat_level = tk.Spinbox(self.frm_flat,from_=1.0,to=255.0, textvariable=self.flat, state=tk.DISABLED)
        self.spn_flat_level.grid(row=0,column=0,padx=10,pady=10)

        self.btn_set_flat = tk.Button(self.frm_flat,text="Set",command=self.flatSet, state=tk.DISABLED)
        self.btn_set_flat.grid(row=0,column=1,padx=15,pady=10)

        self.btn_flat_off = tk.Button(self.frm_flat,text="OFF",command=self.flatOFF, state=tk.DISABLED)
        self.btn_flat_off.grid(row=0,column=2,padx=15,pady=10)

        self.frm_flat.columnconfigure(0, weight=1)

        #########
        # dew heater
        ##########
        self.btn_dew_off = tk.Button(self.frm_dew,text="OFF",command=self.dewOff, state=tk.DISABLED)
        self.btn_dew_off.grid(row=0,column=0,padx=8,pady=10)

        self.btn_dew_low = tk.Button(self.frm_dew,text="LOW",command=self.dewLow, state=tk.DISABLED)
        self.btn_dew_low.grid(row=0,column=1,padx=8,pady=10)

        self.btn_dew_high = tk.Button(self.frm_dew,text="HIGH",command=self.dewHigh, state=tk.DISABLED)
        self.btn_dew_high.grid(row=0,column=2,padx=8,pady=10)

        self.btn_dew_max = tk.Button(self.frm_dew,text="MAX",command=self.dewMax,state=tk.DISABLED)
        self.btn_dew_max.grid(row=0,column=3,padx=8,pady=10)

        # make buttons spread evenly
        for i in range(4):
            self.frm_dew.columnconfigure(i, weight=1)


    def sendCommand(self,command):
        if DEBUG:
            print(command)
            return
        
        time.sleep(0.1)
        self.cover.write(command)
        self.cover.flush()
        time.sleep(0.1)

    def openCover(self):
        command=1001
        self.sendCommand(command)


    def closeCover(self):
        command=1000
        self.sendCommand(command)


    def dewOff(self):
        command=2000
        self.sendCommand(command)


    def dewLow(self):
        command=2050
        self.sendCommand(command)

    def dewHigh(self):
        command=2100
        self.sendCommand(command)

    def dewMax(self):
        command=2150
        self.sendCommand(command)


    def flatOFF(self):
        command=9999
        self.sendCommand(command)

    def flatSet(self):
        try: flat=float(self.flat.get())
        except ValueError:
            messagebox.showerror('Flat panel','Incorrect value!')
            return
        
        if flat>255 or flat<0:
            messagebox.showerror('Flat panel','Value out of range!')
            return
        
        if flat==0: 
            self.flatOFF()
            return
        
        command=int(flat)
        self.sendCommand(command)

    def setConfig(self):        
        try:
            openpos=float(self.openSet.get())
            closepos=float(self.closeSet.get())
        except ValueError:
            messagebox.showerror('Cover position','Incorrect value!')
            return
        
        if openpos>360 or openpos<0:
            messagebox.showerror('Cover position','Value out of range!')
            return
        
        if closepos>=300 or closepos<0:
            messagebox.showerror('Cover position','Value out of range!')
            return
            
        
        if openpos<closepos:
            #open<Close
            messagebox.showerror('Cover position','Value for open position is lower than close position!')
            return
        
        command=int(40000+openpos*100)
        self.sendCommand(command)
        
        time.sleep(1)
        
        command=int(10000+closepos*100)
        self.sendCommand(command)

    def readVal(self):
        #b'WandererCoverV4A20250703A20.00A170.00A18.24A4.91A0A0A0A\r\n'
        if DEBUG: 
            result=b'WandererCoverV4A20250703A20.00A170.00A18.24A4.91A0A0A0A\r\n'
            print(result)
        else: 
            result=self.cover.readline()
            #print(result)
        dat=result.split(b'A')

        self.firmware.set(int(dat[1]))
        self.closePos.set(float(dat[2]))
        self.openPos.set(float(dat[3]))
        self.curPos.set(float(dat[4]))
        self.volt.set(float(dat[5]))
        self.flatVal.set(int(dat[6]))
        self.dew.set(int(dat[7]))
        self.asiair.set(int(dat[8]))



    def disconnect(self):
        if not DEBUG: 
            self.cover.close()
            port = self.port.get().strip()
        
            f=open('port.txt','w')
            f.write(port+'\n')
            f.close()
            
        #disable buttons
        self.btn_disconnect.config(state=tk.DISABLED)
        self.btn_open_cover.config(state=tk.DISABLED)
        self.btn_close_cover.config(state=tk.DISABLED)
        self.btn_get_values.config(state=tk.DISABLED)
        self.btn_set_config.config(state=tk.DISABLED)
        self.btn_set_flat.config(state=tk.DISABLED)
        self.btn_flat_off.config(state=tk.DISABLED)
        self.btn_dew_off.config(state=tk.DISABLED)
        self.btn_dew_low.config(state=tk.DISABLED)
        self.btn_dew_high.config(state=tk.DISABLED)
        self.btn_dew_max.config(state=tk.DISABLED)

        self.spn_open_set.config(state=tk.DISABLED)
        self.spn_close_set.config(state=tk.DISABLED)
        self.spn_flat_level.config(state=tk.DISABLED)


    def connect(self):
        port=self.port.get()
        if (not len(port)==-1) or DEBUG:
            if not DEBUG:
                try:
                    self.cover=serial.Serial(
                        port=port,
                        baudrate=19200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.5,
                    )
                except: return

            try: self.readVal()
            except: return
            
            #default values
            self.openSet.set(self.openPos.get())
            self.closeSet.set(self.closePos.get())
            self.flat.set(self.flatVal.get())
            
            #enable buttons
            self.btn_disconnect.config(state=tk.NORMAL)
            self.btn_open_cover.config(state=tk.NORMAL)
            self.btn_close_cover.config(state=tk.NORMAL)
            self.btn_get_values.config(state=tk.NORMAL)
            self.btn_set_config.config(state=tk.NORMAL)
            self.btn_set_flat.config(state=tk.NORMAL)
            self.btn_flat_off.config(state=tk.NORMAL)
            self.btn_dew_off.config(state=tk.NORMAL)
            self.btn_dew_low.config(state=tk.NORMAL)
            self.btn_dew_high.config(state=tk.NORMAL)
            self.btn_dew_max.config(state=tk.NORMAL)

            self.spn_open_set.config(state=tk.NORMAL)
            self.spn_close_set.config(state=tk.NORMAL)
            self.spn_flat_level.config(state=tk.NORMAL)


    def on_closing(self):
        try:
            self.disconnect()
            time.sleep(1)
        except: pass
        root.destroy()


if not os.path.isfile('port.txt'):
    f=open('port.txt','w')
    f.write('\n')
    f.close()

if __name__ == '__main__':
    '''Main entry point for the application.'''
    global root
    
    if len(sys.argv)>1:
        if sys.argv[1].lower()=='debug': DEBUG=True
    
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = Toplevel1(_top1)
    root.protocol("WM_DELETE_WINDOW", _w1.on_closing)
    root.mainloop()




