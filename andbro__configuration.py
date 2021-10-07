#!/usr/bin/python
#
# class for configurations
#
# by AndBro @2021
# __________________________



class configuration():
    
    def __init__(self):

        self.name="configurations"
        
        self.event = None
        
        self.tbeg = None
        self.tend = None
        
        self.filter = None
        self.filter_type = None
        self.filter_fmax = None
        self.filter_fmin = None
        self.fcorner = None

        
    def get_filter_settings(self):

        self.filter = input("Apply filter (y/n): ") or None

        if self.filter is None or self.filter == '': 
            self.filter = False
        else:
            self.filter = True
            self.filter_type = input("Apply lowpass (lp), highpass (hp) or bandpass (bp)?: ")

            if self.filter_type in ['bp', 'bandpass']:
                self.filter_type = 'bandpass'
                self.filter_fmin = float(input("Enter lower corner frequency (in Hz): ")) or None
                self.filter_fmax = float(input("Enter upper corner frequency (in Hz): ")) or None
            elif self.filter_type in ['hp', 'highpass']:
                self.filter_type = 'highpass'
                self.filter_fmin = float(input("Enter corner frequency (in Hz): ")) or None
            elif self.filter_type in ['lp', 'lowpass']:
                self.filter_type = 'lowpass'
                self.filter_fmax = float(input("Enter corner frequency (in Hz): ")) or None

    def check(self):

        if self.filter and self.filter_type == 'bandpass':
            if self.filter_fmax < self.filter_fmin:
                print(f"-> ERROR: lower frequency: {self.filter_fmin} Hz must be smaller than upper frequency {self.filter_fmax} Hz!")
                return False
        else:
            return
  
## END OF FILE
