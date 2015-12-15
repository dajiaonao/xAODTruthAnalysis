import ROOT,math,array

# Define the input ROOT files
def getROOTFileName(filename):
    return {
        "Sherpa_lvlv"     : "/gdata/atlas/amete/MC15_ModelingUncertainties/FlatNtuples/truth_v3/mc15_13TeV.361068.TRUTH1.root", 
        "Powheg_WWlvlv"   : "/gdata/atlas/amete/MC15_ModelingUncertainties/FlatNtuples/truth_v3/mc15_13TeV.361600.TRUTH1.root",
        "Powheg_ZZllvv"   : "/gdata/atlas/amete/MC15_ModelingUncertainties/FlatNtuples/truth_v3/mc15_13TeV.361604.TRUTH1.root",
        "Powheg_ttbar"    : "/gdata/atlas/amete/MC15_ModelingUncertainties/FlatNtuples/truth_v3/mc15_13TeV.410000.TRUTH1.root",
        "aMCatNLO_ttbar"  : "/gdata/atlas/amete/MC15_ModelingUncertainties/FlatNtuples/truth_v3/mc15_13TeV.410003.TRUTH1.root",
    }.get(filename,"")

# Define cross-sections
def getCrossSection(filename):
    return {
        "Sherpa_lvlv"   : 14.022*0.91,  # 361068 https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MC15SystematicUncertainties#VV_Diboson_V_W_Z 24/11/15
        "Powheg_WWlvlv" : 10.631,       # 361600
        "Powheg_ZZllvv" : 0.92498,      # 361604 
        "Powheg_ttbar"  : 831.76*0.543, # 410000
        "aMCatNLO_ttbar": 831.76*0.543, # 410003
    }.get(filename,"")

# Define X titles
def getXtitle(variable):
    return {
        "lepton_n"        : "Number of leptons", 
        "lepton_pt[0]"    : "Leading lepton p_{T} [GeV]", 
        "lepton_pt[1]"    : "Subleading lepton p_{T} [GeV]",
        "lepton_eta[0]"   : "Leading lepton #eta", 
        "lepton_eta[1]"   : "Subleading lepton #eta",
        "lepton_phi[0]"   : "Leading lepton #phi", 
        "lepton_phi[1]"   : "Subleading lepton #phi",
        "lepton_flav[0]"  : "Leading lepton flavor", 
        "lepton_flav[1]"  : "Subleading lepton flavor",
        "lepton_type[0]"  : "Leading lepton type", 
        "lepton_type[1]"  : "Subleading lepton type",
        "lepton_origin[0]": "Leading lepton origin", 
        "lepton_origin[1]": "Subleading lepton origin",
        "jet_n"           : "Number of jets", 
        "jet_pt[0]"       : "Leading jet p_{T} [GeV]", 
        "jet_pt[1]"       : "Subleading jet p_{T} [GeV]",
        "jet_eta[0]"      : "Leading jet #eta", 
        "jet_eta[1]"      : "Subleading jet #eta",
        "jet_phi[0]"      : "Leading jet #phi", 
        "jet_phi[1]"      : "Subleading jet #phi",
        "jet_flav[0]"     : "Leading jet flavor", 
        "jet_flav[1]"     : "Subleading jet flavor",
        "met_et"          : "E_{T}^{miss} [GeV]",
        "met_phi"         : "#phi(E_{T}^{miss})",
        "meff"            : "m_{eff} [GeV]",
        "pbll"            : "Pbll [GeV]",
        "mT2ll"           : "m_{T2}(ll) [GeV]",
        "mll"             : "m(ll) [GeV]",
        "r1"              : "R1",
        "dphi_met_pbll"   : "#Delta#phi(MET,Pbll)"
    }.get(variable,"N/A") # N/A is default if variable is not found

