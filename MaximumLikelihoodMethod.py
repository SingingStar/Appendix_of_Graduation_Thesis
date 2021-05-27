#!/usr/bin/env python

# import some modules
import sys, os, math
# import ROOT, creat an alias
import ROOT as R

##################################################################
##                                                              ##
##            MaximumLikelihoodMethod Manual                    ## 
## Author: Xingyu Wu                                            ##
## From JiLin University                                        ##
## 2021.4.25                                                    ##
##                                                              ##
## (1) KinematicName example:"CosTheta1", "Pt1", "BDT"          ##
## (2) The example of input is at the last of this script.      ##
## (3) The name of histogram in ROOTFile has its format:        ##
##     Inclusive{KinematicsName}                                ##
##     TT{KinematicsName}                                       ##
##     TL{KinematicsName}                                       ##
##     LL{KinematicsName}                                       ##
##                                                              ##
##################################################################

# Reference
# http://www.physics.utah.edu/~detar/phys6720/handouts/curve_fit/curve_fit/node2.html
# http://www.physics.utah.edu/~detar/phys6720/handouts/curve_fit/curve_fit/node1.html
# how to deduce the mu is recorded in the 2021_4_14_MeetingPresentation
# and the mu error can be calculated by second order derivative of X2


def MaximumLikelihoodMethod(KinematicsName, InputROOTFile_Inclusive, InputROOTFile_TT, InputROOTFile_TL, InputROOTFile_LL):

  # Load each input ROOT file and open them
  ROOTFile_Inclusive = R.TFile.Open(InputROOTFile_Inclusive)
  ROOTFile_TT = R.TFile.Open(InputROOTFile_TT)
  ROOTFile_TL = R.TFile.Open(InputROOTFile_TL)
  ROOTFile_LL = R.TFile.Open(InputROOTFile_LL)

  # Get histograms in each ROOT file
  h_Inclusive = ROOTFile_Inclusive.Get("Inclusive{KinematicsName}".format(KinematicsName = KinematicsName))
  h_TT = ROOTFile_TT.Get("TT{KinematicsName}".format(KinematicsName = KinematicsName))
  h_TL = ROOTFile_TL.Get("TL{KinematicsName}".format(KinematicsName = KinematicsName))
  h_LL = ROOTFile_LL.Get("LL{KinematicsName}".format(KinematicsName = KinematicsName))

  # Get the entries of the 1st histogram, use it for scaling
  Entries = h_Inclusive.GetEntries()
  
  # scale all the histograms to yield
  h_Inclusive.Scale(0.02419*139*1000/Entries)
  h_TT.Scale(0.01688*139*1000/Entries)
  h_TL.Scale(0.005741*139*1000/Entries)
  h_LL.Scale(0.001406*139*1000/Entries)

  # Get the number of bins
  nbins = h_Inclusive.GetNbinsX()

  # since some Kinematics have underflow and overflow, add them to the 1st bin and last bin.
  h_Inclusive.SetBinContent(1, h_Inclusive.GetBinContent(0)+h_Inclusive.GetBinContent(1))
  h_Inclusive.SetBinContent(nbins, h_Inclusive.GetBinContent(nbins)+h_Inclusive.GetBinContent(nbins+1))
  h_TT.SetBinContent(1, h_TT.GetBinContent(0)+h_TT.GetBinContent(1))
  h_TT.SetBinContent(nbins, h_TT.GetBinContent(nbins)+h_TT.GetBinContent(nbins+1))
  h_TL.SetBinContent(1, h_TL.GetBinContent(0)+h_TL.GetBinContent(1))
  h_TL.SetBinContent(nbins, h_TL.GetBinContent(nbins)+h_TL.GetBinContent(nbins+1))
  h_LL.SetBinContent(1, h_LL.GetBinContent(0)+h_LL.GetBinContent(1))
  h_LL.SetBinContent(nbins, h_LL.GetBinContent(nbins)+h_LL.GetBinContent(nbins+1))

  # define some initial values
  a1, a2, a3 = 0, 0, 0
  N_TT, N_TL, N_LL, N_Inclusive = 0, 0, 0, 0
  sigmai, sigmai2 = 0, 0
  mu, significance = 0, 0

  sigmaLLi, sigmaLLi2 = 0, 0
  b1, b2, b3 = 0, 0, 0
  sigma, sigma1 = 0, 0

  f_LL = 0
  NSum_LL, NSum_Inclusive = 0, 0
  for i in range(1, 41):
      """
      Calculate mu
      """
      N_TT = h_TT.GetBinContent(i)
      N_TL = h_TL.GetBinContent(i)
      N_LL = h_LL.GetBinContent(i)
      N_Inclusive = h_Inclusive.GetBinContent(i)
      NSum_LL += N_LL
      NSum_Inclusive += N_Inclusive
      # Using the error of Asimov data
      sigmai = R.TMath.Sqrt(N_Inclusive)
      sigmai2 = sigmai*sigmai

      # sigmai2 is the denominator, so it can't be 0, calculate independently when sigmai2 is 0.
      # if BinContent is 0, it can cause sigmai2 = 0
      if sigmai2 != 0:
          a1 += N_Inclusive*N_LL/sigmai2
          a2 += N_LL*(N_TT + N_TL)/sigmai2
          a3 += N_LL*N_LL/sigmai2
      elif sigmai2 == 0:
          a1 += 0
          a2 += 0
          a3 += 0

  for i in range(1, 41):
      """
      Calculate sigma
      """
      N_TT = h_TT.GetBinContent(i)
      N_TL = h_TL.GetBinContent(i)
      N_LL = h_LL.GetBinContent(i)
      N_Inclusive = h_Inclusive.GetBinContent(i)
      # Using the error of Asimov data
      sigmai = R.TMath.Sqrt(N_Inclusive)
      sigmai2 = sigmai*sigmai
      sigmaLLi = R.TMath.Sqrt(N_LL)
      sigmaLLi2 = sigmaLLi*sigmaLLi

      # sigmai2 is the denominator, so it can't be 0, calculate independently when sigmai2 is 0.
      # if BinContent is 0, it can cause sigmai2 = 0
      if sigmai2 != 0:
          b1 += (N_LL*N_LL)/(sigmai2*a3)
          b2 = ((((N_Inclusive-N_TT-N_TL)*a3)/sigmai2) - (2*N_LL*(N_Inclusive-N_TT-N_TL)*N_LL)/(sigmai2*sigmai2))/(a3*a3)
          b3 += b2*b2*sigmaLLi2
      elif sigmai2 == 0:
          b1 += 0
          b3 += 0


  # the equation of mu is deduced by MaximumLikelihoodMethod
  mu = (a1 - a2)/a3
  # the equation of sigma(the error of mu) is deduced by second order derivative of X2
  sigma1=R.TMath.Sqrt(a3)
  sigma = 1/sigma1
  # calculate the significance
  significance = mu/sigma
  # calculate the proportion of LL Event f_LL
  f_LL = mu*NSum_LL/NSum_Inclusive

  # create an output file to save the result of the mu, sigma and significance
  OutputFile = open("mu_from_{KinematicsName}.txt".format(KinematicsName = KinematicsName), "w")
  OutputFile.write("****************MaximumLikelihoodMethod****************"+"\n")
  OutputFile.write("{KinematicsName}".format(KinematicsName = KinematicsName)+"\n")
  OutputFile.write("EventNumber:"+str(Entries)+"\n")
  OutputFile.write("mu:"+str(mu)+"\n")
  OutputFile.write("sigma:"+str(sigma)+"\n")
  OutputFile.write("significance:"+str(significance)+"\n")
  OutputFile.write("f_LL:"+str(f_LL)+"\n")
  OutputFile.close()

  # also print the result of the mu, sigma and significance
  print("****************MaximumLikelihoodMethod****************")
  print("{KinematicsName}".format(KinematicsName = KinematicsName))
  print("EventNumber", Entries)
  print("mu", mu)
  print("sigma", sigma)
  print("significance", significance)
  print("f_LL", f_LL)


  
  
  # close the ROOTFile
  ROOTFile_Inclusive.Close()
  ROOTFile_TT.Close()
  ROOTFile_TL.Close()
  ROOTFile_LL.Close()

if __name__ == "__main__":

  InputROOTFile_Inclusive = "/users/wuxingyu/WorkingSpace/GraduationThesis/ROOTFile/KinematicQuantity_ssh_v2.root"
  InputROOTFile_TT = "/users/wuxingyu/WorkingSpace/GraduationThesis/ROOTFile/KinematicQuantity_ssh_v2.root"
  InputROOTFile_TL = "/users/wuxingyu/WorkingSpace/GraduationThesis/ROOTFile/KinematicQuantity_ssh_v2.root"
  InputROOTFile_LL = "/users/wuxingyu/WorkingSpace/GraduationThesis/ROOTFile/KinematicQuantity_ssh_v2.root"


  KinematicsName = "M1"
  MaximumLikelihoodMethod(KinematicsName, InputROOTFile_Inclusive, InputROOTFile_TT, InputROOTFile_TL, InputROOTFile_LL)


