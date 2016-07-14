#!/usr/bin/env python
import sys,math,array
from ROOT import *
from rootUtil import waitRootCmd, get_default_fig_dir, useAtlasStyle

from plot_definitions import *

sDir = get_default_fig_dir()
sTag = 'r1_SF_'

# Compute the uncertainty on the transfer factor
def calculate_uncertainty(transfer_factors):
    unc=0.
    for ii in range(len(transfer_factors)):
        if ii == 0: continue # 0 is the nominal
        unc=unc+pow(transfer_factors[ii]-transfer_factors[0],2) # currently assume no correlation
    return math.sqrt(unc)

class tfIput:
    def __init__(self):
        self.inputname  = ['Sherpa_ggllll','Sherpa_ggllll_fac4,Sherpa_ggllll_fac025','Sherpa_ggllll_renorm4,Sherpa_ggllll_renorm025','Sherpa_ggllll_qsf4,Sherpa_ggllll_qsf025']
        self.grouping   = "NONE"                                     # Combination : first one is nominal
        self.varname    = "r1"                                       # Dummy variable
        self.regionname = "EW2L_SR_SF_mT2_90,EW2L_CR_SF"                              # 0 is SR 1 is CR
        self.luminosity = 3210.000                                   # Luminosity should cancel in the calculation

class tfCalculator:
    def __init__(self):
        pass
    def checkTF(self, options):
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
            signal_region_unc       = ROOT.Double(0.) 
            signal_region_count     = histogramsGrouped[ii][0][0].IntegralAndError(0,-1,signal_region_unc)
            signal_region_unc_perc  = (signal_region_unc/signal_region_count)*100 if signal_region_unc !=0 else 0. 
            control_region_unc      = ROOT.Double(0.)
            control_region_count    = histogramsGrouped[ii][1][0].IntegralAndError(0,-1,control_region_unc)
            control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.
            transfer_factors[ii] = signal_region_count/control_region_count 
            if groupList[ii] != "Powheg_ttbar_radHi" and groupList[ii] != "Powheg_ttbar_radLo":       
                print("Sample %s \t\t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e"
                    %(groupList[ii]         ,options.luminosity*1.e-3,
                          signal_region_count   ,signal_region_unc, signal_region_unc_perc, 
                          control_region_count  ,control_region_unc, control_region_unc_perc,
                          transfer_factors[ii]))
            else:
                print("Sample %s \t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e"
                    %(groupList[ii]         ,options.luminosity*1.e-3,
                          signal_region_count   ,signal_region_unc, signal_region_unc_perc, 
                          control_region_count  ,control_region_unc, control_region_unc_perc,
                          transfer_factors[ii]))

        # Calculate the uncertainty
        transfer_factor_nominal     = transfer_factors[0]
        transfer_factor_uncertainty = calculate_uncertainty(transfer_factors)
        print("\nFinal transfer factor is %.2e +/- %.2e (%3.2f%%)\n"%(transfer_factor_nominal,
                                                                      transfer_factor_uncertainty,
                                                                      (transfer_factor_uncertainty/transfer_factor_nominal)*100))

def getSumOfWeights(files):
    sumw=[0 for x in range(len(files))]
    for ii,iiFile in enumerate(files):
        for f in glob.glob(iiFile):
            f1 = ROOT.TFile(f,'read')
            sumw[ii] += f1.Get("CutflowWeighted").GetBinContent(1)
    return sumw

