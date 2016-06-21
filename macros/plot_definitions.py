import ROOT,math,array

# Define the input ROOT files
def getROOTFileName(filename):
    return {
        "Sherpa_lvlv"          : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_361068.root",
        "Sherpa_lvlv_fac4"     : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_363072.root",
        "Sherpa_lvlv_fac025"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_363073.root",
        "Sherpa_lvlv_renorm4"  : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_363074.root",
        "Sherpa_lvlv_renorm025": "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_363075.root",
        "Sherpa_lvlv_qsf4"     : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_363076.root",
        "Sherpa_lvlv_qsf025"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_363077.root",
        "Powheg_WWlvlv"        : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_361600.root",
        "Powheg_ZZllvv"        : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_361604.root",
        "Powheg_ttbar"         : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_410000.root",
        "Powheg_ttbar_radHi"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_410001.root",
        "Powheg_ttbar_radLo"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_410002.root",
        "aMCatNLO_ttbar"       : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_410003.root",
        "PowhegHpp_ttbar"      : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_2/out_410004.root",
        #"Herwigpp_300vs180"    : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/Herwigpp.300vs180.truth1_v3.root",
        #"Madgraph_300vs180"    : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/Madgraph.300vs180.truth1_v3.root",
        #"MadgraphR_300vs180"   : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/MadgraphR.300vs180.truth1_v3.root",
        #"MadgraphL_300vs180"   : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/MadgraphL.300vs180.truth1_v3.root",
        "Herwigpp_250vs160"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_406009.HppEG_UE5C6L1_Tt_bWN_t250_n160_2Lep18.root",
        "HerwigppL_250vs160"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_999999.HppEG_UE5C6L1_Tt_bWN_t250_n160_2Lep18.root",
        "Madgraph_250vs160"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387943.MGPy8EG_A14N23LO_TT_bWN_250_160_2L15.root",
        "MadgraphL_250vs160"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387943.MGPy8EG_A14N23LO_TT_bWN_250_160_2L15.root",
        "MadgraphR_250vs160"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387943.MGPy8EG_A14N23LO_TT_bWN_250_160_2L15.root",
        "Herwigpp_300vs150"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_406010.HppEG_UE5C6L1_Tt_bWN_t300_n150_2Lep18.root",
        "Madgraph_300vs150"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387947.MGPy8EG_A14N23LO_TT_bWN_300_150_2L15.root",
        "MadgraphR_300vs150"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387947.MGPy8EG_A14N23LO_TT_bWN_300_150_2L15.root",
        "HerwigppR_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_406011.HppEG_UE5C6L1_Tt_bWN_t300_n180_2Lep18.root",
        "HerwigppL_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_999998.HppEG_UE5C6L1_Tt_bWN_t300_n180_2Lep18.root",
        "Madgraph_300vs180"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
        "MadgraphM_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
        "MadgraphR_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
        "MadgraphL_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
        "MadgraphFR_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123457.MGPy8EG_A14N_TTright_bWN_300_180_2Lep18.root",
        "MadgraphT_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123458.MGPy8EG_A14N_TTright_bWN_300_180_2Lep18.root",
        "MadgraphFL_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999927.MGPy8EG_A14N23LO_TT_directBWNleft_250_125.root",
        "MadgraphL_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
        "MadgraphM_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
        "MadgraphR_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
        "Madgraph_250vs125"     : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
        "HerwigppL_250vs125"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_999997.HppEG_UE5C6L1_Tt_bWN_t250_n125_2Lep18.root",
        "SerhanFL_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123460.MGPy8EG_A14N_TTleft_bWN_250_125_2Lep18.root",
        "SerhanFR_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123461.MGPy8EG_A14N_TTright_bWN_250_125_2Lep18.root",
        #"MadgraphSlep_100vs1"  : "/gdata/atlas/amete/MC15_SleptonPairProduction/FLAT/DAOD_TRUTH1.MGPy8EG_A14N23LO_SlepSlep_direct_100p0_1p0_2L5_10k.pool.root",
        "MadgraphSlep_100vs1"  : "/data/uclhc/uci/user/amete/slepton_signal_flat/DAOD_TRUTH1.MGPy8EG_A14N23LO_SlepSlep_direct_100p0_1p0_2L5_10k.pool.root",
    }.get(filename,"")

