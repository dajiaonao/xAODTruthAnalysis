#!/usr/bin/env python
import sys,math,array
from ROOT import *
from rootUtil import waitRootCmd, get_default_fig_dir, useAtlasStyle

from plot_definitions import *

sDir = get_default_fig_dir()
sTag = 'r1_SF_'

class oo1:
    pass

def get_TOP_Yields(options, mT2CutList=[90, 120, 150], showPlot=False):
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

#     selection0=("(mcEventWeight/%f)*(%s)"%(sumw,cut0))
#     ch1.Draw(var1+">>"+histoName0, selection0, 'goff')
# 
#     selection1=("(mcEventWeight/%f)*(%s)"%(sumw,cut1))
#     ch1.Draw(var1+">>"+histoName1, selection1, 'goff')


    control_region_unc      = ROOT.Double(0.)
    control_region_count    = histogram0.IntegralAndError(0,-1,control_region_unc)
    control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.

    results = [(histogram0.Integral(0,-1), histogram1.Integral(0,-1)), (control_region_count, control_region_unc_perc)]
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


def getHisto(inputname, region, wt='', luminosity=10000.):
    files = getROOTFileName(inputname)
    sumw = getSumWeight(files)

    ch1 = TChain('SuperTruth')
    ch1.Add(files)
    var1 = 'mT2ll'

    histoName = 'h_'+inputname+'_'+wt.replace('[','_').replace(']','').replace('*','_')+region
    histogram0 = TH1D(histoName, histoName+';mT_{2}(ll) [GeV];Events / 5 GeV',40,0,200)
 
    cut0=getRegionTCut(region)
    selection0=("(mcEventWeight"+wt+"*%f*%f/%f)*(%s)"%(getCrossSection(inputname),luminosity,sumw,cut0))
    print ch1.Draw(var1+">>"+histoName, selection0, 'goff')

    return histogram0

def getHistos(inputnames, region, wt='', hname='hx1'):
    th = None
    for s in inputnames.split(','):
        kk = getHisto(s, region, wt)
        if not th: th = kk.Clone(hname)
        else:
            th.Add(kk)
    return th


def checkDistributions():
    options = oo1()
    options.varname    = "mT2ll"                                       # Dummy variable
    options.regionname = "EW2L_SR_XF,EW2L_TopVR_XF"        #               # 0 is SR 1 is CR
    sTag = 'test1_'

    options.luminosity = 10000.
    options.mT2Cuts = [90]

    options.inputname = 'PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad,PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_top'
    r2 = getHistos(options.inputname, 'EW2L_TopVR_XF_noMT2', '', 'h_radHi')
    r2.Draw()

    options.inputname = 'PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad,PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_top'
    r3 = getHistos(options.inputname, 'EW2L_TopVR_XF_noMT2', '', 'h_radLo')
    r3.Draw('same')

    waitRootCmd()

def get_TOP_Yields_more(options, mT2CutList=[90, 120, 150], showPlot=False, exwt=''):
    sTag = options.inputname
    regions = options.regionname.split(',') 

    th = None
    for s in options.inputname.split(','):
        kk = tag2Hitos(s, regions, exwt)
        if not th: th = kk
        else:
            for i in range(len(kk)):
                th[i].Add(kk[i])
    (histogram0, histogram1) = th