def fillHistograms(files,options):
    inputFileList=options.inputname.split(",")
    variableList=options.varname.split(",") 
    regionList=options.regionname.split(",")

    # Read the sum of weights
    sumw=getSumOfWeights(files) 

    histograms=[[[0 for x in range(len(variableList))] for x in range(len(regionList))] for x in range(len(inputFileList))]

    for ii,inputFile in enumerate(inputFileList):
        # Find the tree 
        currentROOTTree = ROOT.TChain('SuperTruth')
        currentROOTTree.Add(files[ii])

        # Loop over regions 
        for jj,region in enumerate(regionList):
            # Get the TCut for the region 
            cut=getRegionTCut(region)
            if(options.debug): 
                print("INFO :: Retrieving information for region %s" % region)
                print("INFO :: Applying cut %s"%cut)
            # Loop over variables
            for kk,variable in enumerate(variableList):
                # Create the histogram
                histoName=("histo_%i_%i_%i"%(ii,jj,kk))
                # Get the bin information 
                binInfo=getBinInformation(variable.split("[")[0])
                if len(binInfo)==1:
                    histograms[ii][jj][kk]=ROOT.TH1D(histoName,histoName,len(binInfo[0])-1,array.array("d",binInfo[0]))
                elif len(binInfo)==3:
                    histograms[ii][jj][kk]=ROOT.TH1D(histoName,histoName,binInfo[0],binInfo[1],binInfo[2])
                histograms[ii][jj][kk].Sumw2()
                if(options.debug): 
                    print("INFO :: Retrieving information for variable %s" % variable)
                # Fill the histograms
                if variable == "lepton_n"      : variable = "@lepton_pt.size()"
                elif variable == "jet_n"       : variable = "@jet_pt.size()"
                elif variable == "bjet_n"      : variable = "@bjet_pt.size()"
                elif variable == "nonbjet_n"   : variable = "@nonbjet_pt.size()"
                elif variable == "c_bjet_n"    : variable = "@c_bjet_pt.size()"
                elif variable == "c_nonbjet_n" : variable = "@c_nonbjet_pt.size()"
                if(options.debug):
                    print("INFO :: Cross-section %.2f - Luminosity %.2f - Sumw %.2f"%(getCrossSection(inputFile),options.luminosity,sumw[ii]))
                if "MadgraphM" in inputFile:
                    selection=("(mcEventWeight*mcPolWeight_M*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                elif "MadgraphR" in inputFile:
                    selection=("(mcEventWeight*mcPolWeight_R*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                elif ("MadgraphL" in inputFile) or ("TakashiL" in inputFile):
                    selection=("(mcEventWeight*mcPolWeight_L*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                else:
                    selection=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                if options.debug:
                    print("INFO :: Selection is %s" % selection)
                currentROOTTree.Draw(variable+">>"+histoName,selection,"goff")                                

    return histograms


def files2Histogram(ftag, TH1F):
    pass

class oo1:
    pass
#     def __init__(self):
#         self.process = "DB_DF"
#         self.inputname  = "Sherpa_llvv,Sherpa_llvv_fac4,Sherpa_llvv_fac025,Sherpa_llvv_renorm4,Sherpa_llvv_renorm025,Sherpa_llvv_qsf4,Sherpa_llvv_qsf025,Sherpa_llvv_ckkw15,Sherpa_llvv_ckkw30"
#         self.grouping   = "NONE"                         # Combination : first one is nominal
#         self.varname    = "mT2ll"                                       # Dummy variable
#         self.regionname = "EW2L_SR_DF,EW2L_CR_DF"        #               # 0 is SR 1 is CR
#         self.luminosity = 3210.000
#         pass

def test():
    # start with the easist: compare the TF of two samples
    ## Make two histograms from the two TChain
    ## make cuts and get the TF
    options = oo1()
    options.process = "DB_DF"
    options.inputname  = "Sherpa_llvv,Sherpa_llvv_fac4,Sherpa_llvv_fac025,Sherpa_llvv_renorm4,Sherpa_llvv_renorm025,Sherpa_llvv_qsf4,Sherpa_llvv_qsf025,Sherpa_llvv_ckkw15,Sherpa_llvv_ckkw30"
    options.grouping   = "NONE"                         # Combination : first one is nominal
    options.varname    = "mT2ll"                                       # Dummy variable
    options.regionname = "EW2L_SR_DF,EW2L_CR_DF"        #               # 0 is SR 1 is CR
    options.luminosity = 3210.000
   
    files=getROOTFiles(options)
    h1s = fillHistograms(options)


def getSumWeight(iiFile):
    sumw = 0.
    for f in glob.glob(iiFile):
        f1 = ROOT.TFile(f,'read')
        sumw += f1.Get("CutflowWeighted").GetBinContent(1)
    return sumw

def test1():
    ## get TF for one sample
    #1 get nevents
    sTag = 'aMcAtNloHerwigpp_Wt'
    files = getROOTFileName(sTag)
    sumw = getSumWeight(files)

    options = oo1()
    options.process = "DB_DF"
    options.inputname  = "Sherpa_llvv,Sherpa_llvv_fac4,Sherpa_llvv_fac025,Sherpa_llvv_renorm4,Sherpa_llvv_renorm025,Sherpa_llvv_qsf4,Sherpa_llvv_qsf025,Sherpa_llvv_ckkw15,Sherpa_llvv_ckkw30"
    options.grouping   = "NONE"                         # Combination : first one is nominal
    options.varname    = "mT2ll"                                       # Dummy variable
    options.regionname = "EW2L_SR_DF,EW2L_CR_DF"        #               # 0 is SR 1 is CR
    options.luminosity = 3210.000
 
    ch1 = TChain('SuperTruth')
    ch1.Add(files)
    var1 = 'mT2ll'

    histoName = 'h1'
    histograms = TH1D(histoName, histoName+';mT_{2}(ll) [GeV];Events / 5 GeV',40,0,200)

    cut = 'mll>20'
    selection=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(sTag),options.luminosity,sumw,cut))
    ch1.Draw(var1+">>"+histoName, selection, 'goff')

    histograms.Draw()

    control_region_unc      = ROOT.Double(0.)
    control_region_count    = histograms.IntegralAndError(0,-1,control_region_unc)
    control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.

    for slow in [90, 120, 150]:
        bin0 = histograms.GetXaxis().FindBin(slow)
        print slow, bin0, histograms.GetXaxis().GetBinLowEdge(bin0)
        signal_region_unc       = ROOT.Double(0.) 
        signal_region_count     = histograms.IntegralAndError(bin0,-1,signal_region_unc)
        signal_region_unc_perc  = (signal_region_unc/signal_region_count)*100 if signal_region_unc !=0 else 0. 

        transfer_factors = signal_region_count/control_region_count 
        print("Sample %s \t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e"
            %(sTag         ,options.luminosity*1.e-3,
                  signal_region_count   ,signal_region_unc, signal_region_unc_perc, 
                  control_region_count  ,control_region_unc, control_region_unc_perc,
                  transfer_factors))

    waitRootCmd()

def tag2Hitos(sTag, regions, wt='', luminosity=10000.):
    files = getROOTFileName(sTag)
    sumw = getSumWeight(files)

    ch1 = TChain('SuperTruth')
    ch1.Add(files)
    var1 = 'mT2ll'

    histoName = 'h_'+sTag+'_'+wt
    histoName.replace('[','_').replace(']','')
    histoName0 = histoName+regions[0]
    histoName1 = histoName+regions[1]

    histogram0 = TH1D(histoName0, histoName+';mT_{2}(ll) [GeV];Events / 5 GeV',40,0,200)
    histogram1 = histogram0.Clone(histoName1) 

    cut0=getRegionTCut(regions[0])
    cut1=getRegionTCut(regions[1])

    print sTag 
    selection0=("(mcEventWeight"+wt+"*%f*%f/%f)*(%s)"%(getCrossSection(sTag),luminosity,sumw,cut0))
    ch1.Draw(var1+">>"+histoName0, selection0, 'goff')

    selection1=("(mcEventWeight"+wt+"*%f*%f/%f)*(%s)"%(getCrossSection(sTag),luminosity,sumw,cut1))
    ch1.Draw(var1+">>"+histoName1, selection1, 'goff')

    return (histogram0, histogram1)

def get_DF_SF_More(options, mT2CutList=[90, 120, 150], showPlot=False):
    sTag = options.inputname
    regions = options.regionname.split(',') 

    th = None
    for s in options.inputname.split(','):
#         print s
        kk = tag2Hitos(s, regions)
        if not th: th = kk
        else:
            for i in range(len(kk)):
                th[i].Add(kk[i])
    (histogram0, histogram1) = th

    control_region_unc      = ROOT.Double(0.)
    control_region_count    = histogram0.IntegralAndError(0,-1,control_region_unc)
    control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.

    results = [(control_region_count, control_region_unc_perc)]
    for slow in mT2CutList:
        bin0 = histogram1.GetXaxis().FindBin(slow)
#         print slow, bin0, histogram1.GetXaxis().GetBinLowEdge(bin0)
        signal_region_unc       = ROOT.Double(0.) 
        signal_region_count     = histogram1.IntegralAndError(bin0,-1,signal_region_unc)
        signal_region_unc_perc  = (signal_region_unc/signal_region_count)*100 if signal_region_unc !=0 else 0. 

        transfer_factors = signal_region_count/control_region_count 
        tf_unc = math.sqrt(signal_region_unc_perc*signal_region_unc_perc+control_region_unc_perc*control_region_unc_perc)
        print("Sample %s \t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e (%3.2f%%)" 
            %(sTag         ,options.luminosity*1.e-3,
                  signal_region_count   ,signal_region_unc, signal_region_unc_perc, 
                  control_region_count  ,control_region_unc, control_region_unc_perc,
                  transfer_factors, tf_unc))
        results.append((signal_region_count, signal_region_unc_perc, transfer_factors, tf_unc))

    if showPlot:
        histogram0.Draw()
        histogram1.SetLineColor(2)
        histogram1.SetLineStyle(2)
        histogram1.Draw("histsame")
        waitRootCmd()
    return results,th

def get_DF_SF_More_wt(options, mT2CutList=[90, 120, 150], showPlot=False, wt=''):
    sTag = options.inputname
    regions = options.regionname.split(',') 

    th = None
    for s in options.inputname.split(','):
#         print s
        kk = tag2Hitos(s, regions, wt)
        if not th: th = kk
        else:
            for i in range(len(kk)):
                th[i].Add(kk[i])
    (histogram0, histogram1) = th

    control_region_unc      = ROOT.Double(0.)
    control_region_count    = histogram0.IntegralAndError(0,-1,control_region_unc)
    control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.

    results = [(control_region_count, control_region_unc_perc)]
    for slow in mT2CutList:
        bin0 = histogram1.GetXaxis().FindBin(slow)
#         print slow, bin0, histogram1.GetXaxis().GetBinLowEdge(bin0)
        signal_region_unc       = ROOT.Double(0.) 
        signal_region_count     = histogram1.IntegralAndError(bin0,-1,signal_region_unc)
        signal_region_unc_perc  = (signal_region_unc/signal_region_count)*100 if signal_region_unc !=0 else 0. 

        transfer_factors = signal_region_count/control_region_count 
        tf_unc = math.sqrt(signal_region_unc_perc*signal_region_unc_perc+control_region_unc_perc*control_region_unc_perc)
        print("Sample %s \t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e (%3.2f%%)" 
            %(sTag         ,options.luminosity*1.e-3,
                  signal_region_count   ,signal_region_unc, signal_region_unc_perc, 
                  control_region_count  ,control_region_unc, control_region_unc_perc,
                  transfer_factors, tf_unc))
        results.append((signal_region_count, signal_region_unc_perc, transfer_factors, tf_unc))

    if showPlot:
        histogram0.Draw()
        histogram1.SetLineColor(2)
        histogram1.SetLineStyle(2)
        histogram1.Draw("histsame")
        waitRootCmd()
    return results,th


def get_DF_SF_wt(options, mT2CutList=[90, 120, 150], showPlot=False, wt=''):
    sTag = options.inputname
    regions = options.regionname.split(',') 

    files = getROOTFileName(sTag)
    sumw = getSumWeight(files)

    ch1 = TChain('SuperTruth')
    ch1.Add(files)
    var1 = 'mT2ll'

    histoName = 'h1'
    histoName0 = histoName+regions[0]
    histoName1 = histoName+regions[1]

    histogram0 = TH1D(histoName0, histoName+';mT_{2}(ll) [GeV];Events / 5 GeV',40,0,200)
    histogram1 = histogram0.Clone(histoName1) 

    cut0=getRegionTCut(regions[0])
    cut1=getRegionTCut(regions[1])

    
    selection0=("(mcEventWeight*"+wt+"%f*%f/%f)*(%s)"%(getCrossSection(sTag),options.luminosity,sumw,cut0))
    ch1.Draw(var1+">>"+histoName0, selection0, 'goff')

    selection1=("(mcEventWeight*"+wt+"%f*%f/%f)*(%s)"%(getCrossSection(sTag),options.luminosity,sumw,cut1))
    ch1.Draw(var1+">>"+histoName1, selection1, 'goff')


    control_region_unc      = ROOT.Double(0.)
    control_region_count    = histogram0.IntegralAndError(0,-1,control_region_unc)
    control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.

    results = [(control_region_count, control_region_unc_perc)]
    for slow in mT2CutList:
        bin0 = histogram1.GetXaxis().FindBin(slow)
#         print slow, bin0, histogram1.GetXaxis().GetBinLowEdge(bin0)
        signal_region_unc       = ROOT.Double(0.) 
        signal_region_count     = histogram1.IntegralAndError(bin0,-1,signal_region_unc)
        signal_region_unc_perc  = (signal_region_unc/signal_region_count)*100 if signal_region_unc !=0 else 0. 

        transfer_factors = signal_region_count/control_region_count 
        tf_unc = math.sqrt(signal_region_unc_perc*signal_region_unc_perc+control_region_unc_perc*control_region_unc_perc)
        print("Sample %s \t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e (%3.2f%%)" 
            %(sTag         ,options.luminosity*1.e-3,
                  signal_region_count   ,signal_region_unc, signal_region_unc_perc, 
                  control_region_count  ,control_region_unc, control_region_unc_perc,
                  transfer_factors, tf_unc))
        results.append((signal_region_count, signal_region_unc_perc, transfer_factors, tf_unc))

    if showPlot:
        histogram0.Draw()
        histogram1.SetLineColor(2)
        histogram1.SetLineStyle(2)
        histogram1.Draw("histsame")
        waitRootCmd()
    return results


def get_DF_SF(options, mT2CutList=[90, 120, 150], showPlot=False):
    sTag = options.inputname
    regions = options.regionname.split(',') 

    files = getROOTFileName(sTag)
    sumw = getSumWeight(files)

    ch1 = TChain('SuperTruth')
    ch1.Add(files)
    var1 = 'mT2ll'

    histoName = 'h1'
    histoName0 = histoName+regions[0]
    histoName1 = histoName+regions[1]

    histogram0 = TH1D(histoName0, histoName+';mT_{2}(ll) [GeV];Events / 5 GeV',40,0,200)
    histogram1 = histogram0.Clone(histoName1) 

    cut0=getRegionTCut(regions[0])
    cut1=getRegionTCut(regions[1])

    
    selection0=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(sTag),options.luminosity,sumw,cut0))
    ch1.Draw(var1+">>"+histoName0, selection0, 'goff')

    selection1=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(sTag),options.luminosity,sumw,cut1))
    ch1.Draw(var1+">>"+histoName1, selection1, 'goff')


    control_region_unc      = ROOT.Double(0.)
    control_region_count    = histogram0.IntegralAndError(0,-1,control_region_unc)
    control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.

    results = [(control_region_count, control_region_unc_perc)]
    for slow in mT2CutList:
        bin0 = histogram1.GetXaxis().FindBin(slow)