# Define cross-sections
def getCrossSection(filename):
    return {
        "Sherpa_lvlv"          : 14.022*0.91,  # 361068 https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MC15SystematicUncertainties#VV_Diboson_V_W_Z 24/11/15
        "Sherpa_lvlv_fac4"     : 14.022*0.91,  # 363072
        "Sherpa_lvlv_fac025"   : 14.022*0.91,  # 363073
        "Sherpa_lvlv_renorm4"  : 14.022*0.91,  # 363074
        "Sherpa_lvlv_renorm025": 14.022*0.91,  # 363075
        "Sherpa_lvlv_qsf4"     : 14.022*0.91,  # 363076
        "Sherpa_lvlv_qsf025"   : 14.022*0.91,  # 363077
        "Powheg_WWlvlv"        : 10.631,       # 361600
        "Powheg_ZZllvv"        : 0.92498,      # 361604
        "Powheg_ttbar"         : 831.76*0.543, # 410000
        "Powheg_ttbar_radHi"   : 831.76*0.543, # 410001
        "Powheg_ttbar_radLo"   : 831.76*0.543, # 410002
        "aMCatNLO_ttbar"       : 831.76*0.543, # 410003
        "PowhegHpp_ttbar"      : 831.76*0.543, # 410004
        "Herwigpp_250vs160"    : 21.5949*0.040720, # Official 
        "Madgraph_250vs160"    : 21.5949*0.048089, # Official
        "MadgraphL_250vs160"   : 21.5949*0.048089, # Official
        "MadgraphR_250vs160"   : 21.5949*0.048089, # Official
        "Herwigpp_300vs150"    : 8.51615*0.061771, # Official
        "Madgraph_300vs150"    : 8.51615*0.078449, # Official
        "MadgraphR_300vs150"   : 8.51615*0.078449, # Official
        "HerwigppR_300vs180"   : 8.51615*0.047643, # Official 
        "Madgraph_300vs180"    : 8.51615*0.060136, # Official
        "MadgraphM_300vs180"   : 8.51615*0.060136, # Official
        "MadgraphR_300vs180"   : 8.51615*0.060136, # Official
        "MadgraphL_300vs180"   : 8.51615*0.060136, # Official
        "MadgraphFR_300vs180"  : 8.51615*0.216*0.216*0.7123521869, # Private
        "MadgraphT_300vs180"   : 8.51615*0.216*0.216*0.7150234369, # Private
        "HerwigppL_250vs160"   : 21.5949*0.04002850029, # Private
        "HerwigppL_300vs180"   : 8.51615*0.04516371848, # Private
        "Madgraph_250vs125"    : 1,  # Dummy
        "MadgraphM_250vs125"   : 1,  # Dummy
        "MadgraphL_250vs125"   : 1,  # Dummy
        "MadgraphR_250vs125"   : 1,  # Dummy
        "MadgraphFL_250vs125"  : 1,  # Dummy
        "HerwigppL_250vs125"   : 1,  # Dummy
        "SerhanFL_250vs125"    : 1,  # Dummy
        "SerhanFR_250vs125"    : 1,  # Dummy
        "MadgraphSlep_100vs1"  : 1,  # Dummy
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
        "bjet_n"          : "Number of bjets", 
        "nonbjet_n"       : "Number of nonbjets", 
        "bjet_pt[0]"      : "Leading bjet p_{T} [GeV]", 
        "bjet_pt[1]"      : "Subleading bjet p_{T} [GeV]",
        "nonbjet_pt[0]"   : "Leading nonbjet p_{T} [GeV]", 
        "nonbjet_pt[1]"   : "Subleading nonbjet p_{T} [GeV]",
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
        "ptll"            : "p_{T}(ll) [GeV]",
        "mll"             : "m(ll) [GeV]",
        "mDRll"           : "E_{V}^{P} [GeV]",
        "RPT"             : "R_{PT}",
        "gamInvRp1"       : "1/#gamma_{P}^{PP}",
        "DPB_vSS"         : "#Delta#phi(#beta_{PP}^{LAB},p_{V}^{PP})",
        "cosTheta_b"      : "cos#theta_{b}",
        "isDF"            : "isDF",
        "isSF"            : "isSF",
        "isOS"            : "isOS",
        "r1"              : "R1",
        "dphi_met_pbll"   : "#Delta#phi(MET,Pbll)",
        "dphill"          : "#Delta#phi(l,l)",
        "mcEventWeight"   : "MC event weight",
        "susyID"          : "SUSY ID",
        "truth_ststpt"    : "Pt of the stop-pair [GeV]",
        "truth_ststphi"   : "#Delta#phi of the stop-pair",
        "truth_ststmass"  : "Mass of the stop-pair [GeV]",
        "truth_n1n1pt"    : "Pt of the neutralino-pair [GeV]",
        "truth_n1n1phi"   : "#Delta#phi of the neutralino-pair",
        "truth_n1n1mass"  : "Mass of the neutralino-pair [GeV]",
        "truth_stpt"      : "Pt of the stop [GeV]",
        "truth_stpt[0]"   : "Pt of the first stop [GeV]",
        "truth_stpt[1]"   : "Pt of the second stop [GeV]",
        "truth_stmass"    : "Mass of the stop [GeV]",
        "truth_stmass[0]" : "Mass of the first stop [GeV]",
        "truth_stmass[1]" : "Mass of the second stop [GeV]",
        "truth_n1pt"      : "Pt of the neutralino [GeV]",
        "truth_n1pt[0]"   : "Pt of the first neutralino [GeV]",
        "truth_n1pt[1]"   : "Pt of the second neutralino [GeV]",
        "truth_n1mass"    : "Mass of the neutralino [GeV]",
        "truth_n1mass[0]" : "Mass of the first neutralino [GeV]",
        "truth_n1mass[1]" : "Mass of the second neutralino [GeV]",
        "truth_wbpt"      : "Pt of the W+b system [GeV]",
        "truth_wbpt[0]"   : "Pt of the first W+b system [GeV]",
        "truth_wbpt[1]"   : "Pt of the second W+b system [GeV]",
        "truth_wbmass"    : "Mass of the W+b system [GeV]",
        "truth_wbmass[0]" : "Mass of the first W+b system [GeV]",
        "truth_wbmass[1]" : "Mass of the second W+b system [GeV]",
        "truth_wpt"       : "Pt of the W [GeV]",
        "truth_wpt[0]"    : "Pt of the first W [GeV]",
        "truth_wpt[1]"    : "Pt of the second W [GeV]",
        "truth_wmass"     : "Mass of the W [GeV]",
        "truth_wmass[0]"  : "Mass of the first W [GeV]",
        "truth_wmass[1]"  : "Mass of the second W [GeV]",
        "TMath::Cos(truth_thetal)"    : "cos#theta",
        "TMath::Cos(truth_thetal[0])" : "cos#theta of the first system",
        "TMath::Cos(truth_thetal[1])" : "cos#theta of the second system",
    }.get(variable,"N/A") # N/A is default if variable is not found

