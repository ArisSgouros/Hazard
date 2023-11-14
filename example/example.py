import sys
import os
import numpy as np
from itertools import islice

# import the path of the hazard module
sys.path.append('../')
from hazard import CumulativeHazard, FilterDuplicateEvent

if __name__ == "__main__":
   #
   # example from NIST [https://www.itl.nist.gov/div898/handbook/apr/section2/apr222.htm]
   print("example NIST (censored):")
   event_list_in = np.array([50, 37, 73, 100, 132, 195, 200, 248, 222, 250])
   status_list_in = np.array([0, 1, 1, 0, 1, 1, 0, 1, 1, 0])

   print("   compute censored cumulative hazard")
   # event_list is the same with event_list_in because the latter is sorted
   event_list, cumul_hazard = CumulativeHazard(event_list_in, status_list_in)

   print("   export cumulative hazard to o.log_nist_censor")
   with open("o.log_nist_censor", "w") as goo:
      goo.write("%-10s %-10s %-10s\n" % ("A/A", "time", "cumul.haz"))
      for ii in range(len(event_list)):
         goo.write("%-10d %-10.4f %-10.4f\n" % (ii+1, event_list[ii], cumul_hazard[ii]))

   print("example NIST (uncensored):")
   print("   compute uncensored cumulative hazard (status = 1)")
   status_list_in = np.full(len(event_list_in), 1)
   event_list, cumul_hazard = CumulativeHazard(event_list_in, status_list_in)
   print("   export cumulative hazard to o.log_nist_uncensor")
   with open("o.log_nist_uncensor", "w") as goo:
      goo.write("%-10s %-10s %-10s\n" % ("A/A", "time", "cumul.haz"))
      for ii in range(len(event_list)):
         goo.write("%-10d %-10.4f %-10.4f\n" % (ii+1, event_list[ii], cumul_hazard[ii]))

   #
   # example from input distribution
   print("example distribution from file in.dexp")
   event_list_in = []
   status_list_in = []

   with open('in.dexp') as foo:
      lines=foo.readlines()
   for line in lines:
      event_list_in.append(float(line.split()[0]))
      status_list_in.append(int(line.split()[1]))
   event_list_in = np.array(event_list_in)
   status_list_in = np.array(status_list_in)

   print("   compute cumulative hazard (with censoring)")
   event_list, cumul_hazard = CumulativeHazard(event_list_in, status_list_in)

   print("   export cumulative hazard to o.log_dexp")
   with open("o.log_dexp", "w") as goo:
      goo.write("%-10s %-10s %-10s\n" % ("A/A", "event_sort", "cumul.haz"))
      for ii in range(len(event_list)):
         goo.write("%-10d %-10.4f %-10.4f\n" % (ii+1, event_list[ii], cumul_hazard[ii]))

   print("   filter duplicate events")
   event_list, cumul_hazard = FilterDuplicateEvent(event_list, cumul_hazard)

   print("   export cumulative hazard to o.log_dexp_no_dupl")
   with open("o.log_dexp_no_dupl", "w") as goo:
      goo.write("%-10s %-10s %-10s\n" % ("A/A", "event_sort", "cumul.haz"))
      for ii in range(len(event_list)):
         goo.write("%-10d %-10.4f %-10.4f\n" % (ii+1, event_list[ii], cumul_hazard[ii]))
