#ifndef xAODTruthAnalysis_Ewk2LTruthAnalysis_H
#define xAODTruthAnalysis_Ewk2LTruthAnalysis_H

#include <EventLoop/Algorithm.h>

#include <TH1.h>

#include <vector>       // std::vector
#include <map>          // std::map

class Ewk2LTruthAnalysis : public EL::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  // float cutValue;



  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:
  // Tree *myTree; //!
  // TH1 *myHist; //!



  // this is a standard constructor
  Ewk2LTruthAnalysis ();

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
  static const unsigned int m_nHists1D = 31;
  std::vector<TH1*> h_hists1D;  //!
  std::map<std::string,unsigned int> m_nameToIndex;

  // this is needed to distribute the algorithm to the workers
  ClassDef(Ewk2LTruthAnalysis, 1);
};

#endif
