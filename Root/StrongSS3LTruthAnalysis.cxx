#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <xAODTruthAnalysis/StrongSS3LTruthAnalysis.h>

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
//#include "xAODTruth/TruthParticleContainer.h"
#include "xAODMissingET/MissingETContainer.h"
#include "xAODJet/Jet.h"
#include "xAODJet/JetContainer.h"

// Analysis include(s):
#include <xAODTruthAnalysis/MT2_ROOT.h>
#include <xAODTruthAnalysis/PhysicsTools.h>

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
ClassImp(StrongSS3LTruthAnalysis)



StrongSS3LTruthAnalysis :: StrongSS3LTruthAnalysis ()
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  Note that you should only put
  // the most basic initialization here, since this method will be
  // called on both the submission and the worker node.  Most of your
  // initialization code will go into histInitialize() and
  // initialize().
}



EL::StatusCode StrongSS3LTruthAnalysis :: setupJob (EL::Job& job)
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



EL::StatusCode StrongSS3LTruthAnalysis :: histInitialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.

  h_cutflow_weighted = new TH1D("CutflowWeighted","CutflowWeighted",10,0.,10.);
  h_cutflow_weighted->Sumw2();

  // Output Tree
  if(saveTree) {
    TFile *outputFile = wk()->getOutputFile (outputFileName);
    outputTree = new TTree("SuperTruth"/*"susytree"*/,"SuperTruth"/*"susytree"*/);
    h_cutflow_weighted->SetDirectory(outputFile); // Not the best solution, if both Hist and Tree written only shows up in the Tree
    outputTree->SetDirectory(outputFile);
    outputTree->Branch("runNumber"     /* "RunNumber"     */, &m_br_runNumber     ); 
    outputTree->Branch("eventNumber"   /* "EventNumber"   */, &m_br_eventNumber   ); 
    outputTree->Branch("mcEventWeight" /* "EventWeight"   */, &m_br_eventWeight   ); 
    outputTree->Branch("mcEventWeights"/* "mcEventWeights"*/, &m_br_mcEventWeights); 
    outputTree->Branch("susyID"        /* "susyID"        */, &m_br_susyID        ); 
    outputTree->Branch("isSF"          /* "isSF"          */, &m_br_isSF          ); 
    outputTree->Branch("isDF"          /* "isDF"          */, &m_br_isDF          ); 
    outputTree->Branch("isSS"          /* "isSS"          */, &m_br_isSS          ); 
    outputTree->Branch("isOS"          /* "isOS"          */, &m_br_isOS          ); 
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
    outputTree->Branch("dphi_met_pbll" /* "DPhib"         */, &m_br_dphi_met_pbll ); 
  }

  return EL::StatusCode::SUCCESS;
}


