import ROOT,math,array
import glob

# Define the input ROOT files
def getROOTFileName(filename):
#     dir0 = '/net/ustc_home/dzhang/work/bsmSearch/ewSUSY/analysis/syst1/run/r3/fetch/data-myOutput/'
#     dir0 = '/net/s3_datac/dzhang/outSpace/susyEW_out/sys1_Jul11a/fetch/data-myOutput/'
    dir0 = '/net/s3_datac/dzhang/outSpace/susyEW_out/sys1_Jul12b/fetch/data-myOutput/'
    return {
            "Sherpa_ggllll"          : dir0+"Sherpa_CT10_ggllll-*.root",
            "Sherpa_ggllll_fac025"   : dir0+"Sherpa_CT10_ggllll_fac025-*.root",
            "Sherpa_ggllll_fac4"     : dir0+"Sherpa_CT10_ggllll_fac4-*.root",
            "Sherpa_ggllll_qsf025"   : dir0+"Sherpa_CT10_ggllll_qsf025-*.root",
            "Sherpa_ggllll_qsf4"     : dir0+"Sherpa_CT10_ggllll_qsf4-*.root",
            "Sherpa_ggllll_renorm025": dir0+"Sherpa_CT10_ggllll_renorm025-*.root",
            "Sherpa_ggllll_renorm4"  : dir0+"Sherpa_CT10_ggllll_renorm4-*.root",
            "Sherpa_llvv"            : dir0+"Sherpa_CT10_llvv-*.root",
            "Sherpa_llvv_fac025"     : dir0+"Sherpa_CT10_llvv_fac025-*.root",
            "Sherpa_llvv_fac4"       : dir0+"Sherpa_CT10_llvv_fac4-*.root",
            "Sherpa_llvv_qsf025"     : dir0+"Sherpa_CT10_llvv_qsf025-*.root",
            "Sherpa_llvv_qsf4"       : dir0+"Sherpa_CT10_llvv_qsf4-*.root",
            "Sherpa_llvv_renorm025"  : dir0+"Sherpa_CT10_llvv_renorm025-*.root",
            "Sherpa_llvv_renorm4"    : dir0+"Sherpa_CT10_llvv_renorm4-*.root",
            "Sherpa_llvv_ckkw15"     : dir0+"Sherpa_CT10_llvv_ckkw15-*.root",
            "Sherpa_llvv_ckkw30"     : dir0+"Sherpa_CT10_llvv_ckkw30-*.root",
            "aMcAtNloHerwigpp_Wt"    : dir0+"aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Wt_dilepton-0.root",
            "PowhegHerwigpp_Wt"      : dir0+"PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top-0.root",
            "PowhegHerwigpp_Wtbar"   : dir0+"PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop-0.root",
#         "Sherpa_lvlv"          : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_361068.root",
#         "Sherpa_lvlv_fac4"     : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_363072.root",
#         "Sherpa_lvlv_fac025"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_363073.root",
#         "Sherpa_lvlv_renorm4"  : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_363074.root",
#         "Sherpa_lvlv_renorm025": "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_363075.root",
#         "Sherpa_lvlv_qsf4"     : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_363076.root",
#         "Sherpa_lvlv_qsf025"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_363077.root",
#         "Powheg_WWlvlv"        : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_361600.root",
#         "Powheg_ZZllvv"        : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_361604.root",
#         "Powheg_ttbar"         : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_410000.root",
#         "Powheg_ttbar_radHi"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_410001.root",
#         "Powheg_ttbar_radLo"   : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_410002.root",
#         "aMCatNLO_ttbar"       : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_410003.root",
#         "PowhegHpp_ttbar"      : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_410004.root",
#         "Sherpa_ttbar_410021"  : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_410021.root",
#         "Sherpa_ttbar_410189"  : "/data/uclhc/uci/user/amete/truth_analysis_run/combined_3/out_410189.root",
#         #"Herwigpp_300vs180"    : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/Herwigpp.300vs180.truth1_v3.root",
#         #"Madgraph_300vs180"    : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/Madgraph.300vs180.truth1_v3.root",
#         #"MadgraphR_300vs180"   : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/MadgraphR.300vs180.truth1_v3.root",
#         #"MadgraphL_300vs180"   : "/gdata/atlas/amete/StopPolarization/outputs/FlatNtuples/MadgraphL.300vs180.truth1_v3.root",
#         "Herwigpp_250vs160"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_406009.HppEG_UE5C6L1_Tt_bWN_t250_n160_2Lep18.root",
#         "HerwigppL_250vs160"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_999999.HppEG_UE5C6L1_Tt_bWN_t250_n160_2Lep18.root",
#         "Madgraph_250vs160"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387943.MGPy8EG_A14N23LO_TT_bWN_250_160_2L15.root",
#         "MadgraphL_250vs160"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387943.MGPy8EG_A14N23LO_TT_bWN_250_160_2L15.root",
#         "MadgraphR_250vs160"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387943.MGPy8EG_A14N23LO_TT_bWN_250_160_2L15.root",
#         "Herwigpp_300vs150"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_406010.HppEG_UE5C6L1_Tt_bWN_t300_n150_2Lep18.root",
#         "Madgraph_300vs150"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387947.MGPy8EG_A14N23LO_TT_bWN_300_150_2L15.root",
#         "MadgraphR_300vs150"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387947.MGPy8EG_A14N23LO_TT_bWN_300_150_2L15.root",
#         "HerwigppR_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_406011.HppEG_UE5C6L1_Tt_bWN_t300_n180_2Lep18.root",
#         "HerwigppL_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_999998.HppEG_UE5C6L1_Tt_bWN_t300_n180_2Lep18.root",
#         "Madgraph_300vs180"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
#         "MadgraphM_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
#         "MadgraphR_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
#         "MadgraphL_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_387948.MGPy8EG_A14N23LO_TT_bWN_300_180_2L15.root",
#         "MadgraphFR_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123457.MGPy8EG_A14N_TTright_bWN_300_180_2Lep18.root",
#         "MadgraphT_300vs180"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123458.MGPy8EG_A14N_TTright_bWN_300_180_2Lep18.root",
#         "MadgraphFL_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999927.MGPy8EG_A14N23LO_TT_directBWNleft_250_125.root",
#         "MadgraphL_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
#         "MadgraphM_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
#         "MadgraphR_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
#         "Madgraph_250vs125"     : "/data/uclhc/uci/user/amete/stop_signal_flat/takashi/FLAT_999929.MGPy8EG_A14N23LO_TT_directBWN_250_125.root",
#         "HerwigppL_250vs125"   : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_999997.HppEG_UE5C6L1_Tt_bWN_t250_n125_2Lep18.root",
#         "SerhanFL_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123460.MGPy8EG_A14N_TTleft_bWN_250_125_2Lep18.root",
#         "SerhanFR_250vs125"    : "/data/uclhc/uci/user/amete/stop_signal_flat/FLAT_123461.MGPy8EG_A14N_TTright_bWN_250_125_2Lep18.root",
#         #"MadgraphSlep_100vs1"  : "/gdata/atlas/amete/MC15_SleptonPairProduction/FLAT/DAOD_TRUTH1.MGPy8EG_A14N23LO_SlepSlep_direct_100p0_1p0_2L5_10k.pool.root",
#         "MadgraphSlep_100vs1"  : "/data/uclhc/uci/user/amete/slepton_signal_flat/DAOD_TRUTH1.MGPy8EG_A14N23LO_SlepSlep_direct_100p0_1p0_2L5_10k.pool.root",
    }.get(filename,"")

