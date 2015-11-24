#include "xAODTruthAnalysis/PhysicsTools.h"

// D. R. Tovey, JHEP 0804, 034 (2008) [arXiv:0802.2879 [hep-ph]]
// Compute MC (cotransverse mass)
double PhysicsTools::getMC(TLorentzVector& v1, TLorentzVector& v2) 
{
  double mCSQ = v1.M2() + v2.M2() + 2.0*contralinearDot(v1,v2);
  return ((mCSQ > 0.) ? sqrt(mCSQ) : 0.);
}

// D. R. Tovey, JHEP 0804, 034 (2008) [arXiv:0802.2879 [hep-ph]]
// Compute MCT (contransverse mass)
// Note that Et**2 = Pt**2 + m**2 (not mT**2 !!!)
double PhysicsTools::getMCT(TLorentzVector& v1, TLorentzVector& v2) 
{
  double ETv1  = sqrt(v1.Perp2() + v1.M2());
  double ETv2  = sqrt(v2.Perp2() + v2.M2());

  double mCTSQ = pow(ETv1 + ETv2,2) - (v1-v2).Perp2();
  return ((mCTSQ > 0.) ? sqrt(mCTSQ) : 0.);
}

// DON'T USE THIS FUNCTION YET, STILL UNDER SCRUNITY !!!!!!!!!!!!!!!!!!!!!!!
// Konstantin T. Matchev and Myeonghun Park [arXiv:0910.1584v2 [hep-ph]]
// Compute MCTPerp (perpendicular contransverse mass)
// Note that Et**2 = Pt**2 + m**2 (not mT**2 !!!)
double PhysicsTools::getMCTPerp(TLorentzVector& v1, TLorentzVector& v2, TLorentzVector& u) 
{
  // Access the 3-D vectors
  TVector3 v13D = v1.Vect();
  TVector3 v23D = v2.Vect();
  TVector3 u3D  = u.Vect();
  u3D.SetZ(0);
  u3D = u3D.Unit();

  // Calculate p[1,2]Perp
  TVector3 p1Perp = u3D.Cross(v13D.Cross(u3D));
  TVector3 p2Perp = u3D.Cross(v23D.Cross(u3D));

  double ET1Perp  = sqrt(p1Perp.Perp2() + v1.M2());
  double ET2Perp  = sqrt(p2Perp.Perp2() + v2.M2());

  double mCTSQ = pow(ET1Perp + ET2Perp,2) - (p1Perp-p2Perp).Perp2();

  return ((mCTSQ > 0.) ? sqrt(mCTSQ) : 0.);
}

// DON'T USE THIS FUNCTION YET, STILL UNDER SCRUNITY !!!!!!!!!!!!!!!!!!!!!!!
// Konstantin T. Matchev and Myeonghun Park [arXiv:0910.1584v2 [hep-ph]]
// Compute MCTPara (perpendicular contransverse mass)
// Note that Et**2 = Pt**2 + m**2 (not mT**2 !!!)
double PhysicsTools::getMCTPara(TLorentzVector& v1, TLorentzVector& v2, TLorentzVector& u) 
{
  // Access the 3-D vectors
  TVector3 v13D = v1.Vect();
  TVector3 v23D = v2.Vect();
  TVector3 u3D  = u.Vect();
  u3D.SetZ(0);
  u3D = u3D.Unit();

  // Calculate p[1,2]Para
  TVector3 p1Para = v13D.Dot(u3D)*u3D;
  TVector3 p2Para = v23D.Dot(u3D)*u3D;

  double ET1Para  = sqrt(p1Para.Perp2() + v1.M2());
  double ET2Para  = sqrt(p2Para.Perp2() + v2.M2());

  double mCTSQ = pow(ET1Para + ET2Para,2) - (p1Para-p2Para).Perp2();

  return ((mCTSQ > 0.) ? sqrt(mCTSQ) : 0.);
}

// Lorentz contralinear boost invariant 4-dot product
double PhysicsTools::contralinearDot(TLorentzVector& v1, TLorentzVector& v2)
{
  return ( v1.E()*v2.E()   +
           v1.Px()*v2.Px() +
           v1.Py()*v2.Py() +
           v1.Pz()*v2.Pz() );
}

