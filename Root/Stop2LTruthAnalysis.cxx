#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <xAODTruthAnalysis/Stop2LTruthAnalysis.h>

// STD include(s):
#include <algorithm>    // std::sort
#include <stdio.h>      // sscanf

// Infrastructure include(s):
#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/tools/Message.h"

// EDM include(s):
#include "xAODEventInfo/EventInfo.h"
//#include "xAODTruth/TruthEventContainer.h"
#include "xAODTruth/TruthVertex.h"
#include "xAODTruth/TruthParticle.h"
#include "xAODTruth/TruthParticleContainer.h"
#include "xAODMissingET/MissingETContainer.h"
#include "xAODJet/Jet.h"
#include "xAODJet/JetContainer.h"

// Analysis include(s):
#include <xAODTruthAnalysis/MT2_ROOT.h>
#include <xAODTruthAnalysis/PhysicsTools.h>
//#include <StopPolarization/PolarizationReweight.h>

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
ClassImp(Stop2LTruthAnalysis)



Stop2LTruthAnalysis :: Stop2LTruthAnalysis ()
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  Note that you should only put
  // the most basic initialization here, since this method will be
  // called on both the submission and the worker node.  Most of your
  // initialization code will go into histInitialize() and
  // initialize().

  //m_weight_files.push_back(new TFile("/data7/atlas/amete/StopPolarization/Analysis/xAODTruthAnalysis/macros/MassWeight.root"));
  //m_weight_graphs.push_back((TGraph*) m_weight_files.at(0)->Get("Right")); 
  //m_weight_graphs.push_back((TGraph*) m_weight_files.at(0)->Get("Left")); 
}



EL::StatusCode Stop2LTruthAnalysis :: setupJob (EL::Job& job)
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



