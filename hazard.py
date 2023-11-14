###############################################################################
# MIT License
#
# Copyright (c) 2023 ArisSgouros
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

import numpy as np

def CumulativeHazard(event_list_in, status_list_in):
   nevent = event_list_in.size
   if status_list_in.size == 0:
      status_list_in = np.full(nevent, 1)

   # sort arrays based on the event_list
   inds = event_list_in.argsort()
   event_list = event_list_in[inds]
   status_list = status_list_in[inds]

   cumul_hazard_censor = []
   event_list_censor = []
   cumul_hazard = 0.0
   for ii in range(nevent):
      cumul_hazard += status_list[ii]/(nevent - ii)
      if status_list[ii]:
         event_list_censor.append(event_list[ii])
         cumul_hazard_censor.append(cumul_hazard)

   return np.array(event_list_censor), np.array(cumul_hazard_censor)

def FilterDuplicateEvent(event_list_in, cumul_hazard_in):
   nevent = len(event_list_in)
   event_list_filter = []
   cumul_hazard_filter = []
   for ii in range(nevent-1):
      if event_list_in[ii] == event_list_in[ii + 1]:
         continue
      event_list_filter.append(event_list_in[ii])
      cumul_hazard_filter.append(cumul_hazard_in[ii])
   event_list_filter.append(event_list_in[nevent-1])
   cumul_hazard_filter.append(cumul_hazard_in[nevent-1])
   return np.array(event_list_filter), np.array(cumul_hazard_filter)
