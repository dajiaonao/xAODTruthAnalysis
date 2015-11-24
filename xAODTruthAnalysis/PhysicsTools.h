#ifndef PHYSICSTOOLS_H
#define PHYSICSTOOLS_H

#include "TMath.h"
#include "TLorentzVector.h"

// EDM include(s):
#include "xAODTruth/TruthParticle.h"
#include "xAODJet/Jet.h"

namespace PhysicsTools {

  // Compute MC (cotransverse mass)
  double getMC(TLorentzVector& v1, TLorentzVector& v2);
  // Compute MCT (contransverse mass)
  double getMCT(TLorentzVector& v1, TLorentzVector& v2);
  // Compute MCTPerp (perpendicular contransverse mass)
  double getMCTPerp(TLorentzVector& v1, TLorentzVector& v2, TLorentzVector& u);
  // Compute MCTPara (parallel contransverse mass)
  double getMCTPara(TLorentzVector& v1, TLorentzVector& v2, TLorentzVector& u);
  // Lorentz contralinear boost invariant 4-dot product
  double contralinearDot(TLorentzVector& v1, TLorentzVector& v2);
  // Calculate various super-razor variables
  void superRazor( TLorentzVector l0, 
                   TLorentzVector l1,
                   TLorentzVector met,
                   //TVector3& vBETA_z, 
                   //TVector3& pT_CM,
                   //TVector3& vBETA_T_CMtoR, 
                   //TVector3& vBETA_R,
                   //double& SHATR, 
                   double& dphi_LL_vBETA_T, 
                   //double& dphi_L1_L2,
                   //double& gamma_R, 
                   //double& dphi_vBETA_R_vBETA_T,
                   double& MDELTAR//, 
                   //double& costhetaRp1 
                 );
  // Overlap removal
  void l_j_overlap ( std::vector<const xAOD::TruthParticle*>& leptons,
                     std::vector<const xAOD::Jet*>& jets,
                     double dRmin, bool removeJets);
}

#endif
