#!/bin/bash
if [[ "${1}" == "Grid" ]]; then
    ## Diboson
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.361600.PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_WWlvlv.merge.DAOD_TRUTH1.e4054_p2436/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.361604.PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_ZZvvll_mll4.merge.DAOD_TRUTH1.e4054_p2436/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.361068.Sherpa_CT10_llvv.merge.DAOD_TRUTH1.e3836_p2436/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363072.Sherpa_CT10_llvv_fac4.merge.DAOD_TRUTH1.e4681_p2482/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363073.Sherpa_CT10_llvv_fac025.merge.DAOD_TRUTH1.e4681_p2482/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363074.Sherpa_CT10_llvv_renorm4.merge.DAOD_TRUTH1.e4681_p2482/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363075.Sherpa_CT10_llvv_renorm025.merge.DAOD_TRUTH1.e4681_p2482/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363076.Sherpa_CT10_llvv_qsf4.merge.DAOD_TRUTH1.e4681_p2482/;
    #out="$(($(date +%s)-T))"
    #runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.363077.Sherpa_CT10_llvv_qsf025.merge.DAOD_TRUTH1.e4681_p2482/;
    # Top
    out="$(($(date +%s)-T))"
    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.merge.DAOD_TRUTH1.e3698_p2436/;
    out="$(($(date +%s)-T))"
    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410001.PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad.merge.DAOD_TRUTH1.e3783_p2425/;
    out="$(($(date +%s)-T))"
    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410002.PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad.merge.DAOD_TRUTH1.e3783_p2425/;
    out="$(($(date +%s)-T))"
    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410003.aMcAtNloHerwigppEvtGen_ttbar_nonallhad.merge.DAOD_TRUTH1.e4441_p2425/;
    out="$(($(date +%s)-T))"
    runStop2LTruth --saveTree --submitToGrid -t flat_v1 -o ${out} -i mc15_13TeV.410004.PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad.merge.DAOD_TRUTH1.e3836_p2425/;
elif [[ "${1}" == "Local" ]]; then
    #runStop2LTruth --saveTree -o "mc15_13TeV.361600" -i /gdata/atlas/amete/MC15_ModelingUncertainties/TRUTH1/mc15_13TeV.361600/ -sP "*000001*" -n 10000;
    #runStop2LTruth --saveTree -o "mc15_13TeV.361604" -i /gdata/atlas/amete/MC15_ModelingUncertainties/TRUTH1/mc15_13TeV.361604/; #-sP "*000001*" -n 200000;
    #runStop2LTruth --saveTree -o "mc15_13TeV.361068" -i /gdata/atlas/amete/MC15_ModelingUncertainties/TRUTH1/mc15_13TeV.361068/; #-sP "*06923433._000001*" -n 100;
    #runStop2LTruth --saveTree -o "Herwigpp.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/user.amete.mc15_13TeV.406011.TRUTH1.e4107_EXT0;
    #runStop2LTruth --saveTree -o "Madgraph.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/123456 -sD 1;
    #runStop2LTruth --saveTree -o "MadgraphR.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/123456 -sD 1;
    runStop2LTruth --saveTree -o "MadgraphL.300vs180" -i /gdata/atlas/amete/StopPolarization/outputs/DAOD/123456 -sD 1;
else
    echo "Unknown mode..."
fi
