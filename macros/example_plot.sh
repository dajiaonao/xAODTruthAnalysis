#!/bin/bash

var="lepton_n"
#var="${var},isDF"
#var="${var},isSF"
#var="${var},isOS"
#var="${var},lepton_pt[0]"
#var="${var},lepton_eta[0]"
#var="${var},lepton_phi[0]"
#var="${var},lepton_flav[0]"
#var="${var},lepton_type[0]"
#var="${var},lepton_origin[0]"
#var="${var},lepton_pt[1]"
#var="${var},lepton_eta[1]"
#var="${var},lepton_phi[1]"
#var="${var},lepton_flav[1]"
#var="${var},lepton_type[1]"
#var="${var},lepton_origin[1]"
#var="${var},jet_n"
#var="${var},bjet_n"
#var="${var},nonbjet_n"
#var="${var},bjet_pt[0]"
#var="${var},nonbjet_pt[0]"
#var="${var},jet_pt[0]"
#var="${var},jet_eta[0]"
#var="${var},jet_phi[0]"
#var="${var},jet_flav[0]"
#var="${var},bjet_pt[1]"
#var="${var},nonbjet_pt[1]"
#var="${var},jet_pt[1]"
#var="${var},jet_eta[1]"
#var="${var},jet_phi[1]"
#var="${var},jet_flav[1]"
#var="${var},met_et"
#var="${var},met_phi"
#var="${var},r1"
#var="${var},pbll"
#var="${var},mT2ll"
#var="${var},mll"
var="${var},mDRll"
var="${var},RPT"
var="${var},gamInvRp1"
var="${var},DPB_vSS"
var="${var},cosTheta_b"
#var="${var},dphill"
#var="${var},ptll"
#var="${var},dphi_met_pbll"
#var="${var},mcEventWeight"
##var="${var},truth_wbmass[0]"
##var="${var},truth_wbmass[1]"
##var="${var},TMath::Cos(truth_thetal[0])"
##var="${var},TMath::Cos(truth_thetal[1])"
#var="${var},truth_wmass"


#var="truth_wbmass"
#var="${var},TMath::Cos(truth_thetal)"
#var2="truth_wmass"
#var2="${var2},truth_wpt"
#var2="${var2},truth_wbpt"
#var2="${var2},truth_stpt"
#var2="${var2},truth_stmass"
#var2="${var2},truth_ststpt"
#var2="${var2},truth_ststmass"
#var2="${var2},truth_n1pt"
#var2="${var2},truth_n1mass"
#var2="${var2},bjet_n"
#var2="${var2},bjet_pt[0]"
#var2="${var2},nonbjet_n"
#var2="${var2},nonbjet_pt[0]"
#var2="${var2},met_et"

#var2="truth_ststpt"
#var2="${var2},truth_ststphi"
#var2="${var2},truth_n1n1pt"
#var2="${var2},truth_n1n1phi"
#var2="${var2},truth_wbmass"
#var2="${var2},met_et"
#var2="${var2},mT2ll"
#var2="${var2},nonbjet_n"
#var2="${var2},nonbjet_pt[0]"
#var2="${var2},bjet_n"
#var2="${var2},bjet_pt[0]"
#var2="${var2},lepton_pt[0]"
#var2="${var2},truth_wbmass"
#var2="${var2},TMath::Cos(truth_thetal)"

## Stop2L 3-body
#python make_plots.py -i "Sherpa_lvlv,Sherpa_lvlv_fac4,Sherpa_lvlv_fac025,Sherpa_lvlv_renorm4,Sherpa_lvlv_renorm025,Sherpa_lvlv_qsf4,Sherpa_lvlv_qsf025" -v "${var}" -r "Stop2L_CR_VV_noMDR" -f "eps" -l 3210 -b -a -L;
python make_plots.py -i "Powheg_ttbar,Powheg_ttbar_radHi,Powheg_ttbar_radLo,PowhegHpp_ttbar" -v "${var}" -r "Stop2L_CR_Top_noMDR" -f "eps" -l 3210 -b -a -L;

### Sleptons
#var="${var},susyID"
#python make_plots.py -i "MadgraphSlep_100vs1" -v "${var}" -r "VR_SUSY_LEP" -f "eps" -l 1 -b;

