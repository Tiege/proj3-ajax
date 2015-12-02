#### Project 3 - Ajax Brevet Control Calculator #####
######### TREVOR JONES CS399se #########

#Note: For a good test of calculation times use 12/12/2012 12:00 200 km as calculator parameters

#This project is a simple web server ajax application which calculates a series of control points from a distance bike route and reflects the opening and closing times available for each control point. The times are based on the distance between each point and an algorithm taken from the model algorithm at the www.rusa.gov site.

#############################
# Calculations are based on total distance traveled divided by an average speed that is represented in the following table to calculate the time table for each control point.
######################################
#Distance#####Max speed####Min speed#
#   0-200            34            15
# 200-400            32            15
# 400-600            30            15
#600-1000            28          11.4
#   1000+            26          13.3
######################################

#Any given distance given for a control point cannot exceed 10% more than the total distance of the brevet (this is not implimented but implied :))
