import sys,ROOT,math

from stop2L_definitions import *

# Main function
def main():
    # Get the user input
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-p", "--process", action="store", type="string", dest="process",
                      help="process for the TF calculation (Top,WW etc.)", metavar="PROC", default="WW")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                      help="pring debug information")
    (options, args) = parser.parse_args()

    # Print the program variables
    print_userinput(options)

    # Set to batch mode bool 
    ROOT.gROOT.SetBatch(True)

    # Do the internal setup
    if options.process == "DB_DF":
        options.inputname  = "Sherpa_lvlv,Powheg_WWlvlv,Powheg_ZZllvv"  # Samples to be used
        options.grouping   = "0,1+2"                                    # Combination : first one is nominal
        options.varname    = "r1"                                       # Dummy variable
        options.regionname = "SR_DF,CR_DF"                              # 0 is SR 1 is CR
        options.luminosity = 3340.000                                   # Luminosity should cancel in the calculation
    elif options.process == "DB_SF":
        options.inputname  = "Sherpa_lvlv,Powheg_WWlvlv,Powheg_ZZllvv"  # Samples to be used
        options.grouping   = "0,1+2"                                    # Combination : first one is nominal
        options.varname    = "r1"                                       # Dummy variable
        options.regionname = "SR_SF,CR_SF"                              # 0 is SR 1 is CR
        options.luminosity = 3340.000                                   # Luminosity should cancel in the calculation
    elif options.process == "TOP_ALL":
        options.inputname  = "Powheg_ttbar,aMCatNLO_ttbar"              # Samples to be used, first one is nominal
        options.grouping   = "NONE"                                     # Combination : first one is nominal
        options.varname    = "r1"                                       # Dummy variable
        options.regionname = "SR_ALL,CR_TOP"                            # 0 is SR 1 is CR
        options.luminosity = 3340.000                                   # Luminosity should cancel in the calculation
    #elif options.process == "TOP_DF":
    #    options.inputname  = "Powheg_ttbar,aMCatNLO_ttbar"              # Samples to be used, first one is nominal
    #    options.grouping   = "NONE"                                     # Combination : first one is nominal
    #    options.varname    = "r1"                                       # Dummy variable
    #    options.regionname = "SR_DF,CR_TOP"                             # 0 is SR 1 is CR
    #    options.luminosity = 3340.000                                   # Luminosity should cancel in the calculation
    #elif options.process == "TOP_SF":
    #    options.inputname  = "Powheg_ttbar,aMCatNLO_ttbar"              # Samples to be used, first one is nominal
    #    options.grouping   = "NONE"                                     # Combination : first one is nominal
    #    options.varname    = "r1"                                       # Dummy variable
    #    options.regionname = "SR_SF,CR_TOP"                             # 0 is SR 1 is CR
    #    options.luminosity = 3340.000                                   # Luminosity should cancel in the calculation
    else:
        print("ERROR :: Unknown process %s, quitting..." %(options.process))
        return
 
    # Get ROOT files
    files=getROOTFiles(options)

    # Read the sum of weights
    sumw=getSumOfWeights(files) 

    # Fill Histograms
    histograms=fillHistograms(files,options) # [sample][region][variable]

    # Group the histograms
    inputFileList=options.inputname.split(",")
    groupList=options.grouping.split(",")
    if options.grouping == "NONE":           # Regions  = SR : 0, CR : 1                   
        groupList=inputFileList              # Variable = 0
        histogramsGrouped=histograms         # For sample i, the TF = [i][0][0]/[i][1][0]
    else:
        histogramsGrouped=groupHistograms(histograms,options)

    # Loop over samples 
    transfer_factors=[0 for x in range(len(groupList))] 
    print("")
    for ii,inputFile in enumerate(groupList):
        signal_region_unc    = ROOT.Double(0.) 
        signal_region_count  = histogramsGrouped[ii][0][0].IntegralAndError(0,-1,signal_region_unc)
        control_region_unc   = ROOT.Double(0.)
        control_region_count = histogramsGrouped[ii][1][0].IntegralAndError(0,-1,control_region_unc)
        transfer_factors[ii] = signal_region_count/control_region_count 
        #print("Sample %s \t (%.2f fb-1) SR count %.2e +/- %.2e (%3.2f%%) CR count %.2e +/- %.2e (%3.2f%%) TF is %.2e"
        print("Sample %s \t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e"
                %(groupList[ii]         ,options.luminosity*1.e-3,
                  signal_region_count   ,signal_region_unc, (signal_region_unc/signal_region_count)*100,
                  control_region_count  ,control_region_unc, (control_region_unc/control_region_count)*100,
                  transfer_factors[ii]))

    # Calculate the uncertainty
    transfer_factor_nominal     = transfer_factors[0]
    transfer_factor_uncertainty = calculate_uncertainty(transfer_factors)
    print("\nFinal transfer factor is %.2e +/- %.2e (%3.2f%%)\n"%(transfer_factor_nominal,
                                                                  transfer_factor_uncertainty,
                                                                  (transfer_factor_uncertainty/transfer_factor_nominal)*100))

# Compute the uncertainty on the transfer factor
def calculate_uncertainty(transfer_factors):
    unc=0.
    for ii in range(len(transfer_factors)):
        if ii == 0: continue # 0 is the nominal
        unc=unc+pow(transfer_factors[ii]-transfer_factors[0],2) # currently assume no correlation
    return math.sqrt(unc)

# Print user input
def print_userinput(options):
    print("=========================================================================="  )
    print(" Program : calculate_transfer_factors.py")
    print(" Author  : A.S. Mete <amete@cern.ch>")
    print(" Copyright (C) 2015 University of California, Irvine")
    print("=========================================================================="  )
    print(" Flags:\n")
    print("   Processes for the TF calculation  %s " % (options.process)                )
    print("   Print debug information           %i " % (options.debug)                  )
    print("\n==========================================================================")


if __name__ == "__main__":
    main()
