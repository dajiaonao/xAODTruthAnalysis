#!/bin/bash
var="lepton_n"
var="${var},lepton_pt[0]"
var="${var},lepton_eta[0]"
var="${var},lepton_phi[0]"
var="${var},lepton_flav[0]"
var="${var},lepton_type[0]"
var="${var},lepton_origin[0]"
var="${var},lepton_pt[1]"
var="${var},lepton_eta[1]"
var="${var},lepton_phi[1]"
var="${var},lepton_flav[1]"
var="${var},lepton_type[1]"
var="${var},lepton_origin[1]"
var="${var},jet_n"
var="${var},jet_pt[0]"
var="${var},jet_eta[0]"
var="${var},jet_phi[0]"
var="${var},jet_flav[0]"
var="${var},jet_pt[1]"
var="${var},jet_eta[1]"
var="${var},jet_phi[1]"
var="${var},jet_flav[1]"
var="${var},met_et"
var="${var},met_phi"
var="${var},r1"
var="${var},pbll"
var="${var},mT2ll"
var="${var},mll"
var="${var},dphi_met_pbll"

# Dibosons
#python make_plots.py -i "Sherpa_lvlv,Powheg_WWlvlv,Powheg_ZZllvv" -g "0,1+2" -v "${var}" -r "CR_SF,CR_DF" -f "eps" -L -b -a;
#python make_plots.py -i "Sherpa_lvlv,Powheg_WWlvlv,Powheg_ZZllvv" -g "0,1+2" -v "${var}" -r "SR_ALL_NOMT2_NOR1" -f "DB.eps" -L -b -a;

# TTbar
#python make_plots.py -i "Powheg_ttbar,aMCatNLO_ttbar" -v "${var}" -r "CR_TOP" -f "eps" -L -b -a;
#python make_plots.py -i "Powheg_ttbar,aMCatNLO_ttbar" -v "${var}" -r "SR_ALL_NOMT2_NOR1" -f "TOP.eps" -L -b -a;
python make_plots.py -i "Powheg_ttbar,Powheg_ttbar_radHi,Powheg_ttbar_radLo,aMCatNLO_ttbar,PowhegHpp_ttbar" -v "mT2ll" -r "SR_ALL_NOMT2" -f "eps" -L -b -a;

# WW and TTbar
#python make_plots.py -i "Powheg_ttbar,Powheg_WWlvlv" -v "mT2ll,mll,r1,lepton_type[0],lepton_type[1],lepton_origin[0],lepton_origin[1]" -r "SR_SF_NOMT2_NOR1,SR_DF_NOMT2_NOR1" -f "TOPvsDB.eps" -L -b -a;
#python make_plots.py -i "Powheg_ttbar,Powheg_WWlvlv" -v "${var}" -r "SR_SF,SR_DF" -f "TOPvsDB.eps" -L -b -a;