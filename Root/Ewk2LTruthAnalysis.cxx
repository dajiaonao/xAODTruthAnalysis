#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <xAODTruthAnalysis/Ewk2LTruthAnalysis.h>

// STD include(s):
#include <algorithm>    // std::sort
#include <stdio.h>      // sscanf

// Infrastructure include(s):
#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/tools/Message.h"

// EDM include(s):
#include "xAODEventInfo/EventInfo.h"
#include "xAODTruth/TruthVertex.h"
#include "xAODTruth/TruthParticle.h"
#include "xAODTruth/TruthEventContainer.h"
//#include "xAODTruth/TruthParticleContainer.h"
#include "xAODMissingET/MissingETContainer.h"
#include "xAODJet/Jet.h"
#include "xAODJet/JetContainer.h"

// Analysis include(s):
#include <xAODTruthAnalysis/MT2_ROOT.h>
#include <xAODTruthAnalysis/PhysicsTools.h>

#include <LHAPDF/LHAPDF.h>
#include <LHAPDF/Reweighting.h>
// ROOT include(s):
#include <TFile.h>

/// Helper macro for checking xAOD::TReturnCode return values
#define EL_RETURN_CHECK( CONTEXT, EXP )                     \
   do {                                                     \
      if( ! EXP.isSuccess() ) {                             \
         Error( CONTEXT,                                    \
                XAOD_MESSAGE( "Failed to execute: %s" ),    \
                #EXP );                                     \
         return EL::StatusCode::FAILURE;                    \
      }                                                     \
   } while( false )


// Sort function
struct SortByPt {
  bool operator()(const xAOD::TruthParticle *a, const xAOD::TruthParticle *b) const {
    return a->pt() > b->pt();
  }
  bool operator()(const xAOD::Jet *a, const xAOD::Jet *b) const {
    return a->pt() > b->pt();
  }
};

// Convert
#define MEVtoGEV 1.e-3

// this is needed to distribute the algorithm to the workers
ClassImp(Ewk2LTruthAnalysis)



Ewk2LTruthAnalysis :: Ewk2LTruthAnalysis ():CF_l0_pt(10000.),CF_l1_pt(10000.)
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  Note that you should only put
  // the most basic initialization here, since this method will be
  // called on both the submission and the worker node.  Most of your
  // initialization code will go into histInitialize() and
  // initialize().
}