#         print slow, bin0, histogram1.GetXaxis().GetBinLowEdge(bin0)
        signal_region_unc       = ROOT.Double(0.) 
        signal_region_count     = histogram1.IntegralAndError(bin0,-1,signal_region_unc)
        signal_region_unc_perc  = (signal_region_unc/signal_region_count)*100 if signal_region_unc !=0 else 0. 

        transfer_factors = signal_region_count/control_region_count 
        tf_unc = math.sqrt(signal_region_unc_perc*signal_region_unc_perc+control_region_unc_perc*control_region_unc_perc)
        print("Sample %s \t (%.2f fb-1) SR count %.2f +/- %.2f (%3.2f%%) CR count %.2f +/- %.2f (%3.2f%%) TF is %.2e (%3.2f%%)" 
            %(sTag         ,options.luminosity*1.e-3,
                  signal_region_count   ,signal_region_unc, signal_region_unc_perc, 
                  control_region_count  ,control_region_unc, control_region_unc_perc,
                  transfer_factors, tf_unc))
        results.append((signal_region_count, signal_region_unc_perc, transfer_factors, tf_unc))

    if showPlot:
        histogram0.Draw()
        histogram1.SetLineColor(2)
        histogram1.SetLineStyle(2)
        histogram1.Draw("histsame")
        waitRootCmd()
    return results