EL::StatusCode Stop2LTruthAnalysis :: histInitialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.

  h_cutflow_weighted = new TH1D("CutflowWeighted","CutflowWeighted",10,0.,10.);
  h_cutflow_weighted->Sumw2();

  if(saveHists) {
    wk()->addOutput(h_cutflow_weighted);

    const std::string histoNames1D[m_nHists1D] = { "nLep 5 -0.5 4.5",
                                                   "lep0Pt 50 0 500", 
                                                   "lep0Eta 30 -3 3",  
                                                   "lep0Phi 18 -3.6 3.6", 
                                                   "lep1Pt 50 0 500", 
                                                   "lep1Eta 30 -3 3",  
                                                   "lep1Phi 18 -3.6 3.6", 
                                                   "deltaRll 30 0 6",
                                                   "deltaPhill 18 -3.6 3.6",
                                                   "mll 50 0 500",   
                                                   "pTll 50 0 500", 
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
                                                   "sTsTPt 50 0 1000",
                                                   "deltaRsTsT 50 0 10",
                                                   "deltaPhisTsT 18 -3.6 3.6",
                                                   "cosThetaL 50 -1 1",
                                                   "stop0mass 1000 -0.5 999.5",
                                                   "stop1mass 1000 -0.5 999.5",
                                                   "stop0pt 50 0 500",
                                                   "stop1pt 50 0 500",
                                                   "wboson0mass 500 0 500",
                                                   "wboson1mass 500 0 500",
                                                   "wboson0pt 50 0 500",
                                                   "wboson1pt 50 0 500",
                                                   "bquark0pt 50 0 500",
                                                   "bquark1pt 50 0 500",
                                                   "wlepton0pt 50 0 500",
                                                   "wlepton1pt 50 0 500",
                                                   "neutralino0mass 500 0 500",
                                                   "neutralino1mass 500 0 500",
                                                   "neutralino0pt 50 0 500",
                                                   "neutralino1pt 50 0 500",
                                                   "top0mass 500 0 500",
                                                   "top1mass 500 0 500"
                                               };

    int nbin=0;  float xmin=0; float xmax=0; char hName[50]; TH1D* temp;
    for( unsigned int i=0; i<m_nHists1D; ++i) {
      // Create and store the histograms
      sscanf(histoNames1D[i].c_str(),"%s %i %f %f",hName,&nbin,&xmin,&xmax);
      temp = new TH1D(hName,hName,nbin,xmin,xmax);
      temp->Sumw2();
      h_hists1D.push_back(temp);
      wk()->addOutput(h_hists1D.at(i));     
      // For easy filling
      m_nameToIndex1D.insert( std::pair<std::string,unsigned int>(std::string(hName),i) );
    }

    const std::string histoNames2D[m_nHists2D] = { "nLEPvsMET 5 -0.5 4.5 2 0. 120.",
                                                   "topMassVSbpt 20 0 100 30 0 300" };

    int nbiny=0;  float ymin=0; float ymax=0; TH2D* temp2D;
    for( unsigned int i=0; i<m_nHists2D; ++i) {
      // Create and store the histograms
      sscanf(histoNames2D[i].c_str(),"%s %i %f %f %i %f %f",hName,&nbin,&xmin,&xmax,&nbiny,&ymin,&ymax);
      temp2D = new TH2D(hName,hName,nbin,xmin,xmax,nbiny,ymin,ymax);
      temp2D->Sumw2();
      h_hists2D.push_back(temp2D);
      wk()->addOutput(h_hists2D.at(i));
      // For easy filling
      m_nameToIndex2D.insert( std::pair<std::string,unsigned int>(std::string(hName),i) );
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
    outputTree->Branch("mcEventWeight" /* "EventWeight"   */, &m_br_eventWeight   ); 
    outputTree->Branch("mcEventWeights"/* "mcEventWeights"*/, &m_br_mcEventWeights); 
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
    outputTree->Branch("jet_pt"        /* "ptjets"        */, &m_br_jet_pt        ); 
    outputTree->Branch("jet_eta"       /* "etajets"       */, &m_br_jet_eta       ); 
    outputTree->Branch("jet_phi"       /* "phijets"       */, &m_br_jet_phi       ); 
    outputTree->Branch("jet_m"         /* "massjets"      */, &m_br_jet_m         ); 
    outputTree->Branch("jet_flav"      /* "flavjets"      */, &m_br_jet_flav      ); 
    outputTree->Branch("met_et"        /* "MET"           */, &m_br_met_et        ); 
    outputTree->Branch("met_phi"       /* "METphi"        */, &m_br_met_phi       ); 
    outputTree->Branch("mT2ll"         /* "MT2"           */, &m_br_mT2ll         ); 
    outputTree->Branch("mll"           /* "Mll"           */, &m_br_mll           ); 
    outputTree->Branch("pbll"          /* "Pbll"          */, &m_br_pbll          ); 
    outputTree->Branch("r1"            /* "R1"            */, &m_br_r1            ); 
    outputTree->Branch("dphi_met_pbll" /* "DPhib"         */, &m_br_dphi_met_pbll ); 
  }

  return EL::StatusCode::SUCCESS;
}