EL::StatusCode StrongSS3LTruthAnalysis :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode StrongSS3LTruthAnalysis :: changeInput (bool /*firstFile*/)
{
  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode StrongSS3LTruthAnalysis :: initialize ()
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



EL::StatusCode StrongSS3LTruthAnalysis :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  // Clear variables
  if(saveTree) {
    m_br_susyID = 0; 
    m_br_isSF = m_br_isDF = m_br_isOS = m_br_isSS = false;
    m_br_eventNumber = m_br_met_et = m_br_met_phi = m_br_mT2ll = m_br_dphi_met_pbll = 0.; 
    m_br_mll = m_br_pbll = m_br_ptll = m_br_dphill = m_br_eventWeight = 0.;
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
    m_br_jet_pt.clear(); 
    m_br_jet_eta.clear(); 
    m_br_jet_phi.clear(); 
    m_br_jet_m.clear(); 
    m_br_jet_flav.clear();
    m_br_mcEventWeights.clear();
  }

  // Event counter
  if( (m_eventCounter % 1000) ==0 ) Info("execute()", "Event number = %i", m_eventCounter );
  m_eventCounter++;

  // Event info
  xAOD::TEvent* event = wk()->xaodEvent();
  const xAOD::EventInfo* eventInfo = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( eventInfo, "EventInfo"));  
  float eventWeight = eventInfo->mcEventWeight();
  h_cutflow_weighted->Fill(0.,eventWeight);

  // Retrieve the truth leptons
  const xAOD::TruthParticleContainer* truthParticles = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthParticles, "TruthParticles"));
  const xAOD::TruthParticleContainer* truthElectrons = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthElectrons, "TruthElectrons"));
  const xAOD::TruthParticleContainer* truthMuons = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthMuons, "TruthMuons"));

  // Find SUSY ID
  int pdgid1 = 0, pdgid2 = 0;
  if(!FindSusyHardProc(truthParticles,pdgid1,pdgid2,false)) {
    Info("execute()", "Cannot find SUSY process id for event %i", m_eventCounter );  
  } 

  // Loop over truth particles and store electrons and muons
  std::vector<const xAOD::TruthParticle*> *electrons = new std::vector<const xAOD::TruthParticle*>();
  std::vector<const xAOD::TruthParticle*> *muons = new std::vector<const xAOD::TruthParticle*>();

  for(const auto& truthEl : *truthElectrons) {
    if( truthEl->absPdgId() != 11    ) continue; // only electrons
    if( truthEl->status() != 1       ) continue; // only final state objects
    if( truthEl->pt()*MEVtoGEV < 10. ) continue; // pT > 10 GeV 
    if( fabs(truthEl->eta()) > 2.5   ) continue; // |eta| < 2.5 
   
    electrons->push_back(truthEl); // store if passed all
  } // end loop over truth electrons

  for(const auto& truthMu : *truthMuons) {
    if( truthMu->absPdgId() != 13    ) continue; // only muons
    if( truthMu->status() != 1       ) continue; // only final state objects
    if( truthMu->pt()*MEVtoGEV < 10. ) continue; // pT > 10 GeV 
    if( fabs(truthMu->eta()) > 2.5   ) continue; // |eta| < 2.5 
   
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

  // Only >=2 lepton events
  unsigned int nLep = leptons->size();
  if(nLep < 2) return EL::StatusCode::SUCCESS;

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

  // Compute and fill mT2 
  ComputeMT2 mycalc = ComputeMT2(lep0,lep1,met,0.,0.); // masses 0. 0.
  double mT2 = mycalc.Compute();

  // Compute and fill super-razor
  double dPhill_vBETA_T = 0., mDeltaR = 0.;
  PhysicsTools::superRazor(lep0,lep1,met,dPhill_vBETA_T,mDeltaR);

  // Fill Tree
  if(saveTree) {
    m_br_runNumber      = eventInfo->runNumber();  
    m_br_eventNumber    = eventInfo->eventNumber();  
    m_br_eventWeight    = eventInfo->mcEventWeight();
    m_br_mcEventWeights = eventInfo->mcEventWeights();
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
      if(ipar->auxdata<int>("PartonTruthLabelID")==5) {
        m_br_bjet_pt.push_back(ipar_tlv.Pt()*MEVtoGEV);
      } else {
        m_br_nonbjet_pt.push_back(ipar_tlv.Pt()*MEVtoGEV);
      }
    }
    // Event variables
    m_br_isSF          = isSF;
    m_br_isDF          = isDF;
    m_br_isSS          = isSS;
    m_br_isOS          = isOS;
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

bool StrongSS3LTruthAnalysis::FindSusyHardProc(const xAOD::TruthParticleContainer *truthP, int& pdgid1, int& pdgid2, bool isTruth3)
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

EL::StatusCode StrongSS3LTruthAnalysis :: postExecute ()
{
  // Here you do everything that needs to be done after the main event
  // processing.  This is typically very rare, particularly in user
  // code.  It is mainly used in implementing the NTupleSvc.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode StrongSS3LTruthAnalysis :: finalize ()
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



EL::StatusCode StrongSS3LTruthAnalysis :: histFinalize ()
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
