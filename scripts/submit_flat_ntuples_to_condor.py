#!/bin/env python
import os
import sys
import glob
import subprocess

ana_name            = "runStop2LTruth"
tar_location        = "/data/uclhc/uci/user/amete/"
out_dir             = "/data/uclhc/uci/user/amete/truth_analysis_run/outputs_2/" 
log_dir             = "/data/uclhc/uci/user/amete/truth_analysis_run/logs_2/" 
tarred_dir          = "truth_analysis/"
filelist_dir        = "/data/uclhc/uci/user/amete/truth_analysis/inputs/"
in_job_filelist_dir = "/truth_analysis/inputs/"

samples = ["sample_list_split"]

doBrick = False
doLocal = True 
doSDSC  = True 
doUC    = True 

def main():
    print "SubmitCondorSF"

    look_for_condor_executable()

    for s in samples :
        if s.startswith('#') : continue
        print "Submtting sample : %s"%s
        suff = ""
        if not s.endswith("/") : suff = "/"
        sample_lists = glob.glob(filelist_dir + s + suff + "*.txt")
        if len(sample_lists) == 0 :
            print "No sample lists in filelist dir!"
            sys.exit()

        for dataset in sample_lists :
            fullname = str(os.path.abspath(dataset))
            print "    > %s"%dataset

            dataset = "." + dataset[dataset.find(in_job_filelist_dir):]
            print "    >> %s"%dataset

            if not (str(os.path.abspath(out_dir)) == str(os.environ['PWD'])) :
                print "You must call this script from the output directory where the ntuples will be stored!"
                print " >>> Expected submission directory : %s"%os.path.abspath(out_dir)
                sys.exit()

            output_folder="out_%s"%(dataset.split("/")[len(dataset.split("/"))-1].split(".")[1])
            look_for_condor_script(brick_ = doBrick, local_ = doLocal, sdsc_ = doSDSC, uc_ = doUC, out_ = output_folder)

            run_cmd = "ARGS="
            run_cmd += '"'
            run_cmd += ' %s '%out_dir
            run_cmd += ' %s '%log_dir
            run_cmd += ' %s '%ana_name
            run_cmd += ' %s '%tarred_dir
            run_cmd += ' %s '%dataset
            run_cmd += ' -o %s --saveTree --submitToCondor' % (output_folder) # Additional options 
            run_cmd += '"'
            run_cmd += ' condor_submit submitFile_%s.condor '%(output_folder)
            lname = dataset.split("/")[-1].replace(".txt", "")
            run_cmd += ' -append "transfer_input_files = %s" '%(tar_location + "truth_area.tgz")
            run_cmd += ' -append "output = %s%s" '%(log_dir, lname + ".out")
            run_cmd += ' -append "log = %s%s" '%(log_dir, lname + ".log")
            run_cmd += ' -append "error = %s%s" '%(log_dir, lname + ".err")

            print run_cmd
            subprocess.call(run_cmd, shell=True)

def look_for_condor_script(brick_ = False, local_ = False, sdsc_ = False, uc_ = False, out_ = "") :

    brick = 'false'
    local = 'false'
    sdsc  = 'false'
    uc    = 'false'
    if brick_ : brick = 'true'
    if local_ : local = 'true'
    if sdsc_  : sdsc = 'true'
    if uc_    : uc = 'true'

    f = open('submitFile_%s.condor'%(out_), 'w')
    f.write('universe = vanilla\n')
    f.write('+local=%s\n'%brick_)
    f.write('+site_local=%s\n'%local_)
    f.write('+sdsc=%s\n'%sdsc_)
    f.write('+uc=%s\n'%uc_)
    f.write('executable = RunCondorSF.sh\n')
    f.write('arguments = $ENV(ARGS)\n')
    f.write('should_transfer_files = YES\n')
    f.write('transfer_output_files = %s\n'%(out_))
    f.write('when_to_transfer_output = ON_EXIT\n')
    f.write('use_x509userproxy = True\n')
    f.write('notification = Never\n')
    f.write('queue\n')
    f.close()

