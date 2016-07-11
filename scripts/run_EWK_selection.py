#!/usr/bin/env python
import ROOT
import logging
import shutil
import os, re

from optparse import OptionParser

parser = OptionParser()
parser.add_option('-f', "--inputFiles", help="all input file", default=None)
parser.add_option('-l', "--inputList", help="list of input file", default=None)
parser.add_option('-t', "--inputTag", help="tag of input file", default="test")
parser.add_option('-d', "--inputDir", help="dir of input file", default=None)
parser.add_option('-o', "--outputDir", help="direcotry for output files", default="test")
parser.add_option('-n', "--nevents", type=int, help="number of events to process", default=-1)
parser.add_option("-w", "--overwrite", action='store_true', default=False, help="overwrite previous submitDir")
parser.add_option('-s', "--isSignal", action='store_true', help="type of input sample", default=False)
parser.add_option('--saveTree', action='store_true', help="save ttree", default=False)
parser.add_option('--saveHists', action='store_true', help="save histograms", default=False)
parser.add_option('--isRecoSample', action='store_true', help="sample passed reconstruction", default=False)
parser.add_option("--driver", help="select where to run", choices=("direct", "prooflite", "grid", "condor", "LSF"), default="direct")
parser.add_option("--inputDS", help="tag of input data set for grid driver", default=None)
parser.add_option("--shortName", help="shortname", default=None)
parser.add_option("--outputTag", help="tag of output for grid driver", default='test')
parser.add_option("--outputPattern", help="tag of output for grid driver", default=".%in:name[2]%.%in:name[3]%")
parser.add_option("--nFilesPerNode", type=int, help="number of files per node in LSF batch", default=15)
parser.add_option("--test", help="test run", action='store_true', default=False)
parser.add_option("--samplesDir", help="samples dir", default=None)
parser.add_option("--samplePattern", help="sample pattern", default='(.*)')
parser.add_option("--sampleList", help="sample list", default=None)
# parser.add_option("--isShortJob", action='store_true', default=False, help="use condor_submit_short")


(options, args) = parser.parse_args()

#gErrorIgnoreLevel = kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;
ROOT.gErrorIgnoreLevel = ROOT.kInfo
logging.basicConfig(level=logging.INFO)

import atexit
@atexit.register
def quite_exit():
    ROOT.gSystem.Exit(0)


logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

if options.overwrite:
    shutil.rmtree(options.outputDir, True)

#Set up the job for xAOD access:
ROOT.xAOD.Init().ignore();

# create a new sample handler to describe the data files we use
logging.info("creating new sample handler")
sh_all = ROOT.SH.SampleHandler()

if options.inputFiles:
    sample = ROOT.SH.SampleLocal(options.inputTag)
    for file in options.inputFiles.split(','): sample.add(file)
    sh_all.add (sample);
elif options.inputList:
    if options.driver == 'grid':
        with open(options.inputList) as fin1:
            for line in fin1.readlines():
                if line[0] == '#':
                    print line, 'skipped'
                    continue
                if line.find('*') == -1:
                    ROOT.SH.addGrid(sh_all, line.rstrip())
                else: ROOT.SH.scanDQ2(sh_all, line.rstrip())
    else: 
        ROOT.SH.readFileList(sh_all, options.inputTag, options.inputList);
elif options.inputDir:
    dir0 = options.inputDir
    if dir0[-1] != '/': dir0+='/'
    sample = ROOT.SH.SampleLocal(options.inputTag)
    files = [dir0+f for f in os.listdir(options.inputDir) if f.find('.root')!=-1]
    print dir0, len(files), 'files'
    for file in files: sample.add(file)
    sh_all.add (sample)
elif options.inputDS:
    if options.inputDS.find('*') != -1:
        ROOT.SH.scanRucio(sh_all, options.inputDS)
    else: ROOT.SH.addGrid(sh_all, options.inputDS)
elif options.samplesDir:
    dir0 = options.samplesDir
    if dir0[-1] != '/': dir0+='/'
    if options.sampleList:
        with open(options.sampleList) as fin1:
            for line in fin1.readlines():
                if line[0] == '#':
                    print line, 'skipped'
                    continue
                s = line.rstrip().split(':')
                stag = s[0]
                if len(s)==1:
                    vx = stag.split('.')
                    stag = 'mc_'+vx[1]+'.'+vx[2]

                sample = ROOT.SH.SampleLocal(stag)
                d = dir0+s[-1]
                print s[0],d
                for f in filter(lambda x: x.find('.root')!=-1, os.listdir(d)): sample.add(d+'/'+f)
                sh_all.add(sample)
    else:
        dirs = [dir0+d for d in os.listdir(dir0) if os.path.isdir(dir0+d)]
        for d in dirs:
            m1 = re.match(options.samplePattern, d)
            if not m1:
                print d, 'excluded'
                continue
            tag = m1.group(1)
            print tag, d,
            sample = ROOT.SH.SampleLocal(tag)
            files = [d+'/'+f for f in os.listdir(d) if f.find('.root')!=-1]
            print len(files), "files"
            for f in files: sample.add(f)
            sh_all.add(sample)
    if options.test:
        exit(0)


