# xAODTruthAnalysis

Minimal instructions to run as of 30.05.2016:

Setup
=====
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase 

source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

rcSetup Base,2.3.49 # these three steps need to be done in every fresh start

kinit $USER@CERN.CH # Given $USER and lxplus accounts match, to avoid typing password everytime

svn co svn+ssh://svn.cern.ch/reps/atlasphys-susy/Physics/SUSY/Analyses/StopSbottom/StopPolarization/tags/StopPolarization-00-01-03 StopPolarization

git clone https://github.com/amete/xAODTruthAnalysis.git

rc find_packages

rc compile


Run
=====
Three analyses are defined: {runEwk2LTruth, runStop2LTruth, runStrongSS3LTruth} change $exec as needed below:


$exec -i input_dir -o output_dir --options # for each available option do $exec -h

If output trees are requested, these will appear under output_dir.

These trees can be analyzed simply in ROOT. 

There are some macros under macros/ folder that might simplify this step.