def look_for_condor_executable() :
    f = open('RunCondorSF.sh', 'w') 
    f.write('#!/bin/bash\n\n\n')
    f.write('echo " ------- RunCondorSF -------- "\n')
    f.write('output_dir=${1}\n')
    f.write('log_dir=${2}\n')
    f.write('exec=${3}\n')
    f.write('stored_dir=${4}\n')
    f.write('input=${5}\n')
    f.write('options=${@:6}\n\n')
    f.write('echo "    output directory   : ${output_dir}"\n')
    f.write('echo "    log directory      : ${log_dir}"\n')
    f.write('echo "    sflow executable   : ${exec}"\n')
    f.write('echo "    tarred dir         : ${stored_dir}"\n')
    f.write('echo "    sample list        : ${input}"\n')
    f.write('echo "    sflow options      : ${options}"\n\n')
    f.write('while (( "$#" )); do\n')
    f.write('    shift\n')
    f.write('done\n\n')
    f.write('work_dir=${PWD}\n')
    f.write('echo "untarring truth_area.tgz"\n')
    f.write('tar -xzf truth_area.tgz\n\n')
    f.write('echo "done untarring"\n')
    f.write('echo "current directory structure:"\n')
    f.write('ls -ltrh\n\n')
    f.write('export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase\n')
    f.write('source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh\n')
    f.write('echo "Calling : cd ${stored_dir}"\n')
    f.write('cd ${stored_dir}\n')
    f.write('echo "Directory structure:"\n')
    f.write('ls -ltrh\n')
    f.write('lsetup fax\n')
    f.write('source setup_release.sh\n')
    #f.write('echo "Calling : source RootCore/local_setup.sh"\n')
    #f.write('source RootCore/local_setup.sh\n')
    f.write('echo "Calling : cd xAODTruthAnalysis/scripts"\n')
    f.write('cd xAODTruthAnalysis/scripts\n')
    f.write('source setRestFrames.sh\n')
    f.write('echo "Calling : cd ${work_dir}"\n')
    f.write('cd ${work_dir}\n')
    f.write('echo "Calling : ${exec} -i ${input} ${options}"\n')
    f.write('${exec} -i ${input} ${options}\n')
    f.write('echo "final directory structure:"\n')
    f.write('ls -ltrh\n')
    f.close()

if __name__=="__main__" :
    main()

#if [[ "${1}" == "Grid" ]]; then
#    ## Diboson
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.361600.PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_WWlvlv.merge.DAOD_TRUTH1.e4054_p2436/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.361604.PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_ZZvvll_mll4.merge.DAOD_TRUTH1.e4054_p2436/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.361068.Sherpa_CT10_llvv.merge.DAOD_TRUTH1.e3836_p2436/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363072.Sherpa_CT10_llvv_fac4.merge.DAOD_TRUTH1.e4681_p2482/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363073.Sherpa_CT10_llvv_fac025.merge.DAOD_TRUTH1.e4681_p2482/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363074.Sherpa_CT10_llvv_renorm4.merge.DAOD_TRUTH1.e4681_p2482/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363075.Sherpa_CT10_llvv_renorm025.merge.DAOD_TRUTH1.e4681_p2482/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363076.Sherpa_CT10_llvv_qsf4.merge.DAOD_TRUTH1.e4681_p2482/;
#    #out="$(($(date +%s)-T))"
#    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363077.Sherpa_CT10_llvv_qsf025.merge.DAOD_TRUTH1.e4681_p2482/;
#    # Top
#    out="$(($(date +%s)-T))"
#    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.merge.DAOD_TRUTH1.e3698_p2436/;
#    out="$(($(date +%s)-T))"
#    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410001.PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad.merge.DAOD_TRUTH1.e3783_p2425/;
#    out="$(($(date +%s)-T))"
#    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410002.PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad.merge.DAOD_TRUTH1.e3783_p2425/;
#    out="$(($(date +%s)-T))"
#    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410003.aMcAtNloHerwigppEvtGen_ttbar_nonallhad.merge.DAOD_TRUTH1.e4441_p2425/;
#    out="$(($(date +%s)-T))"
#    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410004.PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad.merge.DAOD_TRUTH1.e3836_p2425/;
#elif [[ "${1}" == "Local" ]]; then
#    #runStop2LTruth --saveTree -o "mc15_13TeV.361600" -i /gdata/atlas/amete/MC15_ModelingUncertainties/TRUTH1/mc15_13TeV.361600/ -sP "*000001*" -n 10000;
#    #runStop2LTruth --saveTree -o "mc15_13TeV.361604" -i /gdata/atlas/amete/MC15_ModelingUncertainties/TRUTH1/mc15_13TeV.361604/; #-sP "*000001*" -n 200000;
#    #runStop2LTruth --saveTree -o "mc15_13TeV.361068" -i /gdata/atlas/amete/MC15_ModelingUncertainties/TRUTH1/mc15_13TeV.361068/; #-sP "*06923433._000001*" -n 100;
#    #runStop2LTruth --saveTree -o "Herwigpp.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/user.amete.mc15_13TeV.406011.TRUTH1.e4107_EXT0;
#    #runStop2LTruth --saveTree -o "Madgraph.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/123456 -sD 1;
#    #runStop2LTruth --saveTree -o "MadgraphR.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/123456 -sD 1;
#    runStop2LTruth --saveTree -o "MadgraphL.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/123456 -sD 1;
#else
#    echo "Unknown mode..."
#fi