def checkVary(r0_df, vary, opoints):
    options = oo1()
    options.varname    = "mT2ll"                                       # Dummy variable
#     options.regionname = "EW2L_CR_DF,EW2L_SR_DF"        #               # 0 is SR 1 is CR
    options.regionname = "EW2L_CR_SF,EW2L_SR_SF"        #               # 0 is SR 1 is CR
    options.luminosity = 10000.
    funcname = 'pol2'
    mtb = range(60,200,10)

    if not r0_df:
        options.inputname  = vary[1][2]
        r0_df = get_DF_SF(options, mtb)
    options.inputname = vary[2][2]
    r1_df = get_DF_SF(options, mtb)
    options.inputname = vary[3][2]
    r2_df = get_DF_SF(options, mtb)

    shift = 0.5
    g0 = TGraphErrors()
    g1 = TGraphErrors()
    g2 = TGraphErrors()
    for i in range(len(r1_df)-1):
        g0.SetPoint(i, mtb[i], 0)
        g0.SetPointError(i, 0, r0_df[i+1][3])
        g1.SetPoint(i, mtb[i]+shift, (r1_df[i+1][2]-r0_df[i+1][2])/r0_df[i+1][2]*100)
        g1.SetPointError(i, 0, r1_df[i+1][3])
        g2.SetPoint(i, mtb[i]-shift, (r2_df[i+1][2]-r0_df[i+1][2])/r0_df[i+1][2]*100)
        g2.SetPointError(i, 0, r2_df[i+1][3])

    lg = TLegend(0.2, 0.7, 0.4, 0.9)
    lg.SetFillStyle(0)

    g0.SetMarkerSize(0.01)
    g0.Draw("ALP")
    g0.GetXaxis().SetTitle(getXtitle(options.varname))
    g0.GetYaxis().SetTitle('Uncertainty [%]')
    g1.SetMarkerColor(2)
    g1.SetLineColor(2)
    g1.SetMarkerStyle(23)
    g1.Draw('sameP')
    checkFit(g1.Fit(funcname, 'S'))
    fun1 = g1.GetFunction(funcname)
    fun1.SetLineColor(2)

    g2.SetMarkerColor(4)
    g2.SetMarkerStyle(26)
    g2.SetLineColor(4)
    g2.Draw('sameP')
    checkFit(g2.Fit(funcname, 'S'))
    fun2 = g2.GetFunction(funcname)
    fun2.SetLineColor(4)

    lg.AddEntry(g0, vary[1][1], 'l')
    lg.AddEntry(g1, vary[2][1], 'p')
    lg.AddEntry(g2, vary[3][1], 'p')
    lg.Draw()


    uncert = []
    for x in opoints:
        e1 = fun1.Eval(x)
        e2 = fun2.Eval(x)
        uncert.append((max(abs(e1),abs(e2)), e1, e2))
    print uncert

    gPad.Update()
    waitRootCmd(sDir+sTag+vary[0])

    return uncert