EL::StatusCode Ewk2LTruthAnalysis :: setupJob (EL::Job& job)
{
  // Here you put code that sets up the job on the submission object
  // so that it is ready to work with your algorithm, e.g. you can
  // request the D3PDReader service or add output files.  Any code you
  // put here could instead also go into the submission script.  The
  // sole advantage of putting it here is that it gets automatically
  // activated/deactivated when you add/remove the algorithm from your
  // job, which may or may not be of value to you.

  // let's initialize the algorithm to use the xAODRootAccess package
  job.useXAOD ();
  EL_RETURN_CHECK( "setupJob()", xAOD::Init() ); // call before opening first file

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Ewk2LTruthAnalysis :: histInitialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.

  h_cutflow_weighted = new TH1D("CutflowWeighted","CutflowWeighted",10,0.,10.);
  h_cutflow_weighted->Sumw2();

  if(saveHists) {
    wk()->addOutput(h_cutflow_weighted);

    const std::string histoNames[m_nHists1D] = { "nLep 5 -0.5 4.5",
                                                 "lep0Pt 50 0 1000",
                                                 "lep0Eta 30 -3 3",  
                                                 "lep0Phi 18 -3.6 3.6", 
                                                 "lep1Pt 50 0 1000",
                                                 "lep1Eta 30 -3 3",  
                                                 "lep1Phi 18 -3.6 3.6", 
                                                 "deltaRll 30 0 6",
                                                 "deltaPhill 18 -3.6 3.6",
                                                 "mll 50 0 1000",  
                                                 "pTll 50 0 1000",
                                                 "met 50 0 1000",
                                                 "metRel 50 0 1000",
                                                 "mT2 50 0 500",
                                                 "mDeltaR 50 0 500",
                                                 "r2 20 0 1",
                                                 "deltaPhil0met 18 -3.6 3.6",
                                                 "deltaPhil1met 18 -3.6 3.6",
                                                 "dPhill_vBETA_T 9 0 3.6",
                                                 "nJet 10 -0.5 9.5",
                                                 "jet0Pt 50 0 1000",
                                                 "jet0Eta 50 -5 5",  
                                                 "jet0Phi 18 -3.6 3.6", 
                                                 "jet1Pt 50 0 1000",
                                                 "jet1Eta 50 -5 5",  
                                                 "jet1Phi 18 -3.6 3.6", 
                                                 "mx1 1000 -0.5 999.5",
                                                 "mn1 500 0 500",
                                                 "x1x1Pt 50 0 1000",
                                                 "deltaRx1x1 50 0 10",
                                                 "deltaPhix1x1 18 -3.6 3.6"
                                               };

    int nbin=0;  float xmin=0; float xmax=0; char hName[50]; TH1D* temp;
    for( unsigned int i=0; i<m_nHists1D; ++i) {
      // Create and store the histograms
      sscanf(histoNames[i].c_str(),"%s %i %f %f",hName,&nbin,&xmin,&xmax);
      temp = new TH1D(hName,hName,nbin,xmin,xmax);
      temp->Sumw2();
      h_hists1D.push_back(temp);
      wk()->addOutput(h_hists1D.at(i));     
      // For easy filling
      m_nameToIndex.insert( std::pair<std::string,unsigned int>(std::string(hName),i) );
    }
  }

  // Output Tree
  if(saveTree) {
    TFile *outputFile = wk()->getOutputFile (outputFileName);
    outputTree = new TTree("SuperTruth"/*"susytree"*/,"SuperTruth"/*"susytree"*/);
    h_cutflow_weighted->SetDirectory(outputFile); // Not the best solution, if both Hist and Tree written only shows up in the Tree
    outputTree->SetDirectory(outputFile);
    outputTree->Branch("runNumber"     /* "RunNumber"     */, &m_br_runNumber     ); 
    outputTree->Branch("eventNumber"   /* "EventNumber"   */, &m_br_eventNumber   ); 
    outputTree->Branch("pdfWeights"    /* "pdfWeights"    */, &m_br_pdfWeights     ); 
    outputTree->Branch("mcEventWeight" /* "EventWeight"   */, &m_br_eventWeight   ); 
    outputTree->Branch("mcEventWeights"/* "mcEventWeights"*/, &m_br_mcEventWeights); 
    outputTree->Branch("susyID"        /* "susyID"        */, &m_br_susyID        ); 
    outputTree->Branch("isSF"          /* "isSF"          */, &m_br_isSF          ); 
    outputTree->Branch("isDF"          /* "isDF"          */, &m_br_isDF          ); 
    outputTree->Branch("isSS"          /* "isSS"          */, &m_br_isSS          ); 
    outputTree->Branch("isOS"          /* "isOS"          */, &m_br_isOS          ); 
    outputTree->Branch("isNOHISR"      /* N/A             */, &m_br_isNOHISR      ); 
    outputTree->Branch("lepton_pt"     /* "ptleptons"     */, &m_br_lepton_pt     ); 
    outputTree->Branch("lepton_eta"    /* "etaleptons"    */, &m_br_lepton_eta    ); 
    outputTree->Branch("lepton_phi"    /* "phileptons"    */, &m_br_lepton_phi    ); 
    outputTree->Branch("lepton_m"      /* "massleptons"   */, &m_br_lepton_m      ); 
    outputTree->Branch("lepton_flav"   /* "flavleptons"   */, &m_br_lepton_flav   ); 
    outputTree->Branch("lepton_type"   /* "typeleptons"   */, &m_br_lepton_type   ); 
    outputTree->Branch("lepton_origin" /* "originleptons" */, &m_br_lepton_origin ); 
    outputTree->Branch("lepton_mother" /* "motherleptons" */, &m_br_lepton_mother ); 
    outputTree->Branch("lepton_mother_mass" /* "motherleptons" */, &m_br_lepton_mother_mass ); 
    outputTree->Branch("bjet_pt"       /* N/A             */, &m_br_bjet_pt       ); 
    outputTree->Branch("nonbjet_pt"    /* N/A             */, &m_br_nonbjet_pt    ); 
    outputTree->Branch("forwardjet_pt" /* N/A             */, &m_br_forwardjet_pt ); 
    outputTree->Branch("jet_pt"        /* "ptjets"        */, &m_br_jet_pt        ); 
    outputTree->Branch("jet_eta"       /* "etajets"       */, &m_br_jet_eta       ); 
    outputTree->Branch("jet_phi"       /* "phijets"       */, &m_br_jet_phi       ); 
    outputTree->Branch("jet_m"         /* "massjets"      */, &m_br_jet_m         ); 
    outputTree->Branch("jet_flav"      /* "flavjets"      */, &m_br_jet_flav      ); 
    outputTree->Branch("met_et"        /* "MET"           */, &m_br_met_et        ); 
    outputTree->Branch("met_phi"       /* "METphi"        */, &m_br_met_phi       ); 
    outputTree->Branch("mT2ll"         /* "MT2"           */, &m_br_mT2ll         ); 
    outputTree->Branch("mll"           /* "Mll"           */, &m_br_mll           ); 
    outputTree->Branch("ptll"          /* N/A             */, &m_br_ptll          ); 
    outputTree->Branch("dphill"        /* N/A             */, &m_br_dphill        ); 
    outputTree->Branch("pbll"          /* "Pbll"          */, &m_br_pbll          ); 
    outputTree->Branch("r1"            /* "R1"            */, &m_br_r1            ); 
    outputTree->Branch("dphi_met_pbll" /* "DPhib"         */, &m_br_dphi_met_pbll ); 
  }


  m_pdfs = LHAPDF::mkPDFs("CT10nlo");

  return EL::StatusCode::SUCCESS;
}


