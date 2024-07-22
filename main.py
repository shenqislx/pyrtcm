from sys import argv
from pyrtcm import RTCMReader, parse_msm


def conv_msm_cell_sig(sys, cell_sig):
    sig = "NULL"
    if sys == "GPS":
        if cell_sig == "1C":
            sig = "L1_CA"
        elif cell_sig == "1P":
            sig = "L1_P"
        elif cell_sig == "1W":
            sig = "L1_W"
        elif cell_sig == "2C":
            sig = "L2_CA"
        elif cell_sig == "2P":
            sig = "L2_P"
        elif cell_sig == "2W":
            sig = "L2_W"
        elif cell_sig == "2S":
            sig = "L2C_M"
        elif cell_sig == "2L":
            sig = "L2C_L"
        elif cell_sig == "2X":
            sig = "L2C_ML"
        elif cell_sig == "5I":
            sig = "L5_I"
        elif cell_sig == "5Q":
            sig = "L5_Q"
        elif cell_sig == "5X":
            sig = "L5_IQ"

    return sig


def main(**kwargs):
    infile = kwargs.get("infile", "./examples/rtcmntrip.log")
    with open(infile, "rb") as stream:
        rtr = RTCMReader(stream)
        for _, parsed in rtr:
            if parsed is not None:
                try:
                    msmarray = parse_msm(parsed)
                    if msmarray is not None:
                        #print(msmarray)
                        sys = msmarray[0]["gnss"]
                        print(f'MSG: {msmarray[0]["identity"]} EPOCH: {msmarray[0]["epoch"]} SYS: {sys} NSAT: {msmarray[0]["sats"]} NCELL: {msmarray[0]["cells"]} STATION: {msmarray[0]["station"]}')
                        #for sat in msmarray[1]:  # satellite data array
                            #print(f'PRN {sat["PRN"]}')
                        prn = "-1"
                        for cell in msmarray[2]:
                            if prn != cell["CELLPRN"]:
                                if prn != "-1":
                                    print()
                                prn = cell["CELLPRN"]
                                print(f'PRN: {prn}', end='')
                            print(f', SIG: {cell["CELLSIG"]}', end='')
                        print()
                except KeyError:
                    pass  # unimplemented message type


if __name__ == "__main__":
    main(**dict(arg.split("=") for arg in argv[1:]))
