import ROOT,math,array
import glob

# Define the input ROOT files
def getROOTFileName(filename):
#     dir0 = '/net/ustc_home/dzhang/work/bsmSearch/ewSUSY/analysis/syst1/run/r3/fetch/data-myOutput/'
#     dir0 = '/net/s3_datac/dzhang/outSpace/susyEW_out/sys1_Jul11a/fetch/data-myOutput/'
    dir0 = '/net/s3_datac/dzhang/outSpace/susyEW_out/sys1_Jul12b/fetch/data-myOutput/'
    return {
            "Sherpa_CT10_ggllll"          : dir0+"Sherpa_CT10_ggllll-*.root",
            "Sherpa_CT10_ggllll_fac025"   : dir0+"Sherpa_CT10_ggllll_fac025-*.root",
            "Sherpa_CT10_ggllll_fac4"     : dir0+"Sherpa_CT10_ggllll_fac4-*.root",
            "Sherpa_CT10_ggllll_qsf025"   : dir0+"Sherpa_CT10_ggllll_qsf025-*.root",
            "Sherpa_CT10_ggllll_qsf4"     : dir0+"Sherpa_CT10_ggllll_qsf4-*.root",
            "Sherpa_CT10_ggllll_renorm025": dir0+"Sherpa_CT10_ggllll_renorm025-*.root",
            "Sherpa_CT10_ggllll_renorm4"  : dir0+"Sherpa_CT10_ggllll_renorm4-*.root",
            "Sherpa_CT10_llvv"            : dir0+"Sherpa_CT10_llvv-*.root",
            "Sherpa_CT10_llvv_fac025"     : dir0+"Sherpa_CT10_llvv_fac025-*.root",
            "Sherpa_CT10_llvv_fac4"       : dir0+"Sherpa_CT10_llvv_fac4-*.root",
            "Sherpa_CT10_llvv_qsf025"     : dir0+"Sherpa_CT10_llvv_qsf025-*.root",
            "Sherpa_CT10_llvv_qsf4"       : dir0+"Sherpa_CT10_llvv_qsf4-*.root",
            "Sherpa_CT10_llvv_renorm025"  : dir0+"Sherpa_CT10_llvv_renorm025-*.root",
            "Sherpa_CT10_llvv_renorm4"    : dir0+"Sherpa_CT10_llvv_renorm4-*.root",
            "Sherpa_CT10_llvv_ckkw15"     : dir0+"Sherpa_CT10_llvv_ckkw15-*.root",
            "Sherpa_CT10_llvv_ckkw30"     : dir0+"Sherpa_CT10_llvv_ckkw30-*.root",

            "aMcAtNloHerwigppEvtGen_ttbar_nonallhad"    : dir0+"aMcAtNloHerwigppEvtGen_ttbar_nonallhad-*.root",
            "aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Wt_dilepton"    : dir0+"aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Wt_dilepton-*.root",
            "PhHppEG_AU2CT10_WlnuWlnu"    : dir0+"PhHppEG_AU2CT10_WlnuWlnu-*.root",
            "PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad"    : dir0+"PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad-*.root",
            "PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop"    : dir0+"PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop-*.root",
            "PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top"    : dir0+"PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top-*.root",
            "PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_WWlvlv"    : dir0+"PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_WWlvlv-*.root",
            "PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad"    : dir0+"PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad-*.root",
            "PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_antitop"    : dir0+"PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_antitop-*.root",
            "PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_top"    : dir0+"PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_top-*.root",
            "PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad"    : dir0+"PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad-*.root",
            "PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_antitop"    : dir0+"PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_antitop-*.root",
            "PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_top"    : dir0+"PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_top-*.root",
            "PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil"    : dir0+"PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil-*.root", ## nominal
            "PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop"    : dir0+"PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop-*.root", ## nominal
            "PowhegPythiaEvtGen_P2012_Wt_dilepton_top"    : dir0+"PowhegPythiaEvtGen_P2012_Wt_dilepton_top-*.root", ## nominal
            "PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_antitop"    : dir0+"PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_antitop-*.root",
            "PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_top"    : dir0+"PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_top-*.root",
            "Sherpa_CT10_ggllll"    : dir0+"Sherpa_CT10_ggllll-*.root",
            "Sherpa_CT10_ggllll_fac025"    : dir0+"Sherpa_CT10_ggllll_fac025-*.root",
            "Sherpa_CT10_ggllll_fac4"    : dir0+"Sherpa_CT10_ggllll_fac4-*.root",
            "Sherpa_CT10_ggllll_qsf025"    : dir0+"Sherpa_CT10_ggllll_qsf025-*.root",
            "Sherpa_CT10_ggllll_qsf4"    : dir0+"Sherpa_CT10_ggllll_qsf4-*.root",
            "Sherpa_CT10_ggllll_renorm025"    : dir0+"Sherpa_CT10_ggllll_renorm025-*.root",
            "Sherpa_CT10_ggllll_renorm4"    : dir0+"Sherpa_CT10_ggllll_renorm4-*.root",
            "Sherpa_CT10_ggllvv"    : dir0+"Sherpa_CT10_ggllvv-*.root",
            "Sherpa_CT10_ggllvv_fac025"    : dir0+"Sherpa_CT10_ggllvv_fac025-*.root",
            "Sherpa_CT10_ggllvv_fac4"    : dir0+"Sherpa_CT10_ggllvv_fac4-*.root",
            "Sherpa_CT10_ggllvv_qsf025"    : dir0+"Sherpa_CT10_ggllvv_qsf025-*.root",
            "Sherpa_CT10_ggllvv_qsf4"    : dir0+"Sherpa_CT10_ggllvv_qsf4-*.root",
            "Sherpa_CT10_ggllvv_renorm025"    : dir0+"Sherpa_CT10_ggllvv_renorm025-*.root",
            "Sherpa_CT10_ggllvv_renorm4"    : dir0+"Sherpa_CT10_ggllvv_renorm4-*.root",
            "Sherpa_CT10_llll"    : dir0+"Sherpa_CT10_llll-*.root",
            "Sherpa_CT10_llll_ckkw15"    : dir0+"Sherpa_CT10_llll_ckkw15-*.root",
            "Sherpa_CT10_llll_ckkw30"    : dir0+"Sherpa_CT10_llll_ckkw30-*.root",
            "Sherpa_CT10_llll_fac025"    : dir0+"Sherpa_CT10_llll_fac025-*.root",
            "Sherpa_CT10_llll_fac4"    : dir0+"Sherpa_CT10_llll_fac4-*.root",
            "Sherpa_CT10_lllljj_EW6"    : dir0+"Sherpa_CT10_lllljj_EW6-*.root",
            "Sherpa_CT10_llll_qsf025"    : dir0+"Sherpa_CT10_llll_qsf025-*.root",
            "Sherpa_CT10_llll_qsf4"    : dir0+"Sherpa_CT10_llll_qsf4-*.root",
            "Sherpa_CT10_llll_renorm025"    : dir0+"Sherpa_CT10_llll_renorm025-*.root",
            "Sherpa_CT10_llll_renorm4"    : dir0+"Sherpa_CT10_llll_renorm4-*.root",
            "Sherpa_CT10_lllvjj_EW6"    : dir0+"Sherpa_CT10_lllvjj_EW6-*.root",
            "Sherpa_CT10_lllvOFMinus"    : dir0+"Sherpa_CT10_lllvOFMinus-*.root",
            "Sherpa_CT10_lllvOFMinus_ckkw15"    : dir0+"Sherpa_CT10_lllvOFMinus_ckkw15-*.root",
            "Sherpa_CT10_lllvOFMinus_ckkw30"    : dir0+"Sherpa_CT10_lllvOFMinus_ckkw30-*.root",
            "Sherpa_CT10_lllvOFMinus_fac025"    : dir0+"Sherpa_CT10_lllvOFMinus_fac025-*.root",
            "Sherpa_CT10_lllvOFMinus_fac4"    : dir0+"Sherpa_CT10_lllvOFMinus_fac4-*.root",
            "Sherpa_CT10_lllvOFMinus_qsf025"    : dir0+"Sherpa_CT10_lllvOFMinus_qsf025-*.root",
            "Sherpa_CT10_lllvOFMinus_qsf4"    : dir0+"Sherpa_CT10_lllvOFMinus_qsf4-*.root",
            "Sherpa_CT10_lllvOFMinus_renorm025"    : dir0+"Sherpa_CT10_lllvOFMinus_renorm025-*.root",
            "Sherpa_CT10_lllvOFMinus_renorm4"    : dir0+"Sherpa_CT10_lllvOFMinus_renorm4-*.root",
            "Sherpa_CT10_lllvOFPlus"    : dir0+"Sherpa_CT10_lllvOFPlus-*.root",
            "Sherpa_CT10_lllvOFPlus_ckkw15"    : dir0+"Sherpa_CT10_lllvOFPlus_ckkw15-*.root",
            "Sherpa_CT10_lllvOFPlus_ckkw30"    : dir0+"Sherpa_CT10_lllvOFPlus_ckkw30-*.root",
            "Sherpa_CT10_lllvOFPlus_fac025"    : dir0+"Sherpa_CT10_lllvOFPlus_fac025-*.root",
            "Sherpa_CT10_lllvOFPlus_fac4"    : dir0+"Sherpa_CT10_lllvOFPlus_fac4-*.root",
            "Sherpa_CT10_lllvOFPlus_qsf025"    : dir0+"Sherpa_CT10_lllvOFPlus_qsf025-*.root",
            "Sherpa_CT10_lllvOFPlus_qsf4"    : dir0+"Sherpa_CT10_lllvOFPlus_qsf4-*.root",
            "Sherpa_CT10_lllvOFPlus_renorm025"    : dir0+"Sherpa_CT10_lllvOFPlus_renorm025-*.root",
            "Sherpa_CT10_lllvOFPlus_renorm4"    : dir0+"Sherpa_CT10_lllvOFPlus_renorm4-*.root",
            "Sherpa_CT10_lllvSFMinus"    : dir0+"Sherpa_CT10_lllvSFMinus-*.root",
            "Sherpa_CT10_lllvSFMinus_ckkw15"    : dir0+"Sherpa_CT10_lllvSFMinus_ckkw15-*.root",
            "Sherpa_CT10_lllvSFMinus_ckkw30"    : dir0+"Sherpa_CT10_lllvSFMinus_ckkw30-*.root",
            "Sherpa_CT10_lllvSFMinus_fac025"    : dir0+"Sherpa_CT10_lllvSFMinus_fac025-*.root",
            "Sherpa_CT10_lllvSFMinus_fac4"    : dir0+"Sherpa_CT10_lllvSFMinus_fac4-*.root",
            "Sherpa_CT10_lllvSFMinus_qsf025"    : dir0+"Sherpa_CT10_lllvSFMinus_qsf025-*.root",
            "Sherpa_CT10_lllvSFMinus_qsf4"    : dir0+"Sherpa_CT10_lllvSFMinus_qsf4-*.root",
            "Sherpa_CT10_lllvSFMinus_renorm025"    : dir0+"Sherpa_CT10_lllvSFMinus_renorm025-*.root",
            "Sherpa_CT10_lllvSFMinus_renorm4"    : dir0+"Sherpa_CT10_lllvSFMinus_renorm4-*.root",
            "Sherpa_CT10_lllvSFPlus"    : dir0+"Sherpa_CT10_lllvSFPlus-*.root",
            "Sherpa_CT10_lllvSFPlus_ckkw15"    : dir0+"Sherpa_CT10_lllvSFPlus_ckkw15-*.root",
            "Sherpa_CT10_lllvSFPlus_ckkw30"    : dir0+"Sherpa_CT10_lllvSFPlus_ckkw30-*.root",
            "Sherpa_CT10_lllvSFPlus_fac025"    : dir0+"Sherpa_CT10_lllvSFPlus_fac025-*.root",
            "Sherpa_CT10_lllvSFPlus_fac4"    : dir0+"Sherpa_CT10_lllvSFPlus_fac4-*.root",
            "Sherpa_CT10_lllvSFPlus_qsf025"    : dir0+"Sherpa_CT10_lllvSFPlus_qsf025-*.root",
            "Sherpa_CT10_lllvSFPlus_qsf4"    : dir0+"Sherpa_CT10_lllvSFPlus_qsf4-*.root",
            "Sherpa_CT10_lllvSFPlus_renorm025"    : dir0+"Sherpa_CT10_lllvSFPlus_renorm025-*.root",
            "Sherpa_CT10_lllvSFPlus_renorm4"    : dir0+"Sherpa_CT10_lllvSFPlus_renorm4-*.root",
            "Sherpa_CT10_llvv"    : dir0+"Sherpa_CT10_llvv-*.root",
            "Sherpa_CT10_llvv_ckkw15"    : dir0+"Sherpa_CT10_llvv_ckkw15-*.root",
            "Sherpa_CT10_llvv_ckkw30"    : dir0+"Sherpa_CT10_llvv_ckkw30-*.root",
            "Sherpa_CT10_llvv_fac025"    : dir0+"Sherpa_CT10_llvv_fac025-*.root",
            "Sherpa_CT10_llvv_fac4"    : dir0+"Sherpa_CT10_llvv_fac4-*.root",
            "Sherpa_CT10_llvv_qsf025"    : dir0+"Sherpa_CT10_llvv_qsf025-*.root",
            "Sherpa_CT10_llvv_qsf4"    : dir0+"Sherpa_CT10_llvv_qsf4-*.root",
            "Sherpa_CT10_llvv_renorm025"    : dir0+"Sherpa_CT10_llvv_renorm025-*.root",
            "Sherpa_CT10_llvv_renorm4"    : dir0+"Sherpa_CT10_llvv_renorm4-*.root",
            "Sherpa_CT10_WqqZll_SHv21_improved"    : dir0+"Sherpa_CT10_WqqZll_SHv21_improved-*.root",
            "Sherpa_CT10_WqqZll_SHv21_improved_fac025"    : dir0+"Sherpa_CT10_WqqZll_SHv21_improved_fac025-*.root",
            "Sherpa_CT10_WqqZll_SHv21_improved_fac4"    : dir0+"Sherpa_CT10_WqqZll_SHv21_improved_fac4-*.root",
            "Sherpa_CT10_WqqZll_SHv21_improved_qsf025"    : dir0+"Sherpa_CT10_WqqZll_SHv21_improved_qsf025-*.root",
            "Sherpa_CT10_WqqZll_SHv21_improved_qsf4"    : dir0+"Sherpa_CT10_WqqZll_SHv21_improved_qsf4-*.root",
            "Sherpa_CT10_WqqZll_SHv21_improved_renorm025"    : dir0+"Sherpa_CT10_WqqZll_SHv21_improved_renorm025-*.root",
            "Sherpa_CT10_WqqZll_SHv21_improved_renorm4"    : dir0+"Sherpa_CT10_WqqZll_SHv21_improved_renorm4-*.root",
            "Sherpa_CT10_ZqqZll_SHv21_improved"    : dir0+"Sherpa_CT10_ZqqZll_SHv21_improved-*.root",
            "Sherpa_CT10_ZqqZll_SHv21_improved_fac025"    : dir0+"Sherpa_CT10_ZqqZll_SHv21_improved_fac025-*.root",
            "Sherpa_CT10_ZqqZll_SHv21_improved_fac4"    : dir0+"Sherpa_CT10_ZqqZll_SHv21_improved_fac4-*.root",
            "Sherpa_CT10_ZqqZll_SHv21_improved_qsf025"    : dir0+"Sherpa_CT10_ZqqZll_SHv21_improved_qsf025-*.root",
            "Sherpa_CT10_ZqqZll_SHv21_improved_qsf4"    : dir0+"Sherpa_CT10_ZqqZll_SHv21_improved_qsf4-*.root",
            "Sherpa_CT10_ZqqZll_SHv21_improved_renorm025"    : dir0+"Sherpa_CT10_ZqqZll_SHv21_improved_renorm025-*.root",
            "Sherpa_CT10_ZqqZll_SHv21_improved_renorm4"    : dir0+"Sherpa_CT10_ZqqZll_SHv21_improved_renorm4-*.root",
    }.get(filename,"")

