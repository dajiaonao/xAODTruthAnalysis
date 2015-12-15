import os,sys,ROOT,math

from stop2L_definitions import *

# Main function
def main():
    # Get the user input
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", "--input", action="store", type="string", dest="inputname",
                      help="input ROOT file (if multiple comma seperated)", metavar="FILE", default="Sherpa_lvlv")
    parser.add_option("-g", "--grouping", action="store", type="string", dest="grouping",
                      help="grouping the inputs (format: 0,1+2,3+4...)", metavar="GROUPING", default="NONE")
    parser.add_option("-v", "--variable", action="store", type="string", dest="varname",
                      help="variable to plot (if multiple comma seperated)", metavar="VARIABLE", default="lepton_pt[0]")
    parser.add_option("-r", "--region", action="store", type="string", dest="regionname",
                      help="regions to plot (if multile comma seperated)", metavar="REGION", default="All")
    parser.add_option("-f", "--format", action="store", type="string", dest="plotformat",
                      help="plot format (eps, png etc.)", metavar="PLOTFORMAT", default="eps")
    parser.add_option("-o", "--outdir", action="store", type="string", dest="outdir",
                      help="dir for the plots", metavar="OUTDIR", default="Plots")
    parser.add_option("-l", "--lumi", action="store", type="float", dest="luminosity",
                      help="set luminosity for normalization [pb]", default=3340.)
    parser.add_option("-L", "--log", action="store_true", dest="log", default=False,
                      help="set Logy(true)")
    parser.add_option("-b", "--batch", action="store_true", dest="batch", default=False,
                      help="run ROOT in batch mode")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                      help="pring debug information")
    parser.add_option("-a", "--ratio", action="store_true", dest="ratio", default=False,
                      help="draw ratio plot")
    (options, args) = parser.parse_args()
   
    # Print the program variables
    print_userinput(options)

    # Set batch mode bool 
    ROOT.gROOT.SetBatch(options.batch)

    # Get ROOT files
    files=getROOTFiles(options)

    # Set colors
    colors=setColors(files)     

    # Fill Histograms
    histograms=fillHistograms(files,options)

    # SetAtlasStyle
    setATLASStyle()

    # Convert inputs into lists
    inputFileList=options.inputname.split(",")
    variableList=options.varname.split(",") 
    regionList=options.regionname.split(",")
    groupList=options.grouping.split(",")

    # Group the histograms
    if options.grouping == "NONE":
        groupList=inputFileList
        histogramsGrouped=histograms
    else:
        histogramsGrouped=groupHistograms(histograms,options)

    # Draw canvas
    canvas=ROOT.TCanvas("canvas","canvas",500,500)
    canvas.SetFillColor(0)
    canvas.cd()
    if len(groupList) < 2:
        print("\n\nWARNING :: Tried to plot ratio but provided only nominal sample, skipping ratio\n\n")
        options.ratio = False
    if options.ratio:
        topPad = ROOT.TPad("topPad","topPad",0,0.2,1,1.0)
        botPad = ROOT.TPad("botPad","botPad",0,0.0,1,0.3)
        topPad.SetBottomMargin(0.15)
        botPad.SetBottomMargin(0.3)
        topPad.Draw()
        botPad.Draw()
        ratios=[[[0 for x in range(len(variableList))] for x in range(len(regionList))] for x in range(len(groupList))] 

    # Set the legend
    legend=ROOT.TLegend(0.55,0.7,0.9,0.85)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)

    # Loop over regions 
    for ii,region in enumerate(regionList):
        # Loop over variables
        for jj,variable in enumerate(variableList):
            if options.ratio:
                botPad.cd()
                ROOT.gPad.SetGridy(1)
                dummyHisto=dummifyHistogram(histogramsGrouped[0][ii][jj])
                dummyHisto.GetXaxis().SetTitle(getXtitle(variable))
                dummyHisto.Draw()
                topPad.cd()
            # Loop over files 
            for kk,inputFile in enumerate(groupList):
                # Fill the legend
                if ii == 0 and jj == 0:
                    if "0" in inputFile:
                        legend.AddEntry(histogramsGrouped[kk][ii][jj],inputFile.replace("0","Sherpa_lvlv"),"l")
                    elif "1+2" in inputFile:
                        legend.AddEntry(histogramsGrouped[kk][ii][jj],inputFile.replace("1+2","Powheg_lvlv"),"l")
                    else:
                        legend.AddEntry(histogramsGrouped[kk][ii][jj],inputFile,"l")
                # Histograms are scaled in fillHistograms
                # but here we can scale them to unity to check the shapes
                #scaleToUnity(histogramsGrouped[kk][ii][jj]) 
                # Add the overflow to last bin before plotting
                addOverFlowToLastBin(histogramsGrouped[kk][ii][jj]) 
                # Draw onto canvas
                if kk==0:
                    histogramsGrouped[kk][ii][jj].Draw("hist")
                else:
                    histogramsGrouped[kk][ii][jj].Draw("hist&&same")
                # Set colors, titles, ranges etc.
                histogramsGrouped[kk][ii][jj].SetLineColor(colors[kk])
                histogramsGrouped[kk][ii][jj].SetLineWidth(2)
                histogramsGrouped[kk][ii][jj].GetXaxis().SetTitle(getXtitle(variable))
                histogramsGrouped[kk][ii][jj].GetXaxis().SetTitleOffset(1.3)
                if options.ratio:
                    histogramsGrouped[kk][ii][jj].GetXaxis().SetLabelOffset(10)
                histogramsGrouped[kk][ii][jj].GetYaxis().SetTitle("Events")
                histogramsGrouped[kk][ii][jj].GetYaxis().SetTitleOffset(1.3)
                if options.log:
                    histogramsGrouped[kk][ii][jj].GetYaxis().SetRangeUser(1.e-2,1.e2*pow(10,math.ceil(math.log(histogramsGrouped[kk][ii][jj].GetMaximum())/math.log(10))))
                else:
                    histogramsGrouped[kk][ii][jj].GetYaxis().SetRangeUser(0.,1.5*histogramsGrouped[kk][ii][jj].GetMaximum())
                # Calculate the ratio
                if not options.ratio or kk==0: # 0 is assumed to be the denominator
                    continue
                numerator   = ROOT.TH1TOTGraph(histogramsGrouped[kk][ii][jj])
                denominator = ROOT.TH1TOTGraph(histogramsGrouped[0][ii][jj])
                ratios[kk][ii][jj] = ROOT.myTGraphErrorsDivide(numerator,denominator)
                ratios[kk][ii][jj].SetLineColor(colors[kk])
                ratios[kk][ii][jj].SetMarkerColor(colors[kk])
                ratios[kk][ii][jj].SetMarkerSize(1.)
                botPad.cd()
                ratios[kk][ii][jj].Draw("p&&same&&0&&1")
                topPad.cd()
            # Draw the legend and decorations
            legend.Draw()
            ROOT.myText(0.20,0.88,ROOT.kBlack,"#bf{ATLAS} Internal")
            ROOT.myText(0.20,0.83,ROOT.kBlack,("%.2f fb^{-1} #sqrt{s} = 13 TeV"% (options.luminosity*1.e-3)))
            ROOT.myText(0.55,0.88,ROOT.kBlack,("Region : %s"% (region)))
            ROOT.gPad.SetLogy(options.log)
            # Save canvas
            if not os.path.exists(options.outdir):
                os.mkdir(options.outdir)
            canvas.SaveAs(("%s/%s_%s.%s"%(options.outdir,region,variable.replace("[","").replace("]",""),options.plotformat)))


# Print user input
def print_userinput(options):
    print("==========================================================================")
    print(" Program : make_plots.py")
    print(" Author  : A.S. Mete <amete@cern.ch>")
    print(" Copyright (C) 2015 University of California, Irvine")
    print("==========================================================================")
    print(" Flags:\n")
    print("   Input ROOT file(s) is(are)        %s " % (options.inputname) )
    print("   Grouping is                       %s " % (options.grouping)  )
    print("   Variable(s) to be plotted is(are) %s " % (options.varname)   )
    print("   Region(s) to be plotted is(are)   %s " % (options.regionname))
    print("   Luminosity for normalization      %f " % (options.luminosity))
    print("   Set Logy                          %i " % (options.log)       )
    print("   Run in batch mode                 %i " % (options.batch)     )
    print("   Print debug information           %i " % (options.debug)     )
    print("   Draw raio plot                    %i " % (options.ratio)     )
    print("   Output dir is                     %s " % (options.outdir)    )
    print("   Plot format is                    %s " % (options.plotformat))
    print("\n==========================================================================")

if __name__ == "__main__":
    main()
