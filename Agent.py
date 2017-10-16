# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
# , ImageChops, ImageFilter, ImageStat, ImageMorph
import numpy as np
# import math, operator, functools
import sys


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

        # The primary method for solving incoming Raven's Progressive Matrices.
        # For each problem, your Agent's Solve() method will be called. At the
        # conclusion of Solve(), your Agent should return an int representing its
        # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
        # are also the Names of the individual RavensFigures, obtained through
        # RavensFigure.getName(). Return a negative number to skip a problem.
        #
        # Make sure to return your answer *as an integer* at the end of Solve().
        # Returning your answer as a string may cause your program to crash.

    def pixelChange(self, x):
        if x < 128:
            return 0
        else:
            return 255

    def noDarkPixels(self, figure):
        nfigure = np.array(figure)
        pC = np.vectorize(self.pixelChange)
        nfigure = pC(nfigure)

        # unique, counts = np.unique(nfigure, return_counts=True)
        # print(dict(zip(unique, counts)))
        noBlackA = np.count_nonzero(nfigure == 0)
        # print(noBlackA)
        return noBlackA

    def noIntersectionPixels(self, figure1, figure2):
        count = 0
        nfigure1 = np.array(figure1)
        nfigure2 = np.array(figure2)
        # print(nfigure1.shape[0])
        for x in range(0, nfigure1.shape[0]):
            for y in range(0, nfigure1.shape[1]):
                if nfigure1[x, y] == 0 and nfigure1[x, y] == nfigure2[x, y]:
                    count = count + 1

        return count

    def Solve(self, problem):
        # for figureName in problem.figures:
        if problem.problemType == '2x2':
            figureA = problem.figures['A']
            figureB = problem.figures['B']
            figureC = problem.figures['C']

            figureImageA = Image.open(figureA.visualFilename).convert('L')
            figureImageB = Image.open(figureB.visualFilename).convert('L')
            figureImageC = Image.open(figureC.visualFilename).convert('L')

            noDarkPixelsA = self.noDarkPixels(figureImageA)
            noDarkPixelsB = self.noDarkPixels(figureImageB)
            noDarkPixelsC = self.noDarkPixels(figureImageC)

            noDarkPixelsAB = noDarkPixelsB / noDarkPixelsA
            noDarkPixelsAC = noDarkPixelsC / noDarkPixelsA

            noIntersectionPixelsAB = self.noIntersectionPixels(figureImageA, figureImageB)/(noDarkPixelsA+noDarkPixelsB)
            noIntersectionPixelsAC = self.noIntersectionPixels(figureImageA, figureImageC)/(noDarkPixelsA+noDarkPixelsC)

            noDarkPixelsBOption = []
            noDarkPixelsCOption = []

            noIntersectionPixelsBOption = []
            noIntersectionPixelsCOption = []

            darkPixelsRatioAB = []
            intersectionRatioAB = []
            darkPixelDiffAB = []
            intersectionDiffAB = []

            darkPixelsRatioAC = []
            intersectionRatioAC = []
            darkPixelDiffAC = []
            intersectionDiffAC = []
            # print("\n")
            # print("Problem")
            # print("A: " + str(noDarkPixelsA) + " B: " + str(noDarkPixelsB) + " C:" + str(noDarkPixelsC))
            # print("\n")
            for i in range(1, 7):
                figure = problem.figures[str(i)]
                figureImage = Image.open(figure.visualFilename).convert('L')

                noDarkPixels = self.noDarkPixels(figureImage)
                # print(str(i)+ " noDarkPixels="+str(noDarkPixels))

                noDarkPixelsBOption.append(noDarkPixels / noDarkPixelsB)
                noDarkPixelsCOption.append(noDarkPixels / noDarkPixelsC)

                noIntersectionPixelsBOption.append(self.noIntersectionPixels(figureImageB, figureImage)/(noDarkPixelsB+noDarkPixels))
                noIntersectionPixelsCOption.append(self.noIntersectionPixels(figureImageC, figureImage)/(noDarkPixelsC+noDarkPixels))

                # print("Option " + str(i))
                # print("noDarkPixelsAB="+str(noDarkPixelsAB))
                # print("noDarkPixelsCOption "+str(i)+" "+str(noDarkPixelsCOption[i-1]))
                # print("\n")
                if noDarkPixelsAB != 0:
                    # print("darkPixelsDiffRatioCOption/AB " + str((noDarkPixelsCOption[i - 1] - noDarkPixelsAB)/noDarkPixelsAB))
                    darkPixelsRatioAB.append(
                        tuple([abs((noDarkPixelsCOption[i - 1] - noDarkPixelsAB) / noDarkPixelsAB), i]))
                else:
                    # print("darkPixelsDiffRatioCOption - AB " + str(noDarkPixelsCOption[i - 1] - noDarkPixelsAB))
                    darkPixelDiffAB.append(tuple([noDarkPixelsCOption[i - 1] - noDarkPixelsAB, i]))
                # print("")

                # print("interAB "+ str(noIntersectionPixelsAB))
                # print("inter " + str(i) + " " + str(noIntersectionPixelsCOption[i-1]))
                # print("\n")
                if noIntersectionPixelsAB != 0:
                    # print("intersectionPixelsDiffRatioCOption/AB "+ str((noIntersectionPixelsCOption[i-1] - noIntersectionPixelsAB)/noIntersectionPixelsAB))
                    intersectionRatioAB.append(tuple([abs((noIntersectionPixelsCOption[i - 1] - noIntersectionPixelsAB) / noIntersectionPixelsAB),
                         i]))
                else:
                    # print("intersectionPixelsDiffRatioCOption - AB " + str(noIntersectionPixelsCOption[i - 1] - noIntersectionPixelsAB))
                    intersectionDiffAB.append(tuple([noIntersectionPixelsCOption[i - 1] - noIntersectionPixelsAB, i]))
                # print("\n")
                # print("noDarkPixelsAC=" + str(noDarkPixelsAC))
                # print("noDarkPixelsBOption" + str(i) + " " + str(noDarkPixelsBOption[i - 1]))
                # print("")
                if noDarkPixelsAC != 0:
                    # print("darkPixelsDiffRatioBOption/AC " + str((noDarkPixelsBOption[i - 1]-noDarkPixelsAC)/noDarkPixelsAC))
                    darkPixelsRatioAC.append(
                        tuple([abs((noDarkPixelsBOption[i - 1] - noDarkPixelsAC) / noDarkPixelsAC), i]))
                else:
                    # print("darkPixelsDiffRatioBOption - AC " + str(noDarkPixelsBOption[i - 1] - noDarkPixelsAC))
                    darkPixelDiffAC.append(tuple([abs(noDarkPixelsBOption[i - 1] - noDarkPixelsAC), i]))
                # print("")
                # print("interAC " + str(noIntersectionPixelsAC))
                # print("inter " + str(i) + " " + str(noIntersectionPixelsBOption[i - 1]))
                # print("\n")
                if noIntersectionPixelsAC != 0:
                    # print("intersectionPixelsDiffRatioBOption/AC " + str((noIntersectionPixelsBOption[i - 1]-noIntersectionPixelsAC)/noIntersectionPixelsAC))
                    intersectionRatioAC.append(tuple(
                        [abs((noIntersectionPixelsBOption[i - 1] - noIntersectionPixelsAC) / noIntersectionPixelsAC),
                         i]))
                else:
                    # print("intersectionPixelsDiffRatioBOption - AC " + str(noIntersectionPixelsBOption[i - 1] - noIntersectionPixelsAC))
                    intersectionDiffAC.append(tuple([noIntersectionPixelsBOption[i - 1] - noIntersectionPixelsAC, i]))
                    # print("\n")
                    # if noDarkPixelsAB==noDarkPixelsCOption[i-1] and noIntersectionPixelsAB==noIntersectionPixelsCOption[i-1]:
                    #     return i

            # for i in range(0, len(darkPixelsRatioAB)):
            #     print("DP: "+ str(darkPixelsRatioAB[i][0]))
            # print(sys.version)
            darkPixelsRatioAB.sort()
            darkPixelDiffAB.sort()
            intersectionRatioAB.sort()
            intersectionDiffAB.sort()

            # print("\n")
            # print("DarkPixelRatioAB/COption: ")
            # for i in range(0, len(darkPixelsRatioAB)):
            #     print(darkPixelsRatioAB[i])
            # print("DarkPixelDiffAB/COption: ")
            # for i in range(0, len(darkPixelDiffAB)):
            #     print(darkPixelDiffAB[i])
            #
            # print("\n")
            # print("IntersectionRatioAB/COption: ")
            # for i in range(0, len(intersectionRatioAB)):
            #     print(intersectionRatioAB[i])
            # print("IntersectionDiffAB/COption:")
            # for i in range(0, len(intersectionDiffAB)):
            #     print(intersectionDiffAB[i])

            darkPixelsRatioAC.sort()
            darkPixelDiffAC.sort()
            intersectionRatioAC.sort()
            intersectionDiffAC.sort()
            # print("\n")
            # print("DarkPixelRatioAC/BOption: ")
            # for i in range(0, len(darkPixelsRatioAC)):
            #     print(darkPixelsRatioAC[i])
            # print("DarkPixelDiffAC/BOption: ")
            #
            # for i in range(0, len(darkPixelDiffAC)):
            #     print(darkPixelDiffAC[i])
            # print("\n")
            #
            # print("IntersectionRatioAC/BOption: ")
            # for i in range(0, len(intersectionRatioAC)):
            #     print(intersectionRatioAC[i])
            # print("IntersectionDiffAC/BOption:")
            # for i in range(0, len(intersectionDiffAC)):
            #     print(intersectionDiffAC[i])

            dMin = None
            dMax = None
            darkPixelsRatioAB1 = []
            for i in range(0, len(darkPixelsRatioAB)):
                if dMax == None:
                    dMax = darkPixelsRatioAB[i][0]
                elif darkPixelsRatioAB[i][0] > dMax:
                    dMax = darkPixelsRatioAB[i][0]
                if dMin == None:
                    dMin = darkPixelsRatioAB[i][0]
                elif darkPixelsRatioAB[i][0] < dMin:
                    dMin = darkPixelsRatioAB[i][0]

            darkPixelsRatioAC1 = []

            for i in range(0, len(darkPixelsRatioAC)):
                if dMax == None:
                    dMax = darkPixelsRatioAC[i][0]
                elif darkPixelsRatioAC[i][0] > dMax:
                    dMax = darkPixelsRatioAC[i][0]
                if dMin == None:
                    dMin = darkPixelsRatioAC[i][0]
                elif darkPixelsRatioAC[i][0] < dMin:
                    dMin = darkPixelsRatioAC[i][0]
            # print(str(dMin) + " " + str(dMax) + "\n")
            for i in range(0, len(darkPixelsRatioAB)):
                darkPixelsRatioAB1.append(
                    tuple([(darkPixelsRatioAB[i][0] - dMin) / (dMax - dMin), darkPixelsRatioAB[i][1]]))
            # print("Normal")
            # for i in range(0, len(darkPixelsRatioAB1)):
            #     print(darkPixelsRatioAB1[i])

            for i in range(0, len(darkPixelsRatioAC)):
                darkPixelsRatioAC1.append(
                    tuple([(darkPixelsRatioAC[i][0] - dMin) / (dMax - dMin), darkPixelsRatioAC[i][1]]))

            # print("Normal")
            # for i in range(0, len(darkPixelsRatioAC1)):
            #     print(darkPixelsRatioAC1[i])

            dMin = None
            dMax = None
            intersectionRatioAB1 = []
            for i in range(0, len(intersectionRatioAB)):
                if dMax == None:
                    dMax = intersectionRatioAB[i][0]
                elif intersectionRatioAB[i][0] > dMax:
                    dMax = intersectionRatioAB[i][0]
                if dMin == None:
                    dMin = intersectionRatioAB[i][0]
                elif intersectionRatioAB[i][0] < dMin:
                    dMin = intersectionRatioAB[i][0]

            intersectionRatioAC1 = []
            for i in range(0, len(intersectionRatioAC)):
                if dMax == None:
                    dMax = intersectionRatioAC[i][0]
                elif intersectionRatioAC[i][0] > dMax:
                    dMax = intersectionRatioAC[i][0]
                if dMin == None:
                    dMin = intersectionRatioAC[i][0]
                elif intersectionRatioAC[i][0] < dMin:
                    dMin = intersectionRatioAC[i][0]
            # print(str(dMin) + " " + str(dMax) + "\n")

            for i in range(0, len(intersectionRatioAB)):
                intersectionRatioAB1.append(
                    tuple([(intersectionRatioAB[i][0] - dMin) / (dMax - dMin), intersectionRatioAB[i][1]]))
            # print(str(dMin) + " " + str(dMax))

            # print("Normal")
            # for i in range(0, len(intersectionRatioAB1)):
            #     print(intersectionRatioAB1[i])

            for i in range(0, len(intersectionRatioAC)):
                intersectionRatioAC1.append(
                    tuple([(intersectionRatioAC[i][0] - dMin) / (dMax - dMin), intersectionRatioAC[i][1]]))

            # print("Normal")
            # for i in range(0, len(intersectionRatioAC1)):
            #     print(intersectionRatioAC1[i])

            weightsAB = []
            weightsInterAB = []
            max = 0
            maxIndex = -1
            sumAB = 0.0
            for i in range(0, len(darkPixelsRatioAB1)):
                weightsAB.append(
                    tuple([(1 / (1 + darkPixelsRatioAB1[i][0])) * (1 / (1 + i)), darkPixelsRatioAB1[i][1]]))
                # print(weightsAB[i])
            for i in range(0, len(intersectionRatioAB)):
                weightsInterAB.append(
                    tuple([(1 / (1 + intersectionRatioAB1[i][0])) * (1 / (1 + i)), intersectionRatioAB1[i][1]]))
                # print(weightsInterAB[i])
            for i in range(0, len(weightsInterAB)):
                sumAB = weightsInterAB[i][0]
                for j in range(0, len(weightsAB)):
                    if weightsAB[j][1] == weightsInterAB[i][1]:
                        sumAB = sumAB + weightsAB[j][0]
                        # print("SumAB= " + str(weightsAB[j][1]) + " " + str(sumAB))
                        if sumAB > max:
                            max = sumAB
                            maxIndex = weightsAB[j][1]

            weightsAC = []
            weightsInterAC = []
            for i in range(0, len(darkPixelsRatioAC)):
                weightsAC.append(
                    tuple([(1 / (1 + darkPixelsRatioAC1[i][0])) * (1 / (1 + i)), darkPixelsRatioAC1[i][1]]))
                # print(weightsAC[i])
            for i in range(0, len(intersectionRatioAC)):
                weightsInterAC.append(
                    tuple([(1 / (1 + intersectionRatioAC1[i][0])) * (1 / (1 + i)), intersectionRatioAC1[i][1]]))
                # print(weightsInterAC[i])
            for i in range(0, len(weightsInterAC)):
                sumAB = weightsInterAC[i][0]
                for j in range(0, len(weightsAC)):
                    if weightsAC[j][1] == weightsInterAC[i][1]:
                        sumAB = sumAB + weightsAC[j][0]
                        # print("SumAB= " + str(weightsAC[j][1]) + " " + str(sumAB))
                        if sumAB > max:
                            max = sumAB
                            maxIndex = weightsAC[j][1]

            return maxIndex
        return -1