def test3():
    sf1 = None
    opoints=[90, 120, 150]
    vv1 = []
    vv1.append(['renorm', ('norm', 'Nominal', 'Sherpa_llvv'),('renorm4', 'renorm4', 'Sherpa_llvv_renorm4'), ('renorm025', 'renorm025', 'Sherpa_llvv_renorm025')])
    vv1.append(['qsf', ('norm', 'Nominal', 'Sherpa_llvv'),('qsf4', 'qsf4', 'Sherpa_llvv_qsf4'), ('qsf025', 'qsf025', 'Sherpa_llvv_qsf025')])
    vv1.append(['fac', ('norm', 'Nominal', 'Sherpa_llvv'),('fac4', 'fac4', 'Sherpa_llvv_fac4'), ('fac025', 'fac025', 'Sherpa_llvv_fac025')])
    vv1.append(['ckkw', ('norm', 'Nominal', 'Sherpa_llvv'),('ckkw15', 'ckkw15', 'Sherpa_llvv_ckkw15'), ('ckkw30', 'ckkw30', 'Sherpa_llvv_ckkw30')])

    allS = [0 for x in opoints]
    for v1 in vv1:
        u1 = checkVary(sf1, v1, opoints)
        for i in range(len(allS)):
            allS[i] += pow(u1[i][0],2)
            print opoints[i], math.sqrt(allS[i])
    for i in range(len(allS)):
        print opoints[i], math.sqrt(allS[i])