/*--------------------------------------------------------------------------------*/
// Adapted from SusyNt
void PhysicsTools::superRazor( TLorentzVector l0,
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
                               )
{
// MDR CALCULATION 
//
// Code written by Christopher Rogan <crogan@cern.ch>, 04-23-13
// Details given in paper (http://arxiv.org/abs/1310.4827) written by 
// Matthew R. Buckley, Joseph D. Lykken, Christopher Rogan, Maria Spiropulu
//

  //
  // Lab frame
  //
  //Longitudinal boost
  TVector3 vBETA_z = (1./(l0.E()+l1.E()))*(l0+l1).Vect(); 
  vBETA_z.SetX(0.0);         
  vBETA_z.SetY(0.0);
  
  l0.Boost(-vBETA_z);
  l1.Boost(-vBETA_z);

  //pT of CM frame
  TVector3 pT_CM = (l0+l1).Vect() + met.Vect();
  pT_CM.SetZ(0.0);     
  
  TLorentzVector ll = l0+l1;
  //invariant mass of the total event
  double SHATR = sqrt( 2.*(ll.E()*ll.E() - ll.Vect().Dot(pT_CM) 
		   + ll.E()*sqrt( ll.E()*ll.E() + pT_CM.Mag2() - 2.*ll.Vect().Dot(pT_CM) )));
  
  TVector3 vBETA_T_CMtoR = (1./sqrt(pT_CM.Mag2() + SHATR*SHATR))*pT_CM;
  
  l0.Boost(-vBETA_T_CMtoR);
  l1.Boost(-vBETA_T_CMtoR);
  ll.Boost(-vBETA_T_CMtoR);  

  //
  //R-frame
  //
  dphi_LL_vBETA_T = fabs((ll.Vect()).DeltaPhi(vBETA_T_CMtoR));
  
  //double dphi_L1_L2 = fabs(l0.Vect().DeltaPhi(l1.Vect()));
  
  TVector3 vBETA_R = (1./(l0.E()+l1.E()))*(l0.Vect() - l1.Vect());
  
  //double gamma_R = 1./sqrt(1.-vBETA_R.Mag2());
  
  //double dphi_vBETA_R_vBETA_T = fabs(vBETA_R.DeltaPhi(vBETA_T_CMtoR));
  
  l0.Boost(-vBETA_R);
  l1.Boost(vBETA_R);
 
  //
  //R+1 frame
  //
  MDELTAR = 2.*l0.E();
  //double costhetaRp1 = l0.Vect().Dot(vBETA_R)/(l0.Vect().Mag()*vBETA_R.Mag());

  return;
}

// Overlap removal
void PhysicsTools::l_j_overlap ( std::vector<const xAOD::TruthParticle*>& leptons,
                                 std::vector<const xAOD::Jet*>& jets,
                                  double dRmin, bool removeJets )
{
  if(leptons.size() == 0 || jets.size() == 0) return;

  const unsigned int DEBUG = 0;

  if(DEBUG > 2) std::cout << std::endl; 

  // Lepton loop
  for(int iLep = leptons.size()-1; iLep >=0; --iLep) {
    TLorentzVector lep = leptons.at(iLep)->p4();

    if(DEBUG > 2) 
      std::cout << "PhysicsTools::l_j_overlap iLep " << iLep 
                << " pT " << lep.Pt() << " eta " << lep.Eta() << " phi " << lep.Phi() 
                << " removeJets " << removeJets << std::endl;

    // Jet loop
    for(int iJet = jets.size()-1; iJet >=0; --iJet) {
      TLorentzVector jet = jets.at(iJet)->p4();

      if(DEBUG > 2) 
        std::cout << "PhysicsTools::l_j_overlap iJet " << iJet 
                  << " pT " << jet.Pt() << " eta " << jet.Eta() << " phi " << jet.Phi() 
                  << " deltaR " << lep.DeltaR(jet) << std::endl;

      if( lep.DeltaR(jet) > dRmin) continue;

      if(removeJets) {
        jets.erase(jets.begin()+iJet);
      }
      else {
        leptons.erase(leptons.begin()+iLep);
        break;
      }

    } // end of loop over jets

  } // end of loop over leptons

  if(DEBUG > 2) std::cout << std::endl; 
}