EL::StatusCode Ewk2LTruthAnalysis :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Ewk2LTruthAnalysis :: changeInput (bool /*firstFile*/)
{
  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Ewk2LTruthAnalysis :: initialize ()
{
  // Here you do everything that you need to do after the first input
  // file has been connected and before the first event is processed,
  // e.g. create additional histograms based on which variables are
  // available in the input files.  You can also create all of your
  // histograms and trees in here, but be aware that this method
  // doesn't get called if no events are processed.  So any objects
  // you create here won't be available in the output if you have no
  // input events.
  xAOD::TEvent* event = wk()->xaodEvent();

  // As a check, let's see the number of events in our xAOD
  m_eventCounter = 0;
  Info("initialize()", "Number of events = %lli", event->getEntries() ); // print long long int

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Ewk2LTruthAnalysis :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  // Clear variables
  if(saveTree) {
    m_br_susyID = 0; 
    m_br_isSF = m_br_isDF = m_br_isOS = m_br_isNOHISR = m_br_isSS = false;
    m_br_eventNumber = m_br_met_et = m_br_met_phi = m_br_mT2ll = m_br_dphi_met_pbll = 0.; 
    m_br_mll = m_br_pbll = m_br_ptll = m_br_dphill = m_br_r1 = m_br_eventWeight = 0.;
    m_br_lepton_pt.clear(); 
    m_br_lepton_eta.clear(); 
    m_br_lepton_phi.clear(); 
    m_br_lepton_m.clear(); 
    m_br_lepton_flav.clear();
    m_br_lepton_type.clear();
    m_br_lepton_origin.clear();
    m_br_lepton_mother.clear();
    m_br_lepton_mother_mass.clear();
    m_br_bjet_pt.clear(); 
    m_br_nonbjet_pt.clear(); 
    m_br_forwardjet_pt.clear();
    m_br_jet_pt.clear(); 
    m_br_jet_eta.clear(); 
    m_br_jet_phi.clear(); 
    m_br_jet_m.clear(); 
    m_br_jet_flav.clear();
    m_br_pdfWeights.clear();
    m_br_mcEventWeights.clear();
  }

//   // Event counter
  if( (m_eventCounter % 1000) ==0 ) Info("execute()", "Event number = %i", m_eventCounter );
  m_eventCounter++;

  // Event info
  xAOD::TEvent* event = wk()->xaodEvent();
  const xAOD::EventInfo* eventInfo = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( eventInfo, "EventInfo"));  

  // Retrieve the truth leptons
  const xAOD::TruthParticleContainer* truthParticles = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthParticles, "TruthParticles"));
  const xAOD::TruthParticleContainer* truthElectrons = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthElectrons, "TruthElectrons"));
  const xAOD::TruthParticleContainer* truthMuons = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthMuons, "TruthMuons"));

  int pdgid1 = 0, pdgid2 = 0, susyID = -1;
  const xAOD::TruthParticle *x1m = NULL, *x1p = NULL;
  if(isSignal){
    // Find SUSY ID
    if(!FindSusyHardProc(truthParticles,pdgid1,pdgid2,false)) {
      Info("execute()", "Cannot find SUSY process id for event %i", m_eventCounter );  
    } else {
      if(abs(pdgid1) == abs(pdgid2)) {
        if(abs(pdgid1) == 1000011)      { susyID = 1; }
        else if(abs(pdgid1) == 2000011) { susyID = 2; }
        else if(abs(pdgid1) == 1000013) { susyID = 3; }
        else if(abs(pdgid1) == 2000013) { susyID = 4; }
        else if(abs(pdgid1) == 1000015) { susyID = 5; }
        else if(abs(pdgid1) == 2000015) { susyID = 6; }
        else { susyID = 0; Info("execute()", "Unexpected pair production of |pdgid| %i", abs(pdgid1)); }
      }
      else { susyID = 0; Info("execute()", "Unexpected production of pdgid %ii - %i", pdgid1, pdgid2); }
    }

    // Loop over truth particles to find the sparticles
    for(const auto& truthPar : *truthParticles) {
      if( truthPar->absPdgId() == 1000024 ) {
        if( truthPar->nChildren()!=2 ) continue;
        //Info("execute()"," Found truth chargino in event %i with pdgId %i and mass %.2e and pt %.2e and %i children", m_eventCounter, truthPar->pdgId(), truthPar->m(), truthPar->pt(), truthPar->nChildren());
        if(saveHists) {
          h_hists1D.at(m_nameToIndex["mx1"])->Fill(truthPar->m()*MEVtoGEV);
        }
        if(truthPar->pdgId() > 0) { x1p = truthPar; }
        else                      { x1m = truthPar; }
      }
      if( truthPar->absPdgId() == 1000022 ) {
        if( truthPar->nChildren()!=0 ) continue;
        //Info("execute()"," Found truth neutralino in event %i with pdgId %i and mass %.2e and pt %.2e and %i children", m_eventCounter, truthPar->pdgId(), truthPar->m(), truthPar->pt(), truthPar->nChildren());
        if(saveHists) {
          h_hists1D.at(m_nameToIndex["mn1"])->Fill(truthPar->m()*MEVtoGEV);
        }
      }
    }
  }

  // Loop over truth particles and store electrons and muons
  std::vector<const xAOD::TruthParticle*> *electrons = new std::vector<const xAOD::TruthParticle*>();
  std::vector<const xAOD::TruthParticle*> *muons = new std::vector<const xAOD::TruthParticle*>();

  for(const auto& truthEl : *truthElectrons) {
    if( truthEl->absPdgId() != 11    ) continue; // only electrons
    if( truthEl->status() != 1       ) continue; // only final state objects
    if( truthEl->pt()*MEVtoGEV < 10. ) continue; // pT > 5 GeV 
    if( fabs(truthEl->eta()) > 2.47   ) continue; // |eta| < 2.8 
   
    electrons->push_back(truthEl); // store if passed all
  } // end loop over truth electrons

  for(const auto& truthMu : *truthMuons) {
    if( truthMu->absPdgId() != 13    ) continue; // only muons
    if( truthMu->status() != 1       ) continue; // only final state objects
    if( truthMu->pt()*MEVtoGEV < 10. ) continue; // pT > 5 GeV 
    if( fabs(truthMu->eta()) > 2.4   ) continue; // |eta| < 2.8 
   
    muons->push_back(truthMu); // store if passed all
  } // end loop over truth muons

  // Sort by Pt
  std::sort(electrons->begin(),electrons->end(),SortByPt());
  std::sort(muons->begin(),muons->end(),SortByPt());

  // Retrieve the truth jets
  const xAOD::JetContainer* truthJets = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthJets, "AntiKt4TruthJets"));

  std::vector<const xAOD::Jet*> *jets = new std::vector<const xAOD::Jet*>();

  for(const auto& truthJet : *truthJets) {
    if( truthJet->pt()*MEVtoGEV < 20. ) continue; // pT > 20 GeV 
    if( fabs(truthJet->eta()) > 4.5   ) continue; // |eta| < 4.5
    jets->push_back(truthJet);
  } // end loop over truth jets

  // Sort by Pt
  std::sort(jets->begin(),jets->end(),SortByPt());

  // Overlap removal
  // Remove jets from electrons
  PhysicsTools::l_j_overlap( *electrons, *jets , 0.20, true );
  // Remove electrons from jets
  PhysicsTools::l_j_overlap( *electrons, *jets , 0.40, false);
  // Remove muons from jets
  PhysicsTools::l_j_overlap( *muons    , *jets , 0.40, false);

  // Combine electrons and muons into leptons
  std::vector<const xAOD::TruthParticle*> *leptons = new std::vector<const xAOD::TruthParticle*>();

  for(const auto& truthEl : *electrons) { leptons->push_back(truthEl); }
  for(const auto& truthMu : *muons)     { leptons->push_back(truthMu); }

  // Sort by Pt
  std::sort(leptons->begin(),leptons->end(),SortByPt());

  // Retrieve the truth met
  const xAOD::MissingETContainer* missingET = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( missingET, "MET_Truth"));

  // Only ==2 lepton events and OS
  unsigned int nLep = leptons->size();
  if(saveHists) {
    h_hists1D.at(m_nameToIndex["nLep"])->Fill(nLep);
  }
  if(nLep < 2) return EL::StatusCode::SUCCESS;
  if(leptons->at(0)->pt()<CF_l0_pt || leptons->at(1)->pt()<CF_l1_pt) return EL::StatusCode::SUCCESS;
  //if((leptons->at(0)->pdgId()*leptons->at(1)->pdgId()) > 0) return EL::StatusCode::SUCCESS;


  // Build objects and fill histograms
  TLorentzVector lep0 = leptons->at(0)->p4();
  TLorentzVector lep1 = leptons->at(1)->p4();
  TLorentzVector met;
  met.SetPxPyPzE((*missingET)["NonInt"]->mpx(),
                 (*missingET)["NonInt"]->mpy(),
                 0.,
                 (*missingET)["NonInt"]->met());

  // Basic variables
  bool isSF     = (leptons->at(0)->absPdgId() == leptons->at(1)->absPdgId()) ? true:false;
  bool isDF     = !isSF;
  bool isOS     = (leptons->at(0)->pdgId() * leptons->at(1)->pdgId() < 0) ? true:false;
  bool isSS     = !isOS;
  double mll    = (lep0+lep1).M();
  double pTll   = (lep0+lep1).Pt();
  double dphill = lep0.DeltaPhi(lep1); 
  double pbll   = (lep0+lep1+met).Pt();
  double dphi_met_pbll = met.DeltaPhi(lep0+lep1+met);

  if(saveHists) {
    h_hists1D.at(m_nameToIndex["lep0Pt"]       )->Fill(lep0.Pt()*MEVtoGEV);
    h_hists1D.at(m_nameToIndex["lep0Eta"]      )->Fill(lep0.Eta());
    h_hists1D.at(m_nameToIndex["lep0Phi"]      )->Fill(lep0.Phi());
    h_hists1D.at(m_nameToIndex["lep1Pt"]       )->Fill(lep1.Pt()*MEVtoGEV);
    h_hists1D.at(m_nameToIndex["lep1Eta"]      )->Fill(lep1.Eta());
    h_hists1D.at(m_nameToIndex["lep1Phi"]      )->Fill(lep1.Phi());
    h_hists1D.at(m_nameToIndex["met"]          )->Fill(met.Pt()*MEVtoGEV);
    h_hists1D.at(m_nameToIndex["mll"]          )->Fill((lep0+lep1).M()*MEVtoGEV);
    h_hists1D.at(m_nameToIndex["pTll"]         )->Fill((lep0+lep1).Pt()*MEVtoGEV);
    h_hists1D.at(m_nameToIndex["deltaRll"]     )->Fill(lep0.DeltaR(lep1));
    h_hists1D.at(m_nameToIndex["deltaPhill"]   )->Fill(lep0.DeltaPhi(lep1));
    h_hists1D.at(m_nameToIndex["deltaPhil0met"])->Fill(lep0.DeltaPhi(met));
    h_hists1D.at(m_nameToIndex["deltaPhil1met"])->Fill(lep1.DeltaPhi(met));

    // Compute and fill x1x1 variables
    if( x1p != NULL && x1m != NULL) {
      h_hists1D.at(m_nameToIndex["x1x1Pt"]      )->Fill((x1p->p4()+x1m->p4()).Pt()*MEVtoGEV);
      h_hists1D.at(m_nameToIndex["deltaRx1x1"]  )->Fill(x1p->p4().DeltaR(x1m->p4()));
      h_hists1D.at(m_nameToIndex["deltaPhix1x1"])->Fill(x1p->p4().DeltaPhi(x1m->p4()));
    }
  }

  // Compute and fill mT2 
  ComputeMT2 mycalc = ComputeMT2(lep0,lep1,met,0.,0.); // masses 0. 0.
  double mT2 = mycalc.Compute();
  if(saveHists) {
    h_hists1D.at(m_nameToIndex["mT2"])->Fill(mT2*MEVtoGEV);
  }

  // Compute and fill super-razor
  double r2 = 0., dPhill_vBETA_T = 0., mDeltaR = 0.;
  r2 = met.Pt()/(met.Pt()+lep0.Pt()+lep1.Pt());
  PhysicsTools::superRazor(lep0,lep1,met,dPhill_vBETA_T,mDeltaR);

  if(saveHists) {
    h_hists1D.at(m_nameToIndex["r2"])->Fill(r2);
    h_hists1D.at(m_nameToIndex["dPhill_vBETA_T"])->Fill(dPhill_vBETA_T);
    h_hists1D.at(m_nameToIndex["mDeltaR"])->Fill(mDeltaR*MEVtoGEV);
  }

  // Fill jet variables
  unsigned int nJet = jets->size();
  if(saveHists) {
    h_hists1D.at(m_nameToIndex["nJet"])->Fill(nJet);

    if( nJet > 0) { 
      h_hists1D.at(m_nameToIndex["jet0Pt"] )->Fill(jets->at(0)->p4().Pt()*MEVtoGEV);
      h_hists1D.at(m_nameToIndex["jet0Eta"])->Fill(jets->at(0)->p4().Eta());
      h_hists1D.at(m_nameToIndex["jet0Phi"])->Fill(jets->at(0)->p4().Phi());
    }
    if( nJet > 1) {
      h_hists1D.at(m_nameToIndex["jet1Pt"] )->Fill(jets->at(1)->p4().Pt()*MEVtoGEV);
      h_hists1D.at(m_nameToIndex["jet1Eta"])->Fill(jets->at(1)->p4().Eta());
      h_hists1D.at(m_nameToIndex["jet1Phi"])->Fill(jets->at(1)->p4().Phi());
    }
  }

  // Fill Tree
  if(saveTree) {
    m_br_runNumber      = eventInfo->runNumber();  
    m_br_eventNumber    = eventInfo->eventNumber();  
    m_br_eventWeight    = eventInfo->mcEventWeight();
    h_cutflow_weighted->Fill(0.,m_br_eventWeight);
    m_br_mcEventWeights = eventInfo->mcEventWeights();

    /// pdf reweighting
    const xAOD::TruthEventContainer* truthEvents = 0;
    EL_RETURN_CHECK("execute()",event->retrieve( truthEvents, "TruthEvents"));
    if(truthEvents->size()>0){
      auto pf = (*truthEvents)[0]->pdfInfo();

      for (size_t imem = 0; imem < m_pdfs.size(); imem++) {
        m_br_pdfWeights.push_back( LHAPDF::weightxxQ( pf.pdgId1, pf.pdgId2, pf.x1, pf.x2, pf.Q, m_pdfs[0], m_pdfs[imem]));
//         Info("test", "the weight %lu is %.2f", imem, m_br_pdfWeights[imem]);
       }
    }

    // Leptons
    for(const auto& ipar : *leptons) {
      TLorentzVector ipar_tlv = ipar->p4(); 
      m_br_lepton_pt.push_back(ipar_tlv.Pt()*MEVtoGEV);
      m_br_lepton_eta.push_back(ipar_tlv.Eta());
      m_br_lepton_phi.push_back(ipar_tlv.Phi());
      m_br_lepton_m.push_back(ipar_tlv.M()*MEVtoGEV);
      m_br_lepton_flav.push_back(ipar->pdgId());
      m_br_lepton_type.push_back(ipar->auxdata< unsigned int >("classifierParticleType"));
      m_br_lepton_origin.push_back(ipar->auxdata< unsigned int >("classifierParticleOrigin"));
      /////////////////////////////////////////
      // Home cooked classification 
      // TRUTH1 doesn't have vertices or mothers for leptons in the TruthElectron/TruthMuon containers!!!
      const xAOD::TruthVertex* partOriVert = ipar->hasProdVtx() ? ipar->prodVtx():0;
      const xAOD::TruthParticle* mother = nullptr;
      if( partOriVert!=0 ) {
        for (unsigned int ipIn=0; ipIn<partOriVert->nIncomingParticles(); ++ipIn) {
          if(!(partOriVert->incomingParticle(ipIn))) continue;
          mother = partOriVert->incomingParticle(ipIn);
        }
      }
      m_br_lepton_mother.push_back(mother!=nullptr ? mother->pdgId() : 0);
      m_br_lepton_mother_mass.push_back(mother!=nullptr ? mother->p4().M()*MEVtoGEV : 0);
      /////////////////////////////////////////
    }
    // Jets
    for(const auto& ipar : *jets) {
      TLorentzVector ipar_tlv = ipar->p4(); 
      m_br_jet_pt.push_back(ipar_tlv.Pt()*MEVtoGEV);
      m_br_jet_eta.push_back(ipar_tlv.Eta());
      m_br_jet_phi.push_back(ipar_tlv.Phi());
      m_br_jet_m.push_back(ipar_tlv.M()*MEVtoGEV);
      m_br_jet_flav.push_back(ipar->auxdata<int>("PartonTruthLabelID"));
      if(fabs(ipar_tlv.Eta()<2.4)){
        if(ipar->auxdata<int>("PartonTruthLabelID")==5) {
          m_br_bjet_pt.push_back(ipar_tlv.Pt()*MEVtoGEV);
        } else {
          m_br_nonbjet_pt.push_back(ipar_tlv.Pt()*MEVtoGEV);
        }
      }else{
        m_br_forwardjet_pt.push_back(ipar_tlv.Pt()*MEVtoGEV);
      }
    }
    // Event variables
    m_br_susyID        = susyID; 
    m_br_isSF          = isSF;
    m_br_isDF          = isDF;
    m_br_isSS          = isSS;
    m_br_isOS          = isOS;
    m_br_isNOHISR      = true;
    if(m_br_nonbjet_pt.size()>0) {
      if(m_br_nonbjet_pt.at(0) > 200. || m_br_nonbjet_pt.at(0) < 50.) m_br_isNOHISR = false;
    } 
    m_br_mT2ll         = mT2*MEVtoGEV;
    m_br_mll           = mll*MEVtoGEV; 
    m_br_ptll          = pTll*MEVtoGEV;
    m_br_dphill        = dphill;
    m_br_pbll          = pbll*MEVtoGEV; 
    m_br_met_et        = met.Pt()*MEVtoGEV;
    m_br_met_phi       = met.Phi();
    m_br_dphi_met_pbll = dphi_met_pbll; 
    outputTree->Fill();
  }

  return EL::StatusCode::SUCCESS;
}