# Define region cuts
def getRegionTCut(region):
    # Stop2L regions
    isOSDF          = "(@lepton_pt.size()==2&&isDF&&isOS&&lepton_pt[0]>20.&&lepton_pt[1]>20.&&(lepton_type[0]==2||lepton_type[0]==6)&&(lepton_type[1]==2||lepton_type[1]==6))"
    isOSSF          = "(@lepton_pt.size()==2&&isSF&&isOS&&lepton_pt[0]>20.&&lepton_pt[1]>20.&&(lepton_type[0]==2||lepton_type[0]==6)&&(lepton_type[1]==2||lepton_type[1]==6))"
    zVeto           = "(TMath::Abs(mll-91.2)>10.)"
    bVeto           = "(@bjet_pt.size()==0)"
    bSelection      = "(@bjet_pt.size()>0)"
    commonSRCuts    = "(RPT>0.5&&gamInvRp1>0.8&&DPB_vSS>(0.85*TMath::Abs(cosTheta_b)+1.8))" 
    commonPreSRCuts = "(RPT>0.5&&gamInvRp1>0.8)" 
    return {
        # Actual regions
        "ST2L_SRw_SF"       : "(" + isOSSF + "&&" + commonSRCuts + "&&mDRll>95.&&"  + bVeto      + "&&" + zVeto + ")",
        "ST2L_SRw_DF"       : "(" + isOSDF + "&&" + commonSRCuts + "&&mDRll>95.&&"  + bVeto      + ")",
        "ST2L_SRt_SF"       : "(" + isOSSF + "&&" + commonSRCuts + "&&mDRll>110.&&" + bSelection + "&&" + zVeto + ")",
        "ST2L_SRt_DF"       : "(" + isOSDF + "&&" + commonSRCuts + "&&mDRll>110.&&" + bSelection + ")",
        "ST2L_CR_Top"       : "(" + isOSDF + "&&" + bSelection   + "&&mDRll>80.&&RPT>0.5&&DPB_vSS<(0.85*TMath::Abs(cosTheta_b)+1.8))",
        "ST2L_CR_VV"        : "(" + isOSDF + "&&" + bVeto        + "&&mDRll>30.&&RPT>0.2&&RPT<0.5&&gamInvRp1>0.8&&DPB_vSS<(0.85*TMath::Abs(cosTheta_b)+1.8))",
        # For modeling
        "ST2L_preSRw_SF"    : "(" + isOSSF + "&&" + commonPreSRCuts + "&&mDRll>95.&&" + bVeto      + "&&" + zVeto + ")",
        "ST2L_preSRw_DF"    : "(" + isOSDF + "&&" + commonPreSRCuts + "&&mDRll>95.&&" + bVeto      + ")",
        "ST2L_preSRt_SF"    : "(" + isOSSF + "&&" + commonPreSRCuts + "&&mDRll>95.&&" + bSelection + "&&" + zVeto + ")",
        "ST2L_preSRt_DF"    : "(" + isOSDF + "&&" + commonPreSRCuts + "&&mDRll>95.&&" + bSelection + ")",
        # For plotting
        "ST2L_preCR_VV_DF"   : "(" + isOSDF + "&&" + bVeto        + ")",
        "ST2L_preCR_VV_SF"   : "(" + isOSSF + "&&" + bVeto        + ")",
        "ST2L_noEvp_SRw_ALL" : "((" + isOSSF + "||" + isOSDF + ")&&"  + commonPreSRCuts   + "&&" + bVeto      + "&&" + zVeto + ")",
        "ST2L_noEvp_SRw_SF"  : "("  + isOSSF + "&&" + commonPreSRCuts + "&&" + bVeto      + "&&" + zVeto + ")",
        "ST2L_noEvp_SRw_DF"  : "("  + isOSDF + "&&" + commonPreSRCuts + "&&" + bVeto      + ")",
        "ST2L_noEvp_SRt_ALL" : "((" + isOSSF + "||" + isOSDF + ")&&"  + commonPreSRCuts   + "&&" + bSelection + "&&" + zVeto + ")",
        "ST2L_noEvp_SRt_SF"  : "("  + isOSSF + "&&" + commonPreSRCuts + "&&" + bSelection + "&&" + zVeto + ")",
        "ST2L_noEvp_SRt_DF"  : "("  + isOSDF + "&&" + commonPreSRCuts + "&&" + bSelection + ")",
        ###############
        "SR_ALL_TOP"    : "(isDF || (isSF && (mll<71.||mll>111.)) ) && mll > 20. && mT2ll>100.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_ALL_NOMT2"  : "(isDF || (isSF && (mll<71.||mll>111.)) ) && mll > 20. && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_SF_NOMT2"   : "(isSF && (mll<71.||mll>111.)) && mll > 20. && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_DF_NOMT2"   : "isDF && mll > 20. && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_ALL"        : "(isDF || (isSF && (mll<71.||mll>111.)) ) && mll > 20. && mT2ll>145.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "SR_SF"         : "isSF && mll > 20. && (mll<71.||mll>111.) && mT2ll>145.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "CR_SF"         : "isSF && mll > 20. && (mT2ll>60.  && mT2ll<110.) && pbll<20. && r1>0.4 && TMath::Abs(dphi_met_pbll)<1.5 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_SF"         : "isSF && (mll>71.&&mll<111.) && mT2ll>110. && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "SR_DF"         : "isDF && mll > 20. && mT2ll>145.0 && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)" ,
        "CR_DF"         : "isDF && mll > 20. && (mT2ll>60.  && mT2ll<110.) && pbll<20. && r1>0.4 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_DF"         : "isDF && mll > 20. && (mT2ll>110. && mT2ll<145.) && r1>0.3 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_DF_2"       : "isDF && mll > 20. && (mT2ll>40.  && mT2ll<60. ) && pbll<20. && r1>0.4 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "CR_TOP"        : "isDF && mll > 20. && (mT2ll>60.  && mT2ll<110.) && pbll>30. && r1<0.4 && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_DF_INC"     : "isDF && lepton_pt[0]>20. && lepton_pt[1]>20. && mll>20. && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_SF_INC"     : "isSF && lepton_pt[0]>20. && lepton_pt[1]>20. && mll>20. && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        #"VR_STOP_INC"  : "(@nonbjet_pt.size()==0 || (@nonbjet_pt.size()==1 && nonbjet_pt[0] < 200. && nonbjet_pt[0] > 50.)) && lepton_pt[0]>20. && lepton_pt[1]>20. && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6) ",
        "VR_STOP_NOHISR": "isNOHISR && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6) ",
        "VR_STOP2L_INC" : "isOS && lepton_pt[0]>20. && lepton_pt[1]>20. && (lepton_type[0]==2||lepton_type[0]==6) && (lepton_type[1]==2||lepton_type[1]==6)",
        "VR_SUSY_LEP"   : "@lepton_pt.size()==3"
    }.get(region,"1") # 1 is default if region is not found

