#!/usr/bin/env python

# import some modules
import sys, os
# add MG5_aMC into the path and import the lhe_parser
sys.path.append("/users/wuxingyu/MG5_aMC_v2_9_2/")
from madgraph.various.lhe_parser import *
# import ROOT, creat an alias
import ROOT as R
# import array to save the address in class Branch
from array import array

def TMVAApply(InputFile, Polarization):

  # load data in the ROOT file
  data = InputFile.Get("{Polarization}Tree".format(Polarization = Polarization))

  # Create a set of variables and declare them to the reader
  # the variable names MUST corresponds in name and type to those given in the weight file(s) used
  M1 = array("f", [0])
  M2 = array("f", [0])
  M4l = array("f", [0])
  CosTheta1 = array("f", [0])
  CosTheta2 = array("f", [0])
  Theta1 = array("f", [0])
  Theta2 = array("f", [0])
  ThetaStar1 = array("f", [0])
  ThetaStar2 = array("f", [0])
  CosThetaStar1 = array("f", [0])
  CosThetaStar2 = array("f", [0])
  Phi = array("f", [0])
  Phi1 = array("f", [0])
  CosPhi = array("f", [0])
  CosPhi1 = array("f", [0])
  Eta1 = array("f", [0])
  Eta2 = array("f", [0])
  Eta4l = array("f", [0])
  Pt1 = array("f", [0])
  Pt2 = array("f", [0])
  Pt4l = array("f", [0])
  deltaR1 = array("f", [0])
  deltaR2 = array("f", [0])
  MindeltaR = array("f", [0])
  Y1 = array("f", [0])
  Y2 = array("f", [0])
  deltaY = array("f", [0])

  # Prepare the event tree
  # Here the variable names have to corresponds to the tree
  data.SetBranchAddress("M1", M1)
  data.SetBranchAddress("M2", M2)
  data.SetBranchAddress("M4l", M4l)
  data.SetBranchAddress("CosTheta1", CosTheta1)
  data.SetBranchAddress("CosTheta2", CosTheta2)
  data.SetBranchAddress("Theta1", Theta1)
  data.SetBranchAddress("Theta2", Theta2)
  data.SetBranchAddress("ThetaStar1", ThetaStar1)
  data.SetBranchAddress("ThetaStar2", ThetaStar2)
  data.SetBranchAddress("CosThetaStar1", CosThetaStar1)
  data.SetBranchAddress("CosThetaStar2", CosThetaStar2)
  data.SetBranchAddress("Phi", Phi)
  data.SetBranchAddress("Phi1", Phi1)
  data.SetBranchAddress("CosPhi", CosPhi)
  data.SetBranchAddress("CosPhi1", CosPhi1)
  data.SetBranchAddress("Eta1", Eta1)
  data.SetBranchAddress("Eta2", Eta2)
  data.SetBranchAddress("Eta4l", Eta4l)
  data.SetBranchAddress("Pt1", Pt1)
  data.SetBranchAddress("Pt2", Pt2)
  data.SetBranchAddress("Pt4l", Pt4l)
  data.SetBranchAddress("deltaR1", deltaR1)
  data.SetBranchAddress("deltaR2", deltaR2)
  data.SetBranchAddress("MindeltaR", MindeltaR)
  data.SetBranchAddress("Y1", Y1)
  data.SetBranchAddress("Y2", Y2)
  data.SetBranchAddress("deltaY", deltaY)

  # Create the Reader object
  reader = R.TMVA.Reader("!Color:!Silent")
  reader.AddVariable("M1", M1)
  reader.AddVariable("M2", M2)
  reader.AddVariable("M4l", M4l)
  reader.AddVariable("CosTheta1", CosTheta1)
  reader.AddVariable("CosTheta2", CosTheta2)
  reader.AddVariable("Theta1", Theta1)
  reader.AddVariable("Theta2", Theta2)
  reader.AddVariable("ThetaStar1", ThetaStar1)
  reader.AddVariable("ThetaStar2", ThetaStar2)
  reader.AddVariable("CosThetaStar1", CosThetaStar1)
  reader.AddVariable("CosThetaStar2", CosThetaStar2)
  reader.AddVariable("Phi", Phi)
  reader.AddVariable("Phi1", Phi1)
  reader.AddVariable("CosPhi", CosPhi)
  reader.AddVariable("CosPhi1", CosPhi1)
  reader.AddVariable("Eta1", Eta1)
  reader.AddVariable("Eta2", Eta2)
  reader.AddVariable("Eta4l", Eta4l)
  reader.AddVariable("Pt1", Pt1)
  reader.AddVariable("Pt2", Pt2)
  reader.AddVariable("Pt4l", Pt4l)
  reader.AddVariable("deltaR1", deltaR1)
  reader.AddVariable("deltaR2", deltaR2)
  reader.AddVariable("MindeltaR", MindeltaR)
  reader.AddVariable("Y1", Y1)
  reader.AddVariable("Y2", Y2)
  reader.AddVariable("deltaY", deltaY)
  
  # Book method
  # Make sure that the directory "dataset" is in the present working dircetory!!!
  reader.BookMVA("BDT Method", "dataset/weights/TMVAClassification_BDT.weights.xml")

  # Draw BDT distribution and save it in a ROOT file
  if Polarization == "Inclusive":
      h_InclusiveBDT = R.TH1F("InclusiveBDT", "InclusiveBDT", 40, -1, 1)
      for i in range(0, data.GetEntries()):
          data.GetEntry(i)
          h_InclusiveBDT.Fill(reader.EvaluateMVA("BDT Method"))
      tfout = R.TFile("InclusiveBDT.root", "RECREATE")
      tfout.cd()
      h_InclusiveBDT.Write()
  elif Polarization == "TT":
      h_TTBDT = R.TH1F("TTBDT", "TTBDT", 40, -1, 1)
      for i in range(0, data.GetEntries()):
          data.GetEntry(i)
          h_TTBDT.Fill(reader.EvaluateMVA("BDT Method"))
      tfout = R.TFile("TTBDT.root", "RECREATE")
      tfout.cd()
      h_TTBDT.Write()
  elif Polarization == "TL":
      h_TLBDT = R.TH1F("TLBDT", "TLBDT", 40, -1, 1)
      for i in range(0, data.GetEntries()):
          data.GetEntry(i)
          h_TLBDT.Fill(reader.EvaluateMVA("BDT Method"))
      tfout = R.TFile("TLBDT.root", "RECREATE")
      tfout.cd()
      h_TLBDT.Write()
  elif Polarization == "LL":
      h_LLBDT = R.TH1F("LLBDT", "LLBDT", 40, -1, 1)
      for i in range(0, data.GetEntries()):
          data.GetEntry(i)
          h_LLBDT.Fill(reader.EvaluateMVA("BDT Method"))
      tfout = R.TFile("LLBDT.root", "RECREATE")
      tfout.cd()
      h_LLBDT.Write()

  # Close the ROOT file
  tfout.Close()

  # Close the InputFile
  InputFile.Close()

if __name__ == "__main__":

  InputFile = R.TFile.Open("/users/wuxingyu/WorkingSpace/GraduationThesis/Data/InclusiveTree.root")
  TMVAApply(InputFile, "Inclusive")

  InputFile = R.TFile.Open("/users/wuxingyu/WorkingSpace/GraduationThesis/Data/TTTree.root")
  TMVAApply(InputFile, "TT")
  
  InputFile = R.TFile.Open("/users/wuxingyu/WorkingSpace/GraduationThesis/Data/TLTree.root")
  TMVAApply(InputFile, "TL")
  
  InputFile = R.TFile.Open("/users/wuxingyu/WorkingSpace/GraduationThesis/Data/LLTree.root")
  TMVAApply(InputFile, "LL")