bool Ewk2LTruthAnalysis::FindSusyHardProc(const xAOD::TruthParticleContainer *truthP, int& pdgid1, int& pdgid2, bool isTruth3)
{
  pdgid1 = 0;
  pdgid2 = 0;

  //check for TRUTH3 structure first
  if(isTruth3){
    if(!truthP || truthP->size()<2){
      return false;
    }
   
    //get ID of first two BSM particles
    pdgid1 = (*truthP)[0]->pdgId();
    pdgid2 = (*truthP)[1]->pdgId();
    return true;
  }

  //go for TRUTH1-like if not...
  const xAOD::TruthParticle* firstsp(0);
  const xAOD::TruthParticle* secondsp(0);

  if (!truthP || truthP->empty()) {
    return false;
  }
  for (const auto& tp : *truthP) {

    //check ifSUSY particle
    if ((abs(tp->pdgId()) > 1000000 && abs(tp->pdgId()) < 1000007) || // squarkL
        (abs(tp->pdgId()) > 1000010 && abs(tp->pdgId()) < 1000017) || // sleptonL
        (abs(tp->pdgId()) > 2000000 && abs(tp->pdgId()) < 2000007) || // squarkR
        (abs(tp->pdgId()) > 2000010 && abs(tp->pdgId()) < 2000017) || // sleptonR
        (abs(tp->pdgId()) > 1000020 && abs(tp->pdgId()) < 1000040)) { // gauginos

      if (tp->nParents() != 0) {
        if ( tp->parent(0)->absPdgId()  < 1000000) {
          if (!firstsp) {
            firstsp = tp;
          } else if (!secondsp) {
            secondsp = tp;
          } else {
            if (firstsp->nChildren() != 0 && tp->barcode() == firstsp->child(0)->barcode()) {
              firstsp = tp;
            }
            else if (secondsp->nChildren() != 0 && tp->barcode() == secondsp->child(0)->barcode()) {
              secondsp = tp;
            }
            else if (firstsp->nChildren() != 0 && firstsp->child(0)->barcode() == secondsp->barcode()) {
              firstsp = secondsp;
              secondsp = tp;
            }
            else if (secondsp->nChildren() != 0 && secondsp->child(0)->barcode() == firstsp->barcode()) {
              secondsp = firstsp;
              firstsp = tp;
            }
          }
        }
      }
    }
  }

  // quit if no sparticles found
  if (!firstsp && !secondsp) return true; // should find none or two

  if (firstsp->nChildren() == 1) {
    for (const auto& tp : *truthP) {
      if (tp->barcode() == firstsp->child(0)->barcode() && tp->pdgId() != firstsp->pdgId()) {
        firstsp = tp;
        break;
      }
    }
  }

  if (secondsp->nChildren() == 1) {
    for (const auto& tp : *truthP) {
      if (tp->barcode() == secondsp->child(0)->barcode() && tp->pdgId() != secondsp->pdgId()) {
        secondsp = tp;
        break;
      }
    }
  }

  if (abs(firstsp->pdgId()) > 1000000) pdgid1 = firstsp->pdgId();
  if (abs(secondsp->pdgId()) > 1000000) pdgid2 = secondsp->pdgId();

  // Return gracefully:
  return true;
}