### Stop Polarization
##python make_plots.py -i "Herwigpp_300vs180,MadgraphF_300vs180,MadgraphR_300vs180,MadgraphM_300vs180,MadgraphL_300vs180,Madgraph_300vs180" -v "${var}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
##python make_plots.py -i "Herwigpp_300vs180,MadgraphF_300vs180,MadgraphR_300vs180,MadgraphM_300vs180,MadgraphL_300vs180,Madgraph_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "TakashiF_250vs125,TakashiL_250vs125,Takashi_250vs125" -v "${var}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "TakashiF_250vs125,TakashiL_250vs125,Takashi_250vs125" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "Herwigpp_250vs160,MadgraphR_250vs160,Madgraph_250vs160" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "Herwigpp_250vs160,MadgraphR_250vs160,Madgraph_250vs160" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "Herwigpp_300vs150,MadgraphR_300vs150,Madgraph_300vs150" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "Herwigpp_300vs150,MadgraphR_300vs150,Madgraph_300vs150" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "Herwigpp_300vs180,MadgraphF_300vs180,MadgraphT_300vs180,MadgraphR_300vs180,Madgraph_300vs180" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "Herwigpp_300vs180,MadgraphF_300vs180,MadgraphT_300vs180,MadgraphR_300vs180,Madgraph_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "HerwigppL_250vs160,MadgraphL_250vs160,Madgraph_250vs160" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "HerwigppL_250vs160,MadgraphL_250vs160,Madgraph_250vs160" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "HerwigppL_300vs180,MadgraphL_300vs180,Madgraph_300vs180" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "HerwigppL_300vs180,MadgraphL_300vs180,Madgraph_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "HerwigppR_300vs180,HerwigppL_300vs180" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "HerwigppR_300vs180,HerwigppL_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "HerwigppR_300vs180,MadgraphFR_300vs180" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "HerwigppR_300vs180,MadgraphT_300vs180,MadgraphFR_300vs180,MadgraphR_300vs180,Madgraph_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 

#python make_plots.py -i "MadgraphFL_250vs125,MadgraphL_250vs125,Madgraph_250vs125,HerwigppL_250vs125,SerhanFL_250vs125" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "MadgraphFR_300vs180,MadgraphR_300vs180,Madgraph_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 

#python make_plots.py -i "SerhanFL_250vs125,MadgraphL_250vs125,Madgraph_250vs125" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "SerhanFR_250vs125,MadgraphR_250vs125,Madgraph_250vs125" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "SerhanFL_250vs125,MadgraphFL_250vs125" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "Madgraph_250vs125,MadgraphL_250vs125,MadgraphR_250vs125,MadgraphM_250vs125" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "SerhanFR_250vs125,SerhanFL_250vs125" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 

#python make_plots.py -i "HerwigppR_300vs180,MadgraphFR_300vs180,MadgraphR_300vs180,Madgraph_300vs180" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "HerwigppR_300vs180,MadgraphFR_300vs180,MadgraphR_300vs180,Madgraph_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "HerwigppL_300vs180,MadgraphL_300vs180,Madgraph_300vs180" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "HerwigppL_300vs180,MadgraphL_300vs180,Madgraph_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 
#python make_plots.py -i "MadgraphM_300vs180,MadgraphR_300vs180,MadgraphL_300vs180" -v "${var}"  -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a; 
#python make_plots.py -i "MadgraphM_300vs180,MadgraphR_300vs180,MadgraphL_300vs180" -v "${var2}" -r "VR_STOP2L_INC" -f "eps" -l 10000 -b -a -L; 

### Dibosons
##python make_plots.py -i "Sherpa_lvlv,Powheg_WWlvlv,Powheg_ZZllvv" -g "0,1+2" -v "${var}" -r "CR_SF,CR_DF" -f "eps" -L -b -a;
##python make_plots.py -i "Sherpa_lvlv,Powheg_WWlvlv,Powheg_ZZllvv" -g "0,1+2" -v "${var}" -r "SR_ALL_NOMT2_NOR1" -f "DB.eps" -L -b -a;
##python make_plots.py -i "Sherpa_lvlv,Sherpa_lvlv_fac4,Sherpa_lvlv_fac025,Sherpa_lvlv_renorm4,Sherpa_lvlv_renorm025,Sherpa_lvlv_qsf4,Sherpa_lvlv_qsf025" -v "${var}" -r "SR_SF_NOMT2,SR_DF_NOMT2" -f "eps" -L -b -a;

### TTbar
##python make_plots.py -i "Powheg_ttbar,aMCatNLO_ttbar" -v "${var}" -r "CR_TOP" -f "eps" -L -b -a;
##python make_plots.py -i "Powheg_ttbar,aMCatNLO_ttbar" -v "${var}" -r "SR_ALL_NOMT2_NOR1" -f "TOP.eps" -L -b -a;
##python make_plots.py -i "Powheg_ttbar,Powheg_ttbar_radHi,Powheg_ttbar_radLo,aMCatNLO_ttbar,PowhegHpp_ttbar" -v "${var}" -r "SR_ALL_NOMT2" -f "eps" -L -b -a;

### WW and TTbar
##python make_plots.py -i "Powheg_ttbar,Powheg_WWlvlv" -v "mT2ll,mll,r1,lepton_type[0],lepton_type[1],lepton_origin[0],lepton_origin[1]" -r "SR_SF_NOMT2_NOR1,SR_DF_NOMT2_NOR1" -f "TOPvsDB.eps" -L -b -a;
##python make_plots.py -i "Powheg_ttbar,Powheg_WWlvlv" -v "${var}" -r "SR_SF,SR_DF" -f "TOPvsDB.eps" -L -b -a;