# print out the samples we found
logging.info("%d different datasets to be processed", len(sh_all))

# set the name of the tree in our files
sh_all.setMetaString("nc_tree", "CollectionTree")

# this is the basic description of our job
logging.info("creating new job")
job = ROOT.EL.Job()
job.sampleHandler(sh_all)

# add our algorithm to the job
logging.info("creating algorithms")

alg = ROOT.Ewk2LTruthAnalysis()
alg.outputFileName = "myOutput";
alg.isSignal  = options.isSignal;
alg.saveTree  = options.saveTree;
alg.saveHists = options.saveHists;
alg.isRecoSample = options.isRecoSample;
alg.CF_l0_pt = 25000.
alg.CF_l1_pt = 20000.

#output -- done inside the alg
output = ROOT.EL.OutputStream("myOutput")
job.outputAdd(output)
## not needed
# ntuple = ROOT.EL.NTupleSvc("myOutput")
# job.algsAdd(ntuple);

logging.info("adding algorithms")
job.algsAdd(alg)

# job options
job.options().setDouble(ROOT.EL.Job.optMaxEvents, options.nevents)

# make the driver we want to use:
# this one works by running the algorithm directly
logging.info("creating driver")
driver = None
if (options.driver == "direct"):
        logging.info("running on direct")
        driver = ROOT.EL.DirectDriver()
        logging.info("submit job")
        driver.submit(job, options.outputDir)
elif (options.driver == "prooflite"):
        logging.info("running on prooflite")
        driver = ROOT.EL.ProofDriver()
        logging.info("submit job")
        driver.submit(job, options.outputDir)
elif (options.driver == "condor"):
        logging.info("running on condor")
        driver = ROOT.EL.CondorDriver()
        driver.shellInit = "export HOME=$PWD && export PATH=$PATH:$PWD &&  export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase";
#         if options.isShortJob: driver.shellInit += ' && export PATH=~/.tmp_bin/condor_submit:$PATH'
        #&& source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh && cd .. && rcSetup && cd $HOME";
        #job.options().setString(ROOT.EL.Job.optCondorConf, "GetEnv = True");
        job.options().setString(ROOT.EL.Job.optCondorConf, 'requirements = (regexp("atum-n28",Machine)==FALSE)');
        job.options().setDouble(ROOT.EL.Job.optFilesPerWorker, options.nFilesPerNode);
        logging.info("submit job")
#         driver.submit(job, options.outputDir)
        driver.submitOnly(job, options.outputDir)
elif (options.driver == "LSF"):
        logging.info("running on LSF batch")
        driver = ROOT.EL.LSFDriver()
        driver.options().setString (ROOT.EL.Job.optSubmitFlags, "-L /bin/bash");
        driver.shellInit = "export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase && source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh"
        job.options().setDouble(ROOT.EL.Job.optFilesPerWorker, options.nFilesPerNode);
        logging.info("submit job to LSF batch")
        driver.submitOnly(job, options.outputDir)
elif (options.driver == "grid"):
        logging.info("running on Grid")
        driver = ROOT.EL.PrunDriver()
        outname= "user."+os.environ["RUCIO_ACCOUNT"]+"."+ (options.shortName or options.outputTag+options.outputPattern)
#         outname= "user."+os.environ["RUCIO_ACCOUNT"]+"."+ (options.shortName or options.outputTag+".%in:name[2]%.%in:name[3]%")
#         outname= "user."+os.environ["RUCIO_ACCOUNT"]+"."+ (options.shortName or options.outputTag+".%in:name[4]%")
        driver.options().setString("nc_outputSampleName", outname)
        if options.test:
            driver.options().setDouble(ROOT.EL.Job.optGridNFiles, 4)
            driver.options().setDouble(ROOT.EL.Job.optGridNFilesPerJob, 2)
#         driver.options().setDouble("nc_disableAutoRetry", 1)
        logging.info("submit job")
        driver.submitOnly(job, options.outputDir)