def test2():
    options = oo1()
    options.process = "DB_DF"
#     options.inputname  = "Sherpa_llvv,Sherpa_llvv_fac4,Sherpa_llvv_fac025,Sherpa_llvv_renorm4,Sherpa_llvv_renorm025,Sherpa_llvv_qsf4,Sherpa_llvv_qsf025,Sherpa_llvv_ckkw15,Sherpa_llvv_ckkw30"
    options.inputname  = "Sherpa_llvv"
    options.grouping   = "NONE"                         # Combination : first one is nominal
    options.varname    = "mT2ll"                                       # Dummy variable
    options.regionname = "EW2L_CR_DF,EW2L_SR_DF"        #               # 0 is SR 1 is CR
    options.luminosity = 3210.000

    mtb = range(60,200,10)
    r0_df = get_DF_SF(options, mtb)
    options.inputname = 'Sherpa_llvv_fac4'
    r1_df = get_DF_SF(options, mtb)
    options.inputname = 'Sherpa_llvv_fac025'
    r2_df = get_DF_SF(options, mtb)

    shift = 0.5
    g0 = TGraphErrors()
    g1 = TGraphErrors()
    g2 = TGraphErrors()
    for i in range(len(r1_df)-1):
        g0.SetPoint(i, mtb[i], 0)
        g0.SetPointError(i, 0, r0_df[i+1][3])
        g1.SetPoint(i, mtb[i]+shift, (r1_df[i+1][2]-r0_df[i+1][2])/r0_df[i+1][2]*100)
        g1.SetPointError(i, 0, r1_df[i+1][3])
        g2.SetPoint(i, mtb[i]-shift, (r2_df[i+1][2]-r0_df[i+1][2])/r0_df[i+1][2]*100)
        g2.SetPointError(i, 0, r2_df[i+1][3])

    lg = TLegend(0.2, 0.7, 0.4, 0.9)
    lg.SetFillStyle(0)

    g0.SetMarkerSize(0.01)
    g0.Draw("ALP")
    g0.GetXaxis().SetTitle(getXtitle(options.varname))
    g0.GetYaxis().SetTitle('Uncertainty [%]')
    g1.SetMarkerColor(2)
    g1.SetLineColor(2)
    g1.SetMarkerStyle(23)
    g1.Draw('sameP')
    funcname = 'pol2'
    checkFit(g1.Fit(funcname, 'S'))
    fun1 = g1.GetFunction(funcname)
    fun1.SetLineColor(2)

    g2.SetMarkerColor(4)
    g2.SetMarkerStyle(26)
    g2.SetLineColor(4)
    g2.Draw('sameP')
    checkFit(g2.Fit(funcname, 'S'))
    fun2 = g2.GetFunction(funcname)
    fun2.SetLineColor(4)

    vary1 = 'vary1'
    vary2 = 'vary2'
    lg.AddEntry(g0, 'Norminal', 'l')
    lg.AddEntry(g1, vary1, 'p')
    lg.AddEntry(g2, vary2, 'p')
    lg.Draw()


    for x in mtb:
        print x, fun1.Eval(x), fun2.Eval(x)

    gPad.Update()
    waitRootCmd()

    options.regionname = "EW2L_CR_SF,EW2L_SR_SF"
    get_DF_SF(options)

def checkFit(fr1):
    if fr1.Prob()<0.05:
        print 'bad fit', fr1.Prob()

def compare3(options, samples, tag):
    options.inputname = samples[0][2]
    r0_df,h0s = get_DF_SF_More(options, options.mT2Cuts, False)

    options.inputname = samples[1][2]
    r1_df,h1s = get_DF_SF_More(options, options.mT2Cuts, False)

    options.inputname = samples[2][2]
    r2_df,h2s = get_DF_SF_More(options, options.mT2Cuts, False)

    for i in range(len(r0_df)):
        print r0_df[i], r1_df[i]