# Define region cuts
def getRegionTCut(region):
    return {
        "SR_ALL_TOP" : "(isDF || (isSF && (mll<71.||mll>111.)) ) && mll > 20. && mT2ll>100.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_ALL_NOMT2" : "(isDF || (isSF && (mll<71.||mll>111.)) ) && mll > 20. && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_ALL"     : "(isDF || (isSF && (mll<71.||mll>111.)) ) && mll > 20. && mT2ll>145.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_SF"      : "isSF && mll > 20. && (mll<71.||mll>111.) && mT2ll>145.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "CR_SF"      : "isSF && mll > 20. && (mT2ll>60.  && mT2ll<110.) && pbll<20. && r1>0.4 && TMath::Abs(dphi_met_pbll)<1.5 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_SF"      : "isSF && (mll>71.&&mll<111.) && mT2ll>110. && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "SR_DF"      : "isDF && mll > 20. && mT2ll>145.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "CR_DF"      : "isDF && mll > 20. && (mT2ll>60.  && mT2ll<110.) && pbll<20. && r1>0.4 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_DF"      : "isDF && mll > 20. && (mT2ll>110. && mT2ll<145.) && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_DF_2"    : "isDF && mll > 20. && (mT2ll>40.  && mT2ll<60. ) && pbll<20. && r1>0.4 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "CR_TOP"     : "isDF && mll > 20. && (mT2ll>60.  && mT2ll<110.) && pbll>30. && r1<0.4 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_DF_INC"  : "isDF && lepton_pt[0]>20. && lepton_pt[1]>20. && mll>20. && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_SF_INC"  : "isSF && lepton_pt[0]>20. && lepton_pt[1]>20. && mll>20. && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
    }.get(region,"1") # 1 is default if region is not found

# Define histogram bins
def getBinInformation(variable):
    return {
        "lepton_n"      : [ 10, 0, 10],
        "jet_n"         : [ 20, 0, 20],
        "lepton_pt"     : [[0,20,40,60,80,100,120,140,160,180,200,225,250,300,400,500,1000]],
        "jet_pt"        : [[0,20,40,60,80,100,120,140,160,180,200,225,250,300,400,500,1000]],
        "lepton_eta"    : [50,-2.5,2.5],
        "jet_eta"       : [90,-4.5,4.5],
        "lepton_phi"    : [70,-3.5,3.5],
        "jet_phi"       : [70,-3.5,3.5],
        "mT2ll"         : [[0,10,20,30,40,50,60,70,80,90,100,115,130,145,300]],
        "mll"           : [[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,400,500,1000]],
        "met_et"        : [[0,20,40,60,80,100,120,140,160,180,200,225,250,300,400,500,1000]],
        "met_phi"       : [70,-3.5,3.5],
        "pbll"          : [[0,20,40,60,80,100,120,140,160,180,200,225,250,300,400,500,1000]],
        "r1"            : [ 10,0, 1],
        "lepton_flav"   : [ 10, 10, 20],
        "jet_flav"      : [ 25, 0, 25],
        "lepton_type"   : [ 10, 0, 10],
        "lepton_origin" : [ 50, 0, 50],
        "dphi_met_pbll" : [70,-3.5,3.5],
    }.get(variable,[1,0.5,1.5]) # 1 is default if variable is not found

# Get files
def getROOTFiles(options):
    inputFileList=options.inputname.split(",")
    files=[0 for x in range(len(inputFileList))]
    for ii,inputFile in enumerate(inputFileList):
        files[ii] = ROOT.TFile(getROOTFileName(inputFile),"READ")
    return files

# Get sum of weights
def getSumOfWeights(files):
    sumw=[0 for x in range(len(files))]
    for ii,iiFile in enumerate(files):
        sumw[ii] = iiFile.Get("CutflowWeighted").GetBinContent(1)
    return sumw

# Set colors
def setColors(files):
    colors=[0 for x in range(len(files))] 
    for ii,iiFile in enumerate(files):
        if ii == 0: colors[ii] = ROOT.kBlue
        elif ii == 1: colors[ii] = ROOT.kSpring-1 
        elif ii == 2: colors[ii] = ROOT.kMagenta 
        elif ii == 3: colors[ii] = ROOT.kCyan+1
        elif ii == 4: colors[ii] = ROOT.kViolet+1
        elif ii == 5: colors[ii] = ROOT.kAzure+1
        elif ii == 6: colors[ii] = ROOT.kOrange+1 
        elif ii == 7: colors[ii] = ROOT.kYellow+1
    return colors