EL::StatusCode Stop2LTruthAnalysis :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Stop2LTruthAnalysis :: changeInput (bool /*firstFile*/)
{
  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Stop2LTruthAnalysis :: initialize ()
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

  // Setup MCTruthClassifier
  if(m_mcTruthClassifier == nullptr) m_mcTruthClassifier = new MCTruthClassifier("myMCTruthClassifier"); 
  EL_RETURN_CHECK( "setup MCTruthClassifier()", m_mcTruthClassifier->initialize());

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Stop2LTruthAnalysis :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  // Clear variables
  if(saveTree) {
    m_br_isSF = m_br_isDF = m_br_isOS = m_br_isSS = false;
    m_br_eventNumber = m_br_met_et = m_br_met_phi = m_br_mT2ll = m_br_dphi_met_pbll = 0.; 
    m_br_mll = m_br_pbll = m_br_r1 = m_br_eventWeight = 0.;
    m_br_lepton_pt.clear(); 
    m_br_lepton_eta.clear(); 
    m_br_lepton_phi.clear(); 
    m_br_lepton_m.clear(); 
    m_br_lepton_flav.clear();
    m_br_lepton_type.clear();
    m_br_lepton_origin.clear();
    m_br_lepton_mother.clear();
    m_br_lepton_mother_mass.clear();
    m_br_jet_pt.clear(); 
    m_br_jet_eta.clear(); 
    m_br_jet_phi.clear(); 
    m_br_jet_m.clear(); 
    m_br_jet_flav.clear();
    m_br_mcEventWeights.clear();
  }

  // Event info
  xAOD::TEvent* event = wk()->xaodEvent();
  const xAOD::EventInfo* eventInfo = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( eventInfo, "EventInfo"));  

  //// Truth Event
  //const xAOD::TruthEventContainer* truthEvents = 0;
  //EL_RETURN_CHECK("execute()",event->retrieve( truthEvents, "TruthEvents"));  
  ////// truthEvents->at(0)->weights().at(0) == eventInfo->mcEventWeights().at(0)

  // Event counter and weight
  m_eventCounter++;
  float eventWeight = eventInfo->mcEventWeight();
  h_cutflow_weighted->Fill(0.,eventWeight);
  //if(m_eventCounter==1) {
  //  TString histoName; histoName.Form("CutflowWeighted_%i",eventInfo->runNumber()); 
  //  h_cutflow_weighted->SetName(histoName);
  //  h_cutflow_weighted->SetName(histoName);
  //}

  // Retrieve the truth leptons
  const xAOD::TruthParticleContainer* truthParticles = 0;
  EL_RETURN_CHECK("execute()",event->retrieve( truthParticles, "TruthParticles"));
  const xAOD::TruthParticleContainer* truthElectrons = 0;
  const xAOD::TruthParticleContainer* truthMuons = 0;
  if(!isRecoSample) {
    EL_RETURN_CHECK("execute()",event->retrieve( truthElectrons, "TruthElectrons"));
    EL_RETURN_CHECK("execute()",event->retrieve( truthMuons, "TruthMuons"));
  } else {
    EL_RETURN_CHECK("execute()",event->retrieve( truthElectrons, "TruthParticles"));
    EL_RETURN_CHECK("execute()",event->retrieve( truthMuons, "TruthParticles"));
  }
 
  // Signal specific code
  if(isSignal) {

    // Loop over truth particles to find the stop
    const xAOD::TruthParticle *stop           = nullptr, 
                              *bquark         = nullptr, 
                              *neutralino     = nullptr, 
                              *wboson         = nullptr, 
                              *wlepton        = nullptr;
                              //*wneutrino      = nullptr;
    const xAOD::TruthParticle *stops[2]       = { nullptr }, 
                              *bquarks[2]     = { nullptr },
                              *neutralinos[2] = { nullptr },
                              *wbosons[2]     = { nullptr },
                              *wleptons[2]    = { nullptr };
                              //*wneutrinos[2]  = { nullptr };
    bool selfDecay = false;

    // Loop over truth particles to find stops and their children 
    for(const auto& truthPar : *truthParticles) {
      // Stop
      if(truthPar->absPdgId()==1000006) {
        stop = truthPar;
        if(stop->nChildren()>0) {
          selfDecay = false;
          for(unsigned int i=0; i<stop->nChildren(); i++) {
            const xAOD::TruthParticle* child = stop->child(i);
            if(child->pdgId()==stop->pdgId()) {
              stop = child;
              selfDecay = true;
              break;
            } // end of self decay if
            else if (child->absPdgId()==1000022) {
              neutralino = child;
              if(stop->pdgId()>0)  neutralinos[0] = neutralino;
              else                 neutralinos[1] = neutralino;
            } // end of N1 if
            else if (child->isW()) {
              wboson = child;
              if(child->pdgId()>0) wbosons[0] = wboson;
              else                 wbosons[1] = wboson;
            } // end of W if
            else if (child->absPdgId()==5) {
              bquark = child;
              if(child->pdgId()>0) bquarks[0] = bquark; 
              else                 bquarks[1] = bquark;
            } // end of b if
          } // end of child loop
        } // end of stop nChildren if
      } // end of stop if

      if( selfDecay ) continue;   

      if(stop==nullptr) continue;

      if(stop->pdgId()>0) stops[0] = stop;
      else                stops[1] = stop;
    }

    // Check of all particles exist
    if(
       stops[0] == nullptr       || stops[1] == nullptr       ||
       wbosons[0] == nullptr     || wbosons[1] == nullptr     ||
       neutralinos[0] == nullptr || neutralinos[1] == nullptr ||
       bquarks[0] == nullptr     || bquarks[1] == nullptr     
      ) return EL::StatusCode::SUCCESS;

    // Now find leptons from Ws
    selfDecay=false;
    wboson = wbosons[0];
    do{
      for(unsigned int i=0; i<wboson->nChildren();i++) {
        selfDecay=false;
        const xAOD::TruthParticle* child = wboson->child(i);
        if( child->pdgId()==wboson->pdgId() ){
          wboson = child;
          selfDecay = true;
          break;
        }
        else if ( child->isChLepton() ) {
          wlepton = child;
          wleptons[0] = wlepton;
        }
      }
    } while(selfDecay);

    selfDecay=false;
    wboson = wbosons[1];
    do{
      for(unsigned int i=0; i<wboson->nChildren();i++) {
        selfDecay=false;
        const xAOD::TruthParticle* child = wboson->child(i);
        if( child->pdgId()==wboson->pdgId() ){
          wboson = child;
          selfDecay = true;
          break;
        }
        else if ( child->isChLepton() ) {
          wlepton = child;
          wleptons[1] = wlepton;
        }
      }
    } while(selfDecay);

    // Make sure the leptons exist
    if(wleptons[0] == nullptr || wleptons[1] == nullptr) {
      return EL::StatusCode::SUCCESS; 
    }

    // Calculate the boosts
    double thetal[2] = {0.};
    for(unsigned int ipar=0; ipar<2; ipar++) {
      TLorentzVector top_hlv        = wbosons[ipar]->p4() + bquarks[ipar]->p4();
      TLorentzVector lepton_hlv     = wleptons[ipar]->p4();
      TLorentzVector neutralino_hlv = neutralinos[ipar]->p4();
      TVector3 boostVec             = top_hlv.BoostVector();
      lepton_hlv.Boost(-boostVec);
      neutralino_hlv.Boost(-boostVec);
      thetal[ipar]                  = neutralino_hlv.Angle(lepton_hlv.Vect());
    }

    //////////////////////////////////
    //// TEST TAKASHI
    //StopPolarization::PolarizationReweight *polreweight = new StopPolarization::PolarizationReweight;
    //polreweight->setUnitMeV(); // set MeV
    //polreweight->setMassW(80399.); 
    //polreweight->setWidthW(2085.);
    //polreweight->setMassZ(91187.6);
    //polreweight->setWidthZ(2495.2);
    //polreweight->setMassWThreshold(0.);
    //polreweight->setMassZThreshold(0.);
    //std::string generatorName = "MadGraphPythia8";
    //polreweight->setGeneratorName(generatorName);
    //polreweight->setDecayPythia(true);
    //polreweight->setPhaseSpaceOnly(true);
    //double weight = polreweight->getReweightTopNeutralino(truthParticles, 0.785419, 1.40637);
    //delete polreweight;
    ////////////////////////////////

    // Compute and fill core event variables
    if(saveHists) {
      h_hists1D.at(m_nameToIndex1D["stop0mass"]      )->Fill(stops[0]->p4().M()*MEVtoGEV                      ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["stop1mass"]      )->Fill(stops[1]->p4().M()*MEVtoGEV                      ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["stop0pt"]        )->Fill(stops[0]->p4().Pt()*MEVtoGEV                     ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["stop1pt"]        )->Fill(stops[1]->p4().Pt()*MEVtoGEV                     ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["sTsTPt"]         )->Fill((stops[0]->p4()+stops[1]->p4()).Pt()*MEVtoGEV    ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["deltaRsTsT"]     )->Fill(stops[0]->p4().DeltaR(stops[1]->p4())            ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["deltaPhisTsT"]   )->Fill(stops[0]->p4().DeltaPhi(stops[1]->p4())          ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["top0mass"]       )->Fill((wbosons[0]->p4()+bquarks[0]->p4()).M()*MEVtoGEV ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["top1mass"]       )->Fill((wbosons[1]->p4()+bquarks[1]->p4()).M()*MEVtoGEV ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["wboson0mass"]    )->Fill(wbosons[0]    ->p4().M() *MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["wboson1mass"]    )->Fill(wbosons[1]    ->p4().M() *MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["wboson0pt"]      )->Fill(wbosons[0]    ->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["wboson1pt"]      )->Fill(wbosons[1]    ->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["wlepton0pt"]     )->Fill(wleptons[0]   ->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["wlepton1pt"]     )->Fill(wleptons[1]   ->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["bquark0pt"]      )->Fill(bquarks[0]    ->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["bquark1pt"]      )->Fill(bquarks[1]    ->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["neutralino0mass"])->Fill(neutralinos[0]->p4().M() *MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["neutralino1mass"])->Fill(neutralinos[1]->p4().M() *MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["neutralino0pt"]  )->Fill(neutralinos[0]->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["neutralino1pt"]  )->Fill(neutralinos[1]->p4().Pt()*MEVtoGEV               ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["cosThetaL"]      )->Fill(cos(thetal[0])                                   ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["cosThetaL"]      )->Fill(cos(thetal[1])                                   ,eventWeight);
    } // end of save signal hists                                           
  } // end of signal specific calculations                                  

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

  // Fill histograms
  unsigned int nLep = leptons->size();
  if(saveHists) {
    h_hists1D.at(m_nameToIndex1D["nLep"])->Fill(nLep,eventWeight);
  }

  // Only ==2 OS lepton events
  if(nLep != 2) return EL::StatusCode::SUCCESS;
  if((leptons->at(0)->pdgId()*leptons->at(1)->pdgId()) > 0) return EL::StatusCode::SUCCESS;

  // Build objects and fill histograms
  TLorentzVector lep0_tlv = leptons->at(0)->p4();
  TLorentzVector lep1_tlv = leptons->at(1)->p4();
  TLorentzVector met_tlv;
  met_tlv.SetPxPyPzE((*missingET)["NonInt"]->mpx(),
                     (*missingET)["NonInt"]->mpy(),
                     0.,
                     (*missingET)["NonInt"]->met());

  // Basic variables
  bool isSF   = (leptons->at(0)->absPdgId() == leptons->at(1)->absPdgId()) ? true:false;
  bool isDF   = !isSF;
  bool isOS   = (leptons->at(0)->pdgId() * leptons->at(1)->pdgId() < 0) ? true:false;
  bool isSS   = !isOS;
  double mll  = (lep0_tlv+lep1_tlv).M();
  double pTll = (lep0_tlv+lep1_tlv).Pt();
  double pbll = (lep0_tlv+lep1_tlv+met_tlv).Pt();
  double dphi_met_pbll = met_tlv.DeltaPhi(lep0_tlv+lep1_tlv+met_tlv);
  double meff = lep0_tlv.Pt()+lep1_tlv.Pt()+met_tlv.Pt();
  int jCounter = 0; 
  for(const auto& ijet : *jets) {
    if(jCounter==2)                    break;    // only add first two jets
    if(ijet->p4().Pt()*MEVtoGEV < 50.) continue; // only jets w/ pt > 50 GeV 
    if(fabs(ijet->eta()) > 2.5)        continue; // only jets w/ |eta| < 2.5 
    meff += ijet->p4().Pt();
    jCounter++;
  }

  if(saveHists) {
    h_hists1D.at(m_nameToIndex1D["lep0Pt"]       )->Fill(lep0_tlv.Pt()*MEVtoGEV     ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["lep0Eta"]      )->Fill(lep0_tlv.Eta()             ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["lep0Phi"]      )->Fill(lep0_tlv.Phi()             ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["lep1Pt"]       )->Fill(lep1_tlv.Pt()*MEVtoGEV     ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["lep1Eta"]      )->Fill(lep1_tlv.Eta()             ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["lep1Phi"]      )->Fill(lep1_tlv.Phi()             ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["met"]          )->Fill(met_tlv.Pt()*MEVtoGEV      ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["mll"]          )->Fill(mll*MEVtoGEV               ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["pTll"]         )->Fill(pTll*MEVtoGEV              ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["deltaRll"]     )->Fill(lep0_tlv.DeltaR(lep1_tlv)  ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["deltaPhill"]   )->Fill(lep0_tlv.DeltaPhi(lep1_tlv),eventWeight);
    h_hists1D.at(m_nameToIndex1D["deltaPhil0met"])->Fill(lep0_tlv.DeltaPhi(met_tlv) ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["deltaPhil1met"])->Fill(lep1_tlv.DeltaPhi(met_tlv) ,eventWeight);
  }

  // Compute and fill mT2 
  ComputeMT2 mycalc = ComputeMT2(lep0_tlv,lep1_tlv,met_tlv,0.,0.); // masses 0. 0.
  double mT2 = mycalc.Compute();
  if(saveHists) {
    h_hists1D.at(m_nameToIndex1D["mT2"])->Fill(mT2*MEVtoGEV,eventWeight);
  }

  // Compute and fill super-razor
  double r1 = 0., r2 = 0., dPhill_vBETA_T = 0., mDeltaR = 0.;
  r1 = met_tlv.Pt()/meff; 
  r2 = met_tlv.Pt()/(met_tlv.Pt()+lep0_tlv.Pt()+lep1_tlv.Pt());
  PhysicsTools::superRazor(lep0_tlv,lep1_tlv,met_tlv,dPhill_vBETA_T,mDeltaR);

  if(saveHists) { 
    h_hists1D.at(m_nameToIndex1D["r2"]            )->Fill(r2              ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["dPhill_vBETA_T"])->Fill(dPhill_vBETA_T  ,eventWeight);
    h_hists1D.at(m_nameToIndex1D["mDeltaR"]       )->Fill(mDeltaR*MEVtoGEV,eventWeight);
  }

  // Fill jet variables
  unsigned int nJet = jets->size();
  if(saveHists) {
    h_hists1D.at(m_nameToIndex1D["nJet"])->Fill(nJet,eventWeight);

    if( nJet > 0) {
      TLorentzVector jet0 = jets->at(0)->p4();
      h_hists1D.at(m_nameToIndex1D["jet0Pt"] )->Fill(jet0.Pt()*MEVtoGEV,eventWeight);
      h_hists1D.at(m_nameToIndex1D["jet0Eta"])->Fill(jet0.Eta()        ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["jet0Phi"])->Fill(jet0.Phi()        ,eventWeight);
    }
    if( nJet > 1) {
      TLorentzVector jet1 = jets->at(1)->p4();
      h_hists1D.at(m_nameToIndex1D["jet1Pt"] )->Fill(jet1.Pt()*MEVtoGEV,eventWeight);
      h_hists1D.at(m_nameToIndex1D["jet1Eta"])->Fill(jet1.Eta()        ,eventWeight);
      h_hists1D.at(m_nameToIndex1D["jet1Phi"])->Fill(jet1.Phi()        ,eventWeight);
    }
  }

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
    }
    // Event variables
    m_br_isSF          = isSF;
    m_br_isDF          = isDF;
    m_br_isSS          = isSS;
    m_br_isOS          = isOS;
    m_br_mT2ll         = mT2*MEVtoGEV;
    m_br_mll           = mll*MEVtoGEV; 
    m_br_pbll          = pbll*MEVtoGEV; 
    m_br_r1            = r1; 
    m_br_met_et        = met_tlv.Pt()*MEVtoGEV;
    m_br_met_phi       = met_tlv.Phi();
    m_br_dphi_met_pbll = dphi_met_pbll; 
    outputTree->Fill();
  }

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Stop2LTruthAnalysis :: postExecute ()
{
  // Here you do everything that needs to be done after the main event
  // processing.  This is typically very rare, particularly in user
  // code.  It is mainly used in implementing the NTupleSvc.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Stop2LTruthAnalysis :: finalize ()
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

  EL_RETURN_CHECK( "setup MCTruthClassifier()", m_mcTruthClassifier->finalize());
  delete m_mcTruthClassifier;
  m_mcTruthClassifier=nullptr;

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode Stop2LTruthAnalysis :: histFinalize ()
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
