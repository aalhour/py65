import re

class AddressParser:
    """Parse user input into addresses or ranges of addresses.
    """

    def __init__(self, radix=16, labels={}):
        """Radix is the default radix to use when one is not specified
        as a prefix of any input.  Labels are a dictionary of label
        names that can be substituted for addresses.
        """
        self.radix = radix
        self.labels = labels

    def number(self, num):
        """Parse a string containing a label or number into an address.
        """
        if num.startswith('$'):
            return int(num[1:], 16)

        elif num.startswith('+'):
            return int(num[1:], 10)

        elif num.startswith('%'):
            return int(num[1:], 2)

        elif num in self.labels:
            return self.labels[num]
      
        else:
            matches = re.match('^([^\s+-]+)\s*([+\-])\s*([$+%]?\d+)$', num)
            if matches:
                label, sign, offset = matches.groups()

                if label not in self.labels:
                    raise KeyError("Label not found: %s" % label)

                base = self.labels[label]
                offset = self.number(offset)

                if sign == '+':
                    address = base + offset
                else:
                    address = base - offset

                if address < 0:
                    address = 0
                if address > 0xFFFF:
                    address = 0xFFFF
                return address

            else:
                try:
                    return int(num, self.radix)
                except ValueError:
                    raise KeyError("Label not found: %s" % num)

    def range(self, addresses):
        """Parse a string containing an address or a range of addresses
        into a tuple of (start address, end address)
        """
        matches = re.match('^([^:,]+)\s*[:,]+\s*([^:,]+)$', addresses)
        if matches:
            start, end = map(self.number, matches.groups(0))
        else:
            start = end = self.number(addresses)

        if start > end:
            start, end = end, start            
        return (start, end)

  
def itoa(num, base=10):
    """ Convert a decimal number to its equivalent in another base.
    This is essentially the inverse of int(num, base).
    """
    negative = num < 0
    if negative:
      num = -num
    digits = []
    while num > 0:
      num, last_digit = divmod(num, base)
      digits.append('0123456789abcdefghijklmnopqrstuvwxyz'[last_digit])
    if negative:
      digits.append('-')
    digits.reverse()
    return ''.join(digits) 

def convert_to_bin(bcd):
    return bcd2bin[bcd]

def convert_to_bcd(bin):
    return bin2bcd[bin]

bcd2bin = [
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,  # 0x00
   10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  # 0x10
   20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,  # 0x20
   30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,  # 0x30
   40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,  # 0x40
   50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,  # 0x50
   60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75,  # 0x60
   70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85,  # 0x70
   80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,  # 0x80
   90, 91, 92, 93, 94, 95, 96, 97, 98, 99,100,101,102,103,104,105,  # 0x90
  100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,  # 0xA0
  110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,  # 0xB0
  120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,  # 0xC0
  130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,  # 0xD0
  140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,  # 0xE0
  150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165   # 0xF0
]

bin2bcd = [
  0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,
  0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,
  0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,
  0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,
  0x40,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,
  0x50,0x51,0x52,0x53,0x54,0x55,0x56,0x57,0x58,0x59,
  0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69,
  0x70,0x71,0x72,0x73,0x74,0x75,0x76,0x77,0x78,0x79,
  0x80,0x81,0x82,0x83,0x84,0x85,0x86,0x87,0x88,0x89,
  0x90,0x91,0x92,0x93,0x94,0x95,0x96,0x97,0x98,0x99
]