#     cut0=getRegionTCut(regions[0])
#     cut1=getRegionTCut(regions[1])
# 
#     selection0=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(sTag),options.luminosity,sumw,cut0))
#     ch1.Draw(var1+">>"+histoName0, selection0, 'goff')
# 
#     selection1=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(sTag),options.luminosity,sumw,cut1))
#     ch1.Draw(var1+">>"+histoName1, selection1, 'goff')
# 
    control_region_unc      = ROOT.Double(0.)
    control_region_count    = histogram0.IntegralAndError(0,-1,control_region_unc)
    control_region_unc_perc = (control_region_unc/control_region_count)*100 if control_region_count !=0 else 0.

    results = [(histogram0.Integral(0,-1), histogram1.Integral(0,-1)), (control_region_count, control_region_unc_perc)]
    for slow in mT2CutList:
        bin0 = histogram1.GetXaxis().FindBin(slow)
        signal_region_unc       = ROOT.Double(0.) 
        signal_region_count     = histogram1.IntegralAndError(bin0,-1,signal_region_unc)
        signal_region_unc_perc  = (signal_region_unc/signal_region_count)*100 if signal_region_unc !=0 else 0. 

        transfer_factors = signal_region_count/control_region_count 
        tf_unc = math.sqrt(signal_region_unc_perc*signal_region_unc_perc+control_region_unc_perc*control_region_unc_perc)

        results.append((signal_region_count, signal_region_unc_perc, transfer_factors, tf_unc))

    if showPlot:
        histogram0.Draw()
        histogram1.SetLineColor(2)
        histogram1.SetLineStyle(2)
        histogram1.Draw("histsame")
        waitRootCmd()
    return results






def checkTop1():
    options = oo1()
    options.varname    = "mT2ll"                                       # Dummy variable
    options.regionname = "EW2L_SR_XF,EW2L_TopVR_XF"        #               # 0 is SR 1 is CR
    sTag = 'test1_'

    options.luminosity = 10000.

    options.inputname = 'aMcAtNloHerwigppEvtGen_ttbar_nonallhad'
    r1 = get_TOP_Yields(options)
    print r1

    options.inputname = 'PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad'
    r2 = get_TOP_Yields(options)
    print r2

def checkTop():
    options = oo1()
    options.varname    = "mT2ll"                                       # Dummy variable
    options.regionname = "EW2L_SR_XF,EW2L_TopVR_XF"        #               # 0 is SR 1 is CR
    sTag = 'test1_'

    options.luminosity = 10000.
    options.mT2Cuts = [90]

#     options.inputname = 'PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top'
#     r1 = get_TOP_Yields_more(options)
#     print r1
# 
#     options.inputname = 'aMcAtNloHerwigppEvtGen_ttbar_nonallhad,aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Wt_dilepton'
#     r2 = get_TOP_Yields_more(options)
#     print r2

#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     r1 = get_TOP_Yields_more(options)
#     print r1

#     options.inputname = 'PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop,PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top'
#     r2 = get_TOP_Yields_more(options)
#     print r2

    ### radiation
#     options.inputname = 'PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad,PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_top'
#     r2 = get_TOP_Yields_more(options)
#     print r2
# 
#     options.inputname = 'PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad,PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_top'
#     r3 = get_TOP_Yields_more(options)
#     print r3

    #### top mass
#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp170_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     print get_TOP_Yields_more(options)
# 
#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp171p5_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     print get_TOP_Yields_more(options)
# 
#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp173p5_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     print get_TOP_Yields_more(options)
# 
#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp175_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     print get_TOP_Yields_more(options)
# 
#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp177p5_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
#     print get_TOP_Yields_more(options)
# 

    #### interference
#     options.inputname = 'PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad,PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_top'
#     print get_TOP_Yields_more(options)

    ### pdf
#     options.inputname = 'PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
    options.inputname = 'aMcAtNloHerwigppEvtGen_ttbar_nonallhad,PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop,PowhegPythiaEvtGen_P2012_Wt_dilepton_top'
    checkPDF(options)


def tag2Hitos(sTag, regions, wt='', luminosity=10000.):
    files = getROOTFileName(sTag)
    sumw = getSumWeight(files)

    ch1 = TChain('SuperTruth')
    ch1.Add(files)
    var1 = 'mT2ll'

    histoName = 'h_'+sTag+'_'+wt.replace('[','_').replace(']','').replace('*','_')