# Define cross-sections
def getCrossSection(filename):
    return {
        "Sherpa_ggllll"          : 14.022*0.91,   # 361068 https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MC15SystematicUncertainties#VV_Diboson_V_W_Z 24/11/15
        "Sherpa_ggllll_fac4"     : 14.022*0.91,   # 363072
        "Sherpa_ggllll_fac025"   : 14.022*0.91,   # 363073
        "Sherpa_ggllll_renorm4"  : 14.022*0.91,   # 363074
        "Sherpa_ggllll_renorm025": 14.022*0.91,   # 363075
        "Sherpa_ggllll_qsf4"     : 14.022*0.91,   # 363076
        "Sherpa_ggllll_qsf025"   : 14.022*0.91,   # 363077
        "Sherpa_ggllll_ckkw15"   : 14.022*0.91,   # 363076  
        "Sherpa_ggllll_ckkw30"   : 14.022*0.91,   # 363077
        "Sherpa_llvv"          : 14.022*0.91,
        "Sherpa_llvv_fac4"     : 14.022*0.91,
        "Sherpa_llvv_fac025"   : 14.022*0.91,
        "Sherpa_llvv_renorm4"  : 14.022*0.91,
        "Sherpa_llvv_renorm025": 14.022*0.91,
        "Sherpa_llvv_qsf4"     : 14.022*0.91,
        "Sherpa_llvv_qsf025"   : 14.022*0.91,
        "Sherpa_llvv_ckkw15"   : 14.022*0.91,
        "Sherpa_llvv_ckkw30"   : 14.022*0.91,
        "aMcAtNloHerwigpp_Wt"  : 7.165,
        "PowhegHerwigpp_Wt"    : 3.584,
        "PowhegHerwigpp_Wtbar" : 3.581,
        "Sherpa_lvlv"          : 14.022*0.91,   # 361068 https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MC15SystematicUncertainties#VV_Diboson_V_W_Z 24/11/15
        "Sherpa_lvlv_fac4"     : 14.022*0.91,   # 363072
        "Sherpa_lvlv_fac025"   : 14.022*0.91,   # 363073
        "Sherpa_lvlv_renorm4"  : 14.022*0.91,   # 363074
        "Sherpa_lvlv_renorm025": 14.022*0.91,   # 363075
        "Sherpa_lvlv_qsf4"     : 14.022*0.91,   # 363076
        "Sherpa_lvlv_qsf025"   : 14.022*0.91,   # 363077
        "Powheg_WWlvlv"        : 10.631,        # 361600
        "Powheg_ZZllvv"        : 0.92498,       # 361604
        "Powheg_ttbar"         : 831.76*0.543,  # 410000 => 696.11  1.1949  0.543
        "Powheg_ttbar_radHi"   : 831.76*0.543,  # 410001 => 783.73  1.0613  0.543
        "Powheg_ttbar_radLo"   : 831.76*0.543,  # 410002 => 611.1   1.3611  0.543
        "aMCatNLO_ttbar"       : 831.76*0.543,  # 410003 => 694.59  1.1975  0.543
        "PowhegHpp_ttbar"      : 831.76*0.543,  # 410004 => 696.32  1.1926  0.543 
        "Sherpa_ttbar_410021"  : 78.73*1.17,    # 410021 => 78.73   1.17    1. 
        "Sherpa_ttbar_410189"  : 76.333*1.1484, # 410021 => https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MC15TTbarSamplesPMG 
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
        "c_bjet_n"        : "Number of custom bjets", 
        "c_nonbjet_n"     : "Number of custom nonbjets", 
        "c_bjet_pt[0]"    : "Leading custom bjet p_{T} [GeV]", 
        "c_bjet_pt[1]"    : "Subleading custom bjet p_{T} [GeV]",
        "c_nonbjet_pt[0]" : "Leading custom nonbjet p_{T} [GeV]", 
        "c_nonbjet_pt[1]" : "Subleading custom nonbjet p_{T} [GeV]",
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

    diLep           = "(@lepton_pt.size()==2&&isOS&&lepton_pt[0]>25.&&lepton_pt[1]>20.&&(lepton_type[0]==2||lepton_type[0]==6)&&(lepton_type[1]==2||lepton_type[1]==6))&&mll>20."
    isOSDF          = diLep+"&&isDF"
    isOSSF          = diLep+"&&isSF"

    zVeto           = "&&TMath::Abs(mll-91.2)>10."
    zSel            = "&&TMath::Abs(mll-91.2)<10."
    bVeto           = "&&(@bjet_pt.size()==0)"
    bSelection      = "&&(@bjet_pt.size()>0)"

    centralJetVeto20  = "&&Sum$(nonbjet_pt>20)==0"
    centralJetVeto30  = "&&Sum$(nonbjet_pt>30)==0"
    forwardJetVeto    = "&&Sum$(forwardjet_pt>30)==0"
    forwardJetVeto    = "&&Sum$(jet_pt>30)==0"

    DFSel = isOSDF + bVeto + centralJetVeto30 + forwardJetVeto
    SFSel = isOSSF + bVeto + centralJetVeto20 + forwardJetVeto

    return {
        # Actual regions # These guys don't have the mll>20 GeV cut!!!
        "EW2L_SR_SF_mT2_90"       : "("  + SFSel + zVeto + "&&mT2ll>90)",
        "EW2L_SR_SF_mT2_120"      : "("  + SFSel + zVeto + "&&mT2ll>120)",
        "EW2L_SR_SF_mT2_150"      : "("  + SFSel + zVeto + "&&mT2ll>150)",
        "EW2L_SR_SF"              : "("  + SFSel + zVeto + ")",
        "EW2L_CR_SF"              : "("  + SFSel + zSel  + "&&mT2ll>90)",

        "EW2L_SR_DF_mT2_90"       : "("  + DFSel + "&&mT2ll>90)",
        "EW2L_SR_DF_mT2_120"      : "("  + DFSel + "&&mT2ll>120)",
        "EW2L_SR_DF_mT2_150"      : "("  + DFSel + "&&mT2ll>150)",
        "EW2L_SR_DF"              : "("  + DFSel + ")",
        "EW2L_CR_DF"              : "("  + DFSel + "&&mT2ll>50&&mT2ll<75)",
        "EW2L_TopVR_DF"           : "("  + isOSDF + bSelection + centralJetVeto30 + forwardJetVeto + "&&mT2ll>70&&mT2ll<120)",
        "EW2L_TopVR0_DF"           : "(" + isOSDF + centralJetVeto30 + forwardJetVeto + "&&mT2ll>70&&mT2ll<120)",

        "EW2L_NOmT2_DF"           : "("  + DFSel + ")",
        "EW2L_NOmT2NOmll_SF"      : "("  + SFSel + ")",
    }.get(region,"1") # 1 is default if region is not found

# Define histogram bins
def getBinInformation(variable):
    return {
        "lepton_n"      : [ 10, 0,  10],
        "jet_n"         : [ 20, 0,  20],
        "bjet_n"        : [ 10, 0,  10],
        "nonbjet_n"     : [ 20, 0,  20],
        "lepton_pt"     : [ 25, 0, 250], 
        "bjet_pt"       : [ 25, 0, 250], 
        "nonbjet_pt"    : [ 30, 0, 750], 
        "c_bjet_n"      : [ 20, 0,  20],
        "c_nonbjet_n"   : [ 20, 0,  20],
        "c_lepton_pt"   : [ 25, 0, 250], 
        "c_bjet_pt"     : [ 25, 0, 250], 
        "c_nonbjet_pt"  : [ 30, 0, 750], 
        "jet_pt"        : [ 30, 0, 300], #[[0,20,40,60,80,100,120,140,160,180,200,225,250,300,400,500,1000]],
        "lepton_eta"    : [ 60,-3,3],
        "jet_eta"       : [ 10,-5,5],
        "lepton_phi"    : [70,-3.5,3.5],
        "jet_phi"       : [ 7,-3.5,3.5],
        "mT2ll"         : [ 20, 0, 200], #[[0,10,20,30,40,50,60,70,80,90,100,110,120,130,145,300]],
        "ptll"          : [ 50, 0, 500], 
        "mll"           : [ 8, 0, 400], #[[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,400,500,1000]],
        "mDRll"         : [[0,10,20,30,40,50,60,70,80,95,110,200]],
        "RPT"           : [ 10, 0, 1],
        "gamInvRp1"     : [ 5, 0, 1],
        "cosTheta_b"    : [ 5, -1, 1],
        "DPB_vSS"       : [ 8, 0, 3.2],
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
    return [getROOTFileName(x) for x in options.inputname.split(",")]
#     inputFileList=options.inputname.split(",")
#     files=[0 for x in range(len(inputFileList))]
#     for ii,inputFile in enumerate(inputFileList):
#         files[ii] = ROOT.TFile(getROOTFileName(inputFile),"READ")
#     return files

# Get sum of weights
def getSumOfWeights(files):
    sumw=[0 for x in range(len(files))]
    for ii,iiFile in enumerate(files):
        for f in glob.glob(iiFile):
#             print f
            f1 = ROOT.TFile(f,'read')
            sumw[ii] += f1.Get("CutflowWeighted").GetBinContent(1)
#             sumw[ii] = ROOT.TFile(f,'read').Get("CutflowWeighted").GetBinContent(1)
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
        currentROOTTree = ROOT.TChain('SuperTruth')
        currentROOTTree.Add(files[ii])

#         currentROOTTree = files[ii].Get("SuperTruth")
#         if not currentROOTTree:
#             print("WARNING :: Cannot find ROOT tree in the file %s"%inputFile)
#             continue
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
                if variable == "lepton_n"      : variable = "@lepton_pt.size()"
                elif variable == "jet_n"       : variable = "@jet_pt.size()"
                elif variable == "bjet_n"      : variable = "@bjet_pt.size()"
                elif variable == "nonbjet_n"   : variable = "@nonbjet_pt.size()"
                elif variable == "c_bjet_n"    : variable = "@c_bjet_pt.size()"
                elif variable == "c_nonbjet_n" : variable = "@c_nonbjet_pt.size()"
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