#         res.append()
    res = []
    for i in range(1,len(r0_df)):
        res.append(max(pow(r0_df[i][2]-r1_df[i][2],2), pow(r0_df[i][2]-r2_df[i][2],2)))

#     h0s[0].SetMarkerColor(2)
#     h0s[0].SetLineColor(2)
    h0s[0].Draw()
#     h0s[1].SetLineColor(2)
#     h0s[1].SetLineStyle(2)
    h0s[1].Draw('histsame')
    h1s[0].SetMarkerColor(4)
    h1s[0].SetLineColor(4)
    h1s[0].SetMarkerStyle(24)
    h1s[0].Draw('sameE')
    h1s[1].SetLineColor(4)
    h1s[1].SetLineStyle(0)
    h1s[1].Draw('histsame')
    h2s[0].SetMarkerColor(2)
    h2s[0].SetLineColor(2)
    h2s[0].SetMarkerStyle(25)
    h2s[0].Draw('sameE')
    h2s[1].SetLineColor(2)
    h2s[1].SetLineStyle(2)
    h2s[1].Draw('histsame')

    lg = TLegend(0.6, 0.7, 0.9, 0.92)
    lg.SetFillStyle(0)
    lg.AddEntry(h0s[0], samples[0][1]+'CR', 'p')
    lg.AddEntry(h0s[1], samples[0][1]+'SR', 'l')
    lg.AddEntry(h1s[0], samples[1][1]+'CR', 'p')
    lg.AddEntry(h1s[1], samples[1][1]+'SR', 'l')
    lg.AddEntry(h2s[0], samples[2][1]+'CR', 'p')
    lg.AddEntry(h2s[1], samples[2][1]+'SR', 'l')
    lg.Draw()

    gPad.Update()
    waitRootCmd(sDir+sTag+tag)

    return res 


def compare2(options, samples, tag):
    options.inputname = samples[0][2]
    r0_df,h0s = get_DF_SF_More(options, options.mT2Cuts, False)

    options.inputname = samples[1][2]
    r1_df,h1s = get_DF_SF_More(options, options.mT2Cuts, False)

    for i in range(len(r0_df)):
        print r0_df[i], r1_df[i]
#         res.append()
    res = []
    for i in range(1,len(r0_df)):
        res.append(pow(r0_df[i][2]-r1_df[i][2],2))

    h0s[0].SetMarkerColor(2)
    h0s[0].SetLineColor(2)
    h0s[0].Draw()
    h0s[1].SetLineColor(2)
    h0s[1].SetLineStyle(2)
    h0s[1].Draw('histsame')
    h1s[0].SetMarkerColor(4)
    h1s[0].SetLineColor(4)
    h1s[0].SetMarkerStyle(24)
    h1s[0].Draw('sameE')
    h1s[1].SetLineColor(4)
    h1s[1].SetLineStyle(0)
    h1s[1].Draw('histsame')

    lg = TLegend(0.6, 0.7, 0.9, 0.92)
    lg.SetFillStyle(0)
    lg.AddEntry(h0s[0], samples[0][1]+'CR', 'p')
    lg.AddEntry(h0s[1], samples[0][1]+'SR', 'l')
    lg.AddEntry(h1s[0], samples[1][1]+'CR', 'p')
    lg.AddEntry(h1s[1], samples[1][1]+'SR', 'l')
    lg.Draw()

    gPad.Update()
    waitRootCmd(sDir+sTag+tag)

    return res 


def checkPDF(options, tag='pdf'):
    r0_df,h0s = get_DF_SF_More_wt(options, options.mT2Cuts, False, '*pdfWeights[0]')

    gU = TGraphErrors()
    gD = TGraphErrors()
    ic = 1
    shift = 0.1
    xT = []
    for i in range(26):
        r1_df,h1s = get_DF_SF_More_wt(options, options.mT2Cuts, False, '*pdfWeights['+str(2*i+1)+']')
        r2_df,h2s = get_DF_SF_More_wt(options, options.mT2Cuts, False, '*pdfWeights['+str(2*i+2)+']')
        gU.SetPoint(i, i+shift, (r1_df[ic][2]-r0_df[ic][2])/r0_df[ic][2]*100.)
        gU.SetPointError(i, 0, r1_df[ic][2])
        gD.SetPoint(i, i+shift, (r2_df[ic][2]-r0_df[ic][2])/r0_df[ic][2]*100.)
        gD.SetPointError(i, 0, r2_df[ic][2])
        xT.append(((r1_df[ic][2]-r0_df[ic][2])/r0_df[ic][2]*100., (r2_df[ic][2]-r0_df[ic][2])/r0_df[ic][2]*100.))

    gU.SetMarkerStyle(23)
    gD.SetMarkerStyle(26)
    gU.SetMarkerColor(2)
    gD.SetMarkerColor(4)
    gU.Draw("AP")
    gU.GetXaxis().SetTitle('PDF variation index')
    gU.GetXaxis().SetTitle('Shift [%]')
    gD.Draw("Psame")
    lg = TLegend(0.6, 0.7, 0.9, 0.92)
    lg.SetFillStyle(0)
    lg.AddEntry(gU, "UP", 'p')
    lg.AddEntry(gD, "DOWN", 'p')
    lg.Draw()

    tt1 = 0
    for x in xT:
        tt1 += max(x[0]*x[0],x[1]*x[1])
    print math.sqrt(tt1)

    gPad.Update()
    waitRootCmd(sDir+sTag+tag)