# Define histogram bins
def getBinInformation(variable):
    return {
        "lepton_n"      : [ 10, 0,  10],
        "jet_n"         : [ 20, 0,  20],
        "bjet_n"        : [ 20, 0,  20],
        "nonbjet_n"     : [ 20, 0,  20],
        "lepton_pt"     : [ 25, 0, 250], 
        "bjet_pt"       : [ 25, 0, 250], 
        "nonbjet_pt"    : [ 30, 0, 750], 
        "jet_pt"        : [ 30, 0, 300], #[[0,20,40,60,80,100,120,140,160,180,200,225,250,300,400,500,1000]],
        "lepton_eta"    : [ 60,-3,3],
        "jet_eta"       : [ 10,-5,5],
        "lepton_phi"    : [70,-3.5,3.5],
        "jet_phi"       : [ 7,-3.5,3.5],
        "mT2ll"         : [ 20, 0, 200], #[[0,10,20,30,40,50,60,70,80,90,100,110,120,130,145,300]],
        "ptll"          : [ 50, 0, 500], 
        "mll"           : [ 60, 0, 600], #[[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,400,500,1000]],
        "mDRll"         : [[0,10,20,30,40,50,60,70,80,95,110,200]],
        "RPT"           : [ 10, 0, 1],
        "gamInvRp1"     : [ 10, 0, 1],
        "cosTheta_b"    : [ 10, -1, 1],
        "DPB_vSS"       : [ 16, 0, 3.2],
        "isDF"          : [  2, 0, 2],
        "isSF"          : [  2, 0, 2],
        "isOS"          : [  2, 0, 2],
        "met_et"        : [ 30, 0, 750], #[[0,20,40,60,80,100,120,140,160,180,200,225,250,300,400,500,1000]],
        "met_phi"       : [ 70,-3.5,3.5],
        "pbll"          : [ 50, 0, 1000],
        "r1"            : [ 10,  0,  1],
        "lepton_flav"   : [ 10, 10, 20],
        "jet_flav"      : [ 25,  0, 25],
        "lepton_type"   : [ 10,  0, 10],
        "lepton_origin" : [ 50,  0, 50],
        "dphill"        : [35,-3.5,3.5],
        "dphi_met_pbll" : [70,-3.5,3.5],
        "mcEventWeight" : [100, 0,  20],
        "susyID"        : [ 10, 0,  10],
        "truth_n1n1pt"  : [ 30, 0, 750],
        "truth_n1n1phi" : [70,-3.5,3.5],
        "truth_n1n1mass": [ 75, 500, 2000],
        "truth_ststpt"  : [ 30, 0, 750],
        "truth_ststphi" : [70,-3.5,3.5],
        "truth_ststmass": [ 75, 500, 2000],
        "truth_stpt"    : [ 50, 0, 1000],
        "truth_stmass"  : [20,289.5, 309.5],
        "truth_n1pt"    : [ 50, 0, 1000],
        "truth_n1mass"  : [20, 169.5, 189.5],
        "truth_wpt"     : [ 50,  0, 1000],
        "truth_wmass"   : [ 40, 60, 100],
        "truth_wbpt"    : [ 50,  0, 1000],
        "truth_wbmass"  : [ 75, 50, 200],
        "TMath::Cos(truth_thetal)"  : [10, -1, 1], # Cos of thetal
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
        if ii == 0:   colors[ii] = ROOT.kBlack 
        elif ii == 1: colors[ii] = ROOT.kSpring-1 
        elif ii == 2: colors[ii] = ROOT.kMagenta 
        elif ii == 3: colors[ii] = ROOT.kAzure-3
        elif ii == 4: colors[ii] = ROOT.kCyan-3 
        elif ii == 5: colors[ii] = ROOT.kOrange+1 
        elif ii == 6: colors[ii] = ROOT.kYellow+1 
        elif ii == 7: colors[ii] = ROOT.kRed
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
            print("WARNING :: Cannot find ROOT tree in the file %s"%inputFile)
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
                if variable == "lepton_n"    : variable = "@lepton_pt.size()"
                elif variable == "jet_n"     : variable = "@jet_pt.size()"
                elif variable == "bjet_n"    : variable = "@bjet_pt.size()"
                elif variable == "nonbjet_n" : variable = "@nonbjet_pt.size()"
                if(options.debug):
                    print("INFO :: Cross-section %.2f - Luminosity %.2f - Sumw %.2f"%(getCrossSection(inputFile),options.luminosity,sumw[ii]))
                if "MadgraphM" in inputFile:
                    selection=("(mcEventWeight*mcPolWeight_M*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                elif "MadgraphR" in inputFile:
                    selection=("(mcEventWeight*mcPolWeight_R*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                elif ("MadgraphL" in inputFile) or ("TakashiL" in inputFile):
                    selection=("(mcEventWeight*mcPolWeight_L*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                else:
                    selection=("(mcEventWeight*%f*%f/%f)*(%s)"%(getCrossSection(inputFile),options.luminosity,sumw[ii],cut))
                    #selection=("(mcEventWeight*%f*%f/%f)*(%s)"%(1,1,1,cut))
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
