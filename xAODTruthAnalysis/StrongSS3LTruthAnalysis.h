#ifndef xAODTruthAnalysis_StrongSS3LTruthAnalysis_H
#define xAODTruthAnalysis_StrongSS3LTruthAnalysis_H

#include <EventLoop/Algorithm.h>

#include <TH1.h>
#include <TTree.h>

#include <vector>       // std::vector
#include <map>          // std::map

// EDM include(s):
#include "xAODTruth/TruthParticleContainer.h"

class StrongSS3LTruthAnalysis : public EL::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  // float cutValue;



  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:
  // Set switches
  bool isSignal;
  bool saveTree;

  // Output Tree
  std::string outputFileName;
  TTree *outputTree; //!

  unsigned long long m_br_runNumber; //!
  unsigned long long m_br_eventNumber; //!
  float m_br_eventWeight; //! mcEventWeights[0]
  std::vector<float> m_br_mcEventWeights; //!
  std::vector<float> m_br_lepton_pt; //!
  std::vector<float> m_br_lepton_eta; //!
  std::vector<float> m_br_lepton_phi; //!
  std::vector<float> m_br_lepton_m; //!
  std::vector<int>   m_br_lepton_flav; //!
  std::vector<unsigned int>  m_br_lepton_type; //!
  std::vector<unsigned int>  m_br_lepton_origin; //!
  std::vector<int>   m_br_lepton_mother; //!
  std::vector<float> m_br_lepton_mother_mass; //!
  std::vector<float> m_br_bjet_pt; //!
  std::vector<float> m_br_nonbjet_pt; //!
  std::vector<float> m_br_jet_pt; //!
  std::vector<float> m_br_jet_eta; //!
  std::vector<float> m_br_jet_phi; //!
  std::vector<float> m_br_jet_m; //!
  std::vector<int>   m_br_jet_flav; //!
  int  m_br_susyID;   //!
  bool m_br_isSF;     //!
  bool m_br_isDF;     //!
  bool m_br_isSS;     //!
  bool m_br_isOS;     //!
  float m_br_mll;     //!
  float m_br_ptll;     //!
  float m_br_dphill;     //!
  float m_br_pbll;    //!
  float m_br_met_et;  //!
  float m_br_met_phi; //!
  float m_br_mT2ll;   //!
  float m_br_dphi_met_pbll; //!

  // this is a standard constructor
  StrongSS3LTruthAnalysis ();

  // Own functions
  bool FindSusyHardProc(const xAOD::TruthParticleContainer *truthP, int& pdgid1, int& pdgid2, bool isTruth3);

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode changeInput (bool firstFile);
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();

  // Event variables
  private:
  unsigned int m_eventCounter; //!

  // Histograms
  private:
  TH1* h_cutflow_weighted; //!
  static const unsigned int m_nHists1D = 31;
  std::vector<TH1*> h_hists1D;  //!
  std::map<std::string,unsigned int> m_nameToIndex;

  // this is needed to distribute the algorithm to the workers
  ClassDef(StrongSS3LTruthAnalysis, 1);
};

#endif