def runTopSF():
    # region: EW2L_TopVR_XF,EW2L_SR_XF
    options = oo1()
    options.varname    = "mT2ll"                                       # Dummy variable
    options.regionname = "EW2L_TopVR_XF,EW2L_SR_XF"        #               # 0 is SR 1 is CR
    options.luminosity = 10000.
    options.mT2Cuts = [90, 120, 150]

#     tag = 'generator'
#     samples = []
#     samples.append(('aMcAtNlo', 'aMc@Nlo Top ', 'aMcAtNloHerwigppEvtGen_ttbar_nonallhad,aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Wt_dilepton'))
#     samples.append(('Powheg', 'Powheg Top ', 'PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top'))
#     uncert = compare2(options, samples, tag)
# 
#     print uncert
# 
#     tag = 'PS'
#     samples = []
#     samples.append(('aMcAtNlo', 'aMc@Nlo Top ', 'aMcAtNloHerwigppEvtGen_ttbar_nonallhad,aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Wt_dilepton'))
#     samples.append(('Powheg', 'Powheg Top ', 'PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top'))
#     uncert = compare2(options, samples, tag)
# 
#     print uncert

    tag = 'DS'
    samples = []
    samples.append(('norm', 'Wt DR Top ', 'PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'))
    samples.append(('DS',   'Wt DS Top ', 'PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil,PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_top'))
    uncert = compare2(options, samples, tag)

    print uncert

#     tag = 'rad'
#     samples = []
#     samples.append(('norm', 'Nominal Top ', ',PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'))
#     samples.append(('up',   'Rad-up Top ', 'PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad,PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_top'))
#     samples.append(('down',   'Rad-down Top ', 'PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad,PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_top'))
#     uncert = compare3(options, samples, tag)

#     print uncert

#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     checkPDF(options)


#     tag = 'pdf'
#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     r0_df,h0s = get_DF_SF_More_wt(options, options.mT2Cuts, False, '*pdfWeights[0]')
#     r1_df,h1s = get_DF_SF_More_wt(options, options.mT2Cuts, False, '*pdfWeights[1]')
#     r2_df,h2s = get_DF_SF_More_wt(options, options.mT2Cuts, False, '*pdfWeights[2]')
#     samples = [('', 'v0 Top '), ('', 'v1 Top '), ('', 'v2 Top ')]
#     for i in range(len(r0_df)):
#         print r0_df[i], r1_df[i], r2_df[i]
# #         res.append()
#     res = []
#     for i in range(1,len(r0_df)):
#         res.append(max(pow(r0_df[i][2]-r1_df[i][2],2), pow(r0_df[i][2]-r2_df[i][2],2)))
# 
#     h0s[0].Draw()
#     h0s[1].Draw('histsame')
#     h1s[0].SetMarkerColor(4)
#     h1s[0].SetLineColor(4)
#     h1s[0].SetMarkerStyle(24)
#     h1s[0].Draw('sameE')
#     h1s[1].SetLineColor(4)
#     h1s[1].SetLineStyle(0)
#     h1s[1].Draw('histsame')
#     h2s[0].SetMarkerColor(2)
#     h2s[0].SetLineColor(2)
#     h2s[0].SetMarkerStyle(25)
#     h2s[0].Draw('sameE')
#     h2s[1].SetLineColor(2)
#     h2s[1].SetLineStyle(2)
#     h2s[1].Draw('histsame')
# 
#     lg = TLegend(0.6, 0.7, 0.9, 0.92)
#     lg.SetFillStyle(0)
#     lg.AddEntry(h0s[0], samples[0][1]+'CR', 'p')
#     lg.AddEntry(h0s[1], samples[0][1]+'SR', 'l')
#     lg.AddEntry(h1s[0], samples[1][1]+'CR', 'p')
#     lg.AddEntry(h1s[1], samples[1][1]+'SR', 'l')
#     lg.AddEntry(h2s[0], samples[2][1]+'CR', 'p')
#     lg.AddEntry(h2s[1], samples[2][1]+'SR', 'l')
#     lg.Draw()
# 
#     gPad.Update()
#     waitRootCmd(sDir+sTag+tag)
# 
#     print res
#     return res 


if __name__ == '__main__':
    useAtlasStyle()
    gStyle.SetOptFit(0)
    runTopSF()
#     test3()