# Define cross-sections
def getCrossSection(filename):
    return {
    "Sherpa_CT10_llll"                 : 12.849*0.91,        # 361063
    "Sherpa_CT10_llll_fac4"             : 12.849*0.91,        # 363042
    "Sherpa_CT10_llll_fac025"             : 12.849*0.91,        # 363043
    "Sherpa_CT10_llll_renorm4"             : 12.849*0.91,        # 363044
    "Sherpa_CT10_llll_renorm025"         : 12.849*0.91,        # 363045
    "Sherpa_CT10_llll_qsf4"             : 12.849*0.91,        # 363046
    "Sherpa_CT10_llll_qsf025"             : 12.849*0.91,        # 363047
    "Sherpa_CT10_llll_ckkw15"             : 12.849*0.91,        # 363484
    "Sherpa_CT10_llll_ckkw30"             : 12.849*0.91,        # 363485
    "Sherpa_CT10_lllvSFMinus"             : 1.8446*0.91,       # 361064
    "Sherpa_CT10_lllvSFMinus_fac4"         : 1.8446*0.91,       # 363048
    "Sherpa_CT10_lllvSFMinus_fac025"       : 1.8446*0.91,       # 363049
    "Sherpa_CT10_lllvSFMinus_renorm4"     : 1.8446*0.91,       # 363050
    "Sherpa_CT10_lllvSFMinus_renorm025"     : 1.8446*0.91,       # 363051
    "Sherpa_CT10_lllvSFMinus_qsf4"         : 1.8446*0.91,       # 363052
    "Sherpa_CT10_lllvSFMinus_qsf025"      : 1.8446*0.91,       # 363053
    "Sherpa_CT10_lllvSFMinus_ckkw15"     : 1.8446*0.91,       # 363291
    "Sherpa_CT10_lllvSFMinus_ckkw30"     : 1.8446*0.91,       # 363292
    "Sherpa_CT10_lllvOFMinus"             : 3.6235*0.91,       # 361065
    "Sherpa_CT10_lllvOFMinus_fac4"         : 3.6235*0.91,       # 363054
    "Sherpa_CT10_lllvOFMinus_fac025"         : 3.6235*0.91,       # 363055
    "Sherpa_CT10_lllvOFMinus_renorm4"     : 3.6235*0.91,       # 363056
    "Sherpa_CT10_lllvOFMinus_renorm025"     : 3.6235*0.91,       # 363057
    "Sherpa_CT10_lllvOFMinus_qsf4"         : 3.6235*0.91,       # 363058
    "Sherpa_CT10_lllvOFMinus_qsf025"     : 3.6235*0.91,       # 363059
    "Sherpa_CT10_lllvOFMinus_ckkw15"     : 3.6235*0.91,       # 363293
    "Sherpa_CT10_lllvOFMinus_ckkw30"     : 3.6235*0.91,       # 363294
    "Sherpa_CT10_lllvSFPlus"             : 2.5656*0.91,       # 361066
    "Sherpa_CT10_lllvSFPlus_fac4"         : 2.5656*0.91,       # 363060
    "Sherpa_CT10_lllvSFPlus_fac025"         : 2.5656*0.91,       # 363061
    "Sherpa_CT10_lllvSFPlus_renorm4"     : 2.5656*0.91,       # 363062
    "Sherpa_CT10_lllvSFPlus_renorm025"     : 2.5656*0.91,       # 363063
    "Sherpa_CT10_lllvSFPlus_qsf4"         : 2.5656*0.91,       # 363064
    "Sherpa_CT10_lllvSFPlus_qsf025"         : 2.5656*0.91,       # 363065
    "Sherpa_CT10_lllvSFPlus_ckkw15"         : 2.5656*0.91,       # 363295
    "Sherpa_CT10_lllvSFPlus_ckkw30"         : 2.5656*0.91,       # 363296
    "Sherpa_CT10_lllvOFPlus"             : 5.0169*0.91,       # 361067
    "Sherpa_CT10_lllvOFPlus_fac4"         : 5.0169*0.91,       # 363066
    "Sherpa_CT10_lllvOFPlus_fac025"         : 5.0169*0.91,       # 363067
    "Sherpa_CT10_lllvOFPlus_renorm4"     : 5.0169*0.91,       # 363068
    "Sherpa_CT10_lllvOFPlus_renorm025"     : 5.0169*0.91,       # 363069
    "Sherpa_CT10_lllvOFPlus_qsf4"         : 5.0169*0.91,       # 363070
    "Sherpa_CT10_lllvOFPlus_qsf025"         : 5.0169*0.91,       # 363071
    "Sherpa_CT10_lllvOFPlus_ckkw15"         : 5.0169*0.91,       # 363297
    "Sherpa_CT10_lllvOFPlus_ckkw30"         : 5.0169*0.91,       # 363298
    "Sherpa_CT10_llvv"                 : 14.022*0.91,       # 361068
    "Sherpa_CT10_llvv_fac4"             : 14.022*0.91,       # 363072
    "Sherpa_CT10_llvv_fac025"             : 14.022*0.91,       # 363073
    "Sherpa_CT10_llvv_renorm4"         : 14.022*0.91,       # 363074
    "Sherpa_CT10_llvv_renorm025"         : 14.022*0.91,       # 363075
    "Sherpa_CT10_llvv_qsf4"             : 14.022*0.91,       # 363076
    "Sherpa_CT10_llvv_qsf025"             : 14.022*0.91,       # 363077
    "Sherpa_CT10_llvv_ckkw15"         : 14.022*0.91,       # 363299
    "Sherpa_CT10_llvv_ckkw30"         : 14.022*0.91,       # 363300

    "Sherpa_CT10_lllvjj_EW6"             : 0.042017*0.91,       # 361071
    "Sherpa_CT10_lllljj_EW6"             : 0.031496*0.91,       # 361072

    "Sherpa_CT10_ggllll"                 : 0.02095*0.91,       # 361073
    "Sherpa_CT10_ggllll_fac4"             : 0.02095*0.91,       # 363078
    "Sherpa_CT10_ggllll_fac025"         : 0.02095*0.91,       # 363079
    "Sherpa_CT10_ggllll_renorm4"         : 0.02095*0.91,       # 363080
    "Sherpa_CT10_ggllll_renorm025"         : 0.02095*0.91,       # 363081
    "Sherpa_CT10_ggllll_qsf4"             : 0.02095*0.91,       # 363082
    "Sherpa_CT10_ggllll_qsf025"         : 0.02095*0.91,       # 363083

    "Sherpa_CT10_ggllvv"             : 0.85492*0.91,       # 361077
    "Sherpa_CT10_ggllvv_fac4"             : 0.85492*0.91,       # 363084
    "Sherpa_CT10_ggllvv_fac025"         : 0.85492*0.91,       # 363085
    "Sherpa_CT10_ggllvv_renorm4"         : 0.85492*0.91,       # 363086
    "Sherpa_CT10_ggllvv_renorm025"         : 0.85492*0.91,       # 363087
    "Sherpa_CT10_ggllvv_qsf4"             : 0.85492*0.91,       # 363088
    "Sherpa_CT10_ggllvv_qsf025"         : 0.85492*0.91,       # 363089

    "Sherpa_CT10_WqqZll_SHv21_improved"     : 3.4234*0.91*1.0000E+00,       # 361094
    "Sherpa_CT10_ZqqZll_SHv21_improved"     : 16.445*0.91*1.4307E-01,       # 361096

    "PhHppEG_AU2CT10_WlnuWlnu"                 : 10.628,       # 361591
    "PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_WWlvlv"     : 10.631,       # 361600

    "Sherpa_CT10_WqqZll_SHv21_improved_fac4"         : 3.4675*0.91,    # 363018
    "Sherpa_CT10_WqqZll_SHv21_improved_fac025"         : 3.385*0.91,       # 363019
    "Sherpa_CT10_WqqZll_SHv21_improved_renorm4"     : 3.04*0.91,       # 363020
    "Sherpa_CT10_WqqZll_SHv21_improved_renorm025"     : 4.012*0.91,       # 363021
    "Sherpa_CT10_WqqZll_SHv21_improved_qsf4"         : 3.3616*0.91,    # 363022
    "Sherpa_CT10_WqqZll_SHv21_improved_qsf025"         : 3.4638*0.91,    # 363023

    "Sherpa_CT10_ZqqZll_SHv21_improved_fac4"         : 16.662*0.91*1.4317E-01,    # 363030
    "Sherpa_CT10_ZqqZll_SHv21_improved_fac025"         : 16.135*0.91*1.4355E-01,    # 363031
    "Sherpa_CT10_ZqqZll_SHv21_improved_renorm4"     : 15.331*0.91*1.4296E-01,    # 363032
    "Sherpa_CT10_ZqqZll_SHv21_improved_renorm025"     : 17.843*0.91*1.4321E-01,    # 363033
    "Sherpa_CT10_ZqqZll_SHv21_improved_qsf4"         : 16.071*0.91*1.4353E-01,    # 363034
    "Sherpa_CT10_ZqqZll_SHv21_improved_qsf025"         : 16.858*0.91*1.4331E-01,    # 363035

    "PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad"     : 783.73*1.0613*0.543,    # 410001
    "PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad"     : 611.1*1.3611*0.543,        # 410002
    "aMcAtNloHerwigppEvtGen_ttbar_nonallhad"                 : 694.59*1.1975*0.543,    # 410003
    "PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad"     : 696.32*1.1926*0.543,    # 410004

    "PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil"             : 696.12*1.1949*0.1053,    # 410009
    "PowhegPythiaEvtGen_P2012_Wt_dilepton_top"                 : 3.5835*1.054,        # 410015
    "PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_top"             : 3.5835*1.054,        # 410103
    "PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_top"             : 3.5835*1.054,        # 410104
    "PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_top"             : 3.5835*1.054,        # 410145

    "PowhegPythiaEvtGen_P2012_Wt_dilepton_antitop"             : 3.5814*1.054,        # 410016
    "PowhegPythiaEvtGen_P2012radHi_Wt_dilepton_antitop"             : 3.5814*1.054,        # 410105
    "PowhegPythiaEvtGen_P2012radLo_Wt_dilepton_antitop"             : 3.5814*1.054,        # 410106
    "PowhegHerwigppEvtGen_UEEE5_Wt_dilepton_antitop"             : 3.5814*1.054,        # 410146

    "PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_top"             : 3.4133*1.054,        # 410064
    "PowhegPythiaEvtGen_P2012_Wt_DS_dilepton_antitop"             : 3.409*1.054,            # 410065

    "aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Wt_dilepton"     : 7.871,            # 410164

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


def getCrossSection1(filename):
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
#     forwardJetVeto    = "&&Sum$(jet_pt>30)==0"

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

        "EW2L_SR_XF"              : "("  + diLep + bVeto + centralJetVeto30 + forwardJetVeto + ")",
        "EW2L_TopVR_XF"           : "("  + diLep + bSelection + centralJetVeto30 + forwardJetVeto + "&&mT2ll>70&&mT2ll<120)",

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