EL::StatusCode Ewk2LTruthAnalysis :: postExecute ()
{
  // Here you do everything that needs to be done after the main event
  // processing.  This is typically very rare, particularly in user
  // code.  It is mainly used in implementing the NTupleSvc.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Ewk2LTruthAnalysis :: finalize ()
{
  // This method is the mirror image of initialize(), meaning it gets
  // called after the last event has been processed on the worker node
  // and allows you to finish up any objects you created in
  // initialize() before they are written to disk.  This is actually
  // fairly rare, since this happens separately for each worker node.
  // Most of the time you want to do your post-processing on the
  // submission node after all your histogram outputs have been
  // merged.  This is different from histFinalize() in that it only
  // gets called on worker nodes that processed input events.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Ewk2LTruthAnalysis :: histFinalize ()
{
  // This method is the mirror image of histInitialize(), meaning it
  // gets called after the last event has been processed on the worker
  // node and allows you to finish up any objects you created in
  // histInitialize() before they are written to disk.  This is
  // actually fairly rare, since this happens separately for each
  // worker node.  Most of the time you want to do your
  // post-processing on the submission node after all your histogram
  // outputs have been merged.  This is different from finalize() in
  // that it gets called on all worker nodes regardless of whether
  // they processed input events.
  return EL::StatusCode::SUCCESS;
}