# Fill histograms
def fillHistograms(files,options):

    inputFileList=options.inputname.split(",")
    variableList=options.varname.split(",") 
    regionList=options.regionname.split(",")

    # Read the sum of weights
    sumw=getSumOfWeights(files) 

    histograms=[[[0 for x in range(len(variableList))] for x in range(len(regionList))] for x in range(len(inputFileList))]

    for ii,inputFile in enumerate(inputFileList):
        # Find the tree 
        currentROOTTree = files[ii].Get("SuperTruth")
        if not currentROOTTree:
            print("WARNING :: Cannot find ROOT tree in the file %s"%fullInputFileName)
            continue
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
                if variable == "lepton_n": variable = "@lepton_pt.size()"
                elif variable == "jet_n" : variable = "@jet_pt.size()"
                #currentROOTTree.Draw(variable+">>"+histoName,"mcEventWeight*("+cut+")","goff")                                
                selection=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                if options.debug:
                    print("INFO :: Selection is %s" % selection)
                currentROOTTree.Draw(variable+">>"+histoName,selection,"goff")                                

    return histograms

# Set ATLAS style
def setATLASStyle(path="/home/amete/ATLASStyle/current/"):
    ROOT.gROOT.SetMacroPath(path)
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle() 

# Scale to requested luminosity
def scaleToLuminosity(histogram,luminosity,crossSection,sumw):
    histogram.Scale(luminosity*crossSection/sumw)

# Scale to unity 
def scaleToUnity(histogram):
    integral = histogram.Integral()
    histogram.Scale(1./integral)

# Dummy ratio histogram
def dummifyHistogram(histo):
    ratio_histo = histo.Clone();
    ratio_histo.Reset();
    ratio_histo.SetMarkerSize(1.2);
    ratio_histo.SetMarkerStyle(20);
    ratio_histo.SetLineWidth(2);
    ratio_histo.GetYaxis().SetTitle("#frac{variation}{nominal}");
    ratio_histo.GetXaxis().SetLabelSize(0.1);
    ratio_histo.GetXaxis().SetLabelOffset(0.02);
    ratio_histo.GetXaxis().SetTitleSize(0.12);
    ratio_histo.GetXaxis().SetTitleOffset(1.);
    ratio_histo.GetYaxis().SetRangeUser(0.001,2);
    ratio_histo.GetYaxis().SetLabelSize(0.1);
    ratio_histo.GetYaxis().SetTitleSize(0.12);
    ratio_histo.GetYaxis().SetTitleOffset(0.5);
    ratio_histo.GetYaxis().SetNdivisions(5);
    return ratio_histo

# Function to add overflow to last bin
def addOverFlowToLastBin(histo):
    lastBin = histo.GetXaxis().GetNbins()
    lastBinValue  = histo.GetBinContent(lastBin)
    lastBinError  = histo.GetBinError(lastBin);
    overFlowValue = histo.GetBinContent(lastBin+1);
    overFlowError = histo.GetBinError(lastBin+1);
    histo.SetBinContent(lastBin+1,0);
    histo.SetBinError(lastBin+1,0);
    histo.SetBinContent(lastBin,lastBinValue+overFlowValue);
    histo.SetBinError(lastBin,math.sqrt(lastBinError*lastBinError+overFlowError*overFlowError));

# Group histograms
def groupHistograms(histograms,options):
    if options.grouping == "NONE":
        return histograms
 
    # Convert inputs into lists
    inputFileList=options.inputname.split(",")
    variableList=options.varname.split(",") 
    regionList=options.regionname.split(",")
    groupList=options.grouping.split(",")

    histogramsGrouped=[[[0 for x in range(len(variableList))] for x in range(len(regionList))] for x in range(len(groupList))]

    # Loop over regions 
    for jj,region in enumerate(regionList):
        # Loop over variables
        for kk,variable in enumerate(variableList):
            # Loop over groups
            for aa,group in enumerate(groupList):
                # Loop over contributions
                for bb,ii in enumerate(group.split("+")):
                    if histogramsGrouped[aa][jj][kk] == 0:
                        histogramsGrouped[aa][jj][kk] = histograms[int(ii)][jj][kk].Clone()
                    else:
                        histogramsGrouped[aa][jj][kk].Add(histograms[int(ii)][jj][kk]) 
   
    return histogramsGrouped 
