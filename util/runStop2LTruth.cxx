#include <cstdlib>
#include "xAODRootAccess/Init.h"
#include "SampleHandler/SampleHandler.h"
#include "SampleHandler/ScanDir.h"
#include "SampleHandler/ToolsDiscovery.h"
#include "EventLoop/Job.h"
#include "EventLoop/DirectDriver.h"
#include "EventLoopGrid/PrunDriver.h"
#include "SampleHandler/DiskListLocal.h"
#include <TSystem.h>
#include "SampleHandler/ScanDir.h"
#include <EventLoopAlgs/NTupleSvc.h>
#include <EventLoop/OutputStream.h>

#include "xAODTruthAnalysis/Stop2LTruthAnalysis.h"

#include <iostream>

void help() {
  printf("==========================================================================================================\n");  
  printf(" Author: A.S. Mete <amete@cern.ch>                   \n");
  printf(" Copyright (C) 2015 University of California, Irvine \n");
  printf("==========================================================================================================\n");  
  printf(" Usage:\n");
  printf("\tinputPath\t:\t%s\n","Input folder where the file(s) reside");
  printf("\toutputPath\t:\t%s\n","Output folder where the result(s) will be written");
  printf("\tprodTag\t\t:\t%s\n","If submitted to the Grid, use this in the output name for tagging");
  printf("\tsamplePattern\t:\t%s\n","Pattern to be searched in the file name, default = *.pool.root*");
  printf("\tsampleDepth\t:\t%s\n","Subfolder depth in the inputPath for the ROOT files, default = 0");
  printf("\tnEvents\t\t:\t%s\n","Events to be processed, default = -1");
  printf("\tisSignal\t:\t%s\n","Bool for 3-body stop decay, default = 0");
  printf("\tsaveTree\t:\t%s\n","Save results in a Tree, default = 0");
  printf("\tsaveHists\t:\t%s\n","Save results as Histograms, default = 0");
  printf("\tisRecoSample\t:\t%s\n","Bool for looping over SUSY2, default = 0");
  printf("==========================================================================================================\n");  
}

int main( int argc, char* argv[] ) {

  // Take the submit directory from the input if provided:
  std::string inputPath      = "/data7/atlas/amete/MC15_ModelingUncertainties/";
  std::string samplePattern  = "*.pool.root*";
  std::string outputPath     = "outputPath";
  std::string prodTag        = "test";
  int  sampleDepth           = 0; 
  bool isSignalSample        = false;
  bool saveROOTwithTree      = false;
  bool saveROOTwithHist      = false;
  bool submitToGrid          = false;
  bool submitToCondor        = false;
  int  nEvents               = -1;
  bool isRecoSample          = false;

  // Read inputs to program 
  for(int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-n"                 ) == 0)
      nEvents = atoi(argv[++i]);
    else if (strcmp(argv[i], "-i"            ) == 0)
      inputPath = argv[++i];
    else if (strcmp(argv[i], "-o"            ) == 0)
      outputPath = argv[++i];
    else if (strcmp(argv[i], "-sD"           ) == 0)
      sampleDepth = atoi(argv[++i]);
    else if (strcmp(argv[i], "-sP"           ) == 0)
      samplePattern = argv[++i];
    else if (strcmp(argv[i], "-t"            ) == 0)
      prodTag = argv[++i];
    else if (strcmp(argv[i], "--isSignal"    ) == 0)
      isSignalSample = true;
    else if (strcmp(argv[i], "--saveHists"   ) == 0)
      saveROOTwithHist = true;
    else if (strcmp(argv[i], "--saveTree"    ) == 0)
      saveROOTwithTree = true;
    else if (strcmp(argv[i], "--submitToGrid") == 0)
      submitToGrid = true;
    else if (strcmp(argv[i], "--submitToCondor") == 0)
      submitToCondor = true;
    else if (strcmp(argv[i], "--isRecoSample") == 0)
      isRecoSample = true;
    else
    {
       help();
       return 0;
     }
  }

  // Currently either Hist or Tree
  if( (saveROOTwithHist && saveROOTwithTree) ||
      (!saveROOTwithHist && !saveROOTwithTree) ) {
    help();
    return 0;
  }

  printf("==========================================================================================================\n");  
  printf(" Author: A.S. Mete <amete@cern.ch>                   \n");
  printf(" Copyright (C) 2015 University of California, Irvine \n");
  printf("==========================================================================================================\n");  
  printf(" Flags:\n");
  printf("\tinputPath\t:\t%s\n",inputPath.c_str());
  printf("\toutputPath\t:\t%s\n",outputPath.c_str());
  printf("\tprodTag\t\t:\t%s\n",prodTag.c_str());
  printf("\tsamplePattern\t:\t%s\n",samplePattern.c_str());
  printf("\tsampleDepth\t:\t%i\n",sampleDepth);
  printf("\tnEvents\t\t:\t%i\n",nEvents);
  printf("\tisSignal\t:\t%i\n",isSignalSample);
  printf("\tsaveTree\t:\t%i\n",saveROOTwithTree);
  printf("\tsaveHists\t:\t%i\n",saveROOTwithHist);
  printf("\tisRecoSample\t:\t%i\n",isRecoSample);
  printf("==========================================================================================================\n");  

  // Set up the job for xAOD access:
  xAOD::Init().ignore();

  // Construct the samples to run on:
  SH::SampleHandler sh;

  // use SampleHandler to scan all of the subdirectories of a directory for particular MC single file:
  const char* inputFilePath = gSystem->ExpandPathName (inputPath.c_str());
  if(!submitToGrid && !submitToCondor) {
    SH::ScanDir().sampleDepth(sampleDepth).samplePattern(samplePattern).scan(sh, inputFilePath);
  } else if (submitToGrid) {
    SH::scanRucio(sh, inputFilePath);
  } else {
    SH::readFileList(sh, "sample", inputFilePath);
  }

  // Set the name of the input TTree. It's always "CollectionTree"
  // for xAOD files.
  sh.setMetaString( "nc_tree", "CollectionTree" );

  // Print what we found:
  sh.print();

  // Create an EventLoop job:
  EL::Job job;
  job.sampleHandler( sh );
  job.options()->setDouble (EL::Job::optMaxEvents, nEvents);
  if(saveROOTwithTree) {
    EL::OutputStream output  ("myOutput");
    job.outputAdd (output);
    EL::NTupleSvc *ntuple = new EL::NTupleSvc ("myOutput");
    job.algsAdd (ntuple);
  }

  // Add our analysis to the job:
  Stop2LTruthAnalysis* alg = new Stop2LTruthAnalysis();
  alg->outputFileName = "myOutput";
  alg->isSignal  = isSignalSample;
  alg->saveTree  = saveROOTwithTree;
  alg->saveHists = saveROOTwithHist;
  alg->isRecoSample = isRecoSample;
  job.algsAdd( alg );

  // Run the job using the local/direct driver:
  if(!submitToGrid) {
    EL::DirectDriver driver;
    driver.submit( job, outputPath );
  } else {
    EL::PrunDriver driver;
    // Official sample
    driver.options()->setString("nc_outputSampleName", "user.amete."+prodTag+".%in:name[2]%.%in:name[6]%");
    // User sample
    //driver.options()->setString("nc_outputSampleName", "user.amete."+prodTag+".%in:name[4]%.%in:name[6]%");
    driver.submitOnly( job, outputPath );
  }

  return 0;
}