#     print wt
#     histoName.replace('[','_').replace(']','').replace('*','_')
    histoName0 = histoName+regions[0]
    histoName1 = histoName+regions[1]
#     print histoName0, histoName1

    histogram0 = TH1D(histoName0, histoName+';mT_{2}(ll) [GeV];Events / 5 GeV',40,0,200)
    histogram1 = histogram0.Clone(histoName1) 

    cut0=getRegionTCut(regions[0])
    cut1=getRegionTCut(regions[1])
 
#     ch1.Scan("pdfWeights[1]")

#     print ch1.GetEntries()
#     ch1.Draw(var1,"(pdfWeights[0]*mcEventWeight*450.924159*10000.000000/819156.000000)*(((@lepton_pt.size()==2&&isOS&&lepton_pt[0]>25.&&lepton_pt[1]>20.&&(lepton_type[0]==2||lepton_type[0]==6)&&(lepton_type[1]==2||lepton_type[1]==6))&&mll>20.&&(@bjet_pt.size()==0)&&Sum$(nonbjet_pt>30)==0&&Sum$(forwardjet_pt>30)==0))")
#     waitRootCmd()

    print sTag 
    selection0=("(mcEventWeight"+wt+"*%f*%f/%f)*(%s)"%(getCrossSection(sTag),luminosity,sumw,cut0))
#     selection0=("("+wt+"mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(sTag),luminosity,sumw,cut0))
#     print selection0
    print ch1.Draw(var1+">>"+histoName0, selection0, 'goff')
#     waitRootCmd()

    selection1=("(mcEventWeight"+wt+"*%f*%f/%f)*(%s)"%(getCrossSection(sTag),luminosity,sumw,cut1))
#     selection1=("("+wt+"mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(sTag),luminosity,sumw,cut1))
    print ch1.Draw(var1+">>"+histoName1, selection1, 'goff')
#     print histogram0.Integral(0,-1)
#     histogram0.Draw()
#     waitRootCmd()

    return (histogram0, histogram1)



def getSumWeight(iiFile):
    sumw = 0.
    for f in glob.glob(iiFile):
        f1 = ROOT.TFile(f,'read')
        sumw += f1.Get("CutflowWeighted").GetBinContent(1)
    return sumw

def checkPDF(options, tag='pdf'):
    r0_df = get_TOP_Yields_more(options, options.mT2Cuts, False, '*pdfWeights[0]')
#     r0_df = get_TOP_Yields_more(options, options.mT2Cuts, False, '*1')
    print r0_df

    gU = TGraphErrors()
    gD = TGraphErrors()
    ic = 1
    shift = 0.1
    xT = []
    for i in range(26):
        r1_df = get_TOP_Yields_more(options, options.mT2Cuts, False, '*pdfWeights['+str(2*i+1)+']')
        r2_df = get_TOP_Yields_more(options, options.mT2Cuts, False, '*pdfWeights['+str(2*i+2)+']')
        print r1_df
        print r2_df

        gU.SetPoint(i, i+shift, (r1_df[ic][0]-r0_df[ic][0])/r0_df[ic][0]*100.)
        gU.SetPointError(i, 0, r1_df[ic][1])
        gD.SetPoint(i, i+shift, (r2_df[ic][0]-r0_df[ic][0])/r0_df[ic][0]*100.)
        gD.SetPointError(i, 0, r2_df[ic][1])

        xT.append(((r1_df[ic][0]-r0_df[ic][0])/r0_df[ic][0]*100., (r2_df[ic][0]-r0_df[ic][0])/r0_df[ic][0]*100.))

    gU.SetMarkerStyle(23)
    gD.SetMarkerStyle(26)
    gU.SetMarkerColor(2)
    gU.SetLineColor(2)
    gD.SetLineColor(4)
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

if __name__ == '__main__':
    useAtlasStyle()
    gStyle.SetOptFit(0)
#     runTopSF()
#     runVVSF()
#     checkTop()
    checkDistributions()

