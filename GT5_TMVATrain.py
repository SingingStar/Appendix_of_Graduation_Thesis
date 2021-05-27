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

# define a function named "TMVATrain"
def TMVATrain(InputFileSignal, InputFileBackground):


  ROOTFileSignal = R.TFile.Open(InputFileSignal)
  ROOTFileBackground = R.TFile.Open(InputFileBackground)


  Signal = ROOTFileSignal.Get("LLTree")
  Background = ROOTFileBackground.Get("TTTLTree")
  SignalWeight = 1
  BackgroundWeight = 1

  OutputFile = R.TFile("TMVATrain.root", "RECREATE")


  factory = R.TMVA.Factory("TMVAClassification", OutputFile, "!V:Color:DrawProgressBar:Transformations=I:AnalysisType=Classification")

  dataloader = R.TMVA.DataLoader("dataset")


  dataloader.AddSignalTree(Signal, SignalWeight)
  dataloader.AddBackgroundTree(Background, BackgroundWeight)

  dataloader.AddVariable("M1", "F")
  dataloader.AddVariable("M2", "F")
  dataloader.AddVariable("M4l", "F")
  dataloader.AddVariable("CosTheta1", "F")
  dataloader.AddVariable("CosTheta2", "F")
  dataloader.AddVariable("Theta1", "F")
  dataloader.AddVariable("Theta2", "F")
  dataloader.AddVariable("ThetaStar1", "F")
  dataloader.AddVariable("ThetaStar2", "F")
  dataloader.AddVariable("CosThetaStar1","F")
  dataloader.AddVariable("CosThetaStar2","F")
  dataloader.AddVariable("Phi", "F")
  dataloader.AddVariable("Phi1", "F")
  dataloader.AddVariable("CosPhi", "F")
  dataloader.AddVariable("CosPhi1", "F")
  dataloader.AddVariable("Eta1", "F")
  dataloader.AddVariable("Eta2", "F")
  dataloader.AddVariable("Eta4l", "F")
  dataloader.AddVariable("Pt1", "F")
  dataloader.AddVariable("Pt2", "F")
  dataloader.AddVariable("Pt4l", "F")
  dataloader.AddVariable("deltaR1", "F")
  dataloader.AddVariable("deltaR2", "F")
  dataloader.AddVariable("MindeltaR", "F")
  dataloader.AddVariable("Y1", "F")
  dataloader.AddVariable("Y2", "F")
  dataloader.AddVariable("deltaY", "F")

  mycut = R.TCut("")
  dataloader.PrepareTrainingAndTestTree(mycut, "SplitMode=Random")

  factory.BookMethod(dataloader, R.TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=400:MinNodeSize=4%:MaxDepth=5:BoostType=AdaBoost:AdaBoostBeta=0.15:nCuts=80")

  factory.TrainAllMethods()
  factory.TestAllMethods()
  factory.EvaluateAllMethods()

  OutputFile.Close()

  R.TMVA.TMVAGui("TMVATrain.root")



if __name__ == "__main__":

  InputFileSignal = "/users/wuxingyu/WorkingSpace/GraduationThesis/Data/LLTree.root"
  InputFileBackground = "/users/wuxingyu/WorkingSpace/GraduationThesis/Data/TTTLTree.root"

  TMVATrain(InputFileSignal=InputFileSignal, InputFileBackground=InputFileBackground)
