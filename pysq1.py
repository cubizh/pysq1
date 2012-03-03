#		Copyright (c) 2012 António Gomes (cubizh at gmail dot com)
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


# Associating a letter and number to corners and edges respectively
# A-YGO;B-YRG;C-YRB;D-YBO;E-WGO;F-WRG;G-WRB;H-WBO
# 1-YG;2-YR;3-YB;4-YO;5-WG;6-WR;7-WB;8-WO
# * - Any value accepted



import copy

MAX_DEPTH = 6
# sq1state class. A square-1 state is defined by two strings
# u and d with 12 positions each, representing their state
# Other methods should be more or less self-explanatory
class sq1state:
	#Initialization : U and D are given by strings, which by default
	#                 are set to solved state
	def __init__(self,u='aa1bb2cc3dd4',d='ee5ff6gg7hh8'):
		self.u=u
		self.d=d
		# Define which are the valid (slicable) turns for this state
		self.fix_twists()
	
	#Output of the square-1. Only necessary (for shortness U and D):	
	def __repr__(self):
		return "U: %s - D: %s" %(self.u,self.d)
		
	def __str__(self):
		return "U: %s - D: %s" %(self.u,self.d)

	# Checking for equal states
	def __eq__(self,x):
		# Two states are equal if all of U and D match on both
		# '*' means anything goes, so it's not checked
		for i in range(12):
			if x.u[i]!='*':
				if self.u[i]!=x.u[i] or self.d[i]!=x.d[i]:
					return False
		return True

	#Copying a sq1 state from one class to another
	def copy(self):
		return sq1state(self.u,self.d)

	# Apply face turns to the square-1. Move is a tuple (A,B)
	def turn(self, move):
		if move in self.valid_twists:
			self.u=self.u[-move[0]:]+self.u[:-move[0]]
			self.d=self.d[move[1]:]+self.d[:move[1]]


	# For the given square-1 state, find all valid moves (except (0,0) )
	# and store them in the valid_twists list
	def fix_twists(self):
		if '*' in self.u or '*' in self.d:
			self.valid_twists=[]
		else:
			self.valid_twists = [(a,b) \
		          for a in \
		          [t for t in range(-5,7) \
		          if (self.u[-t]!=self.u[-(t+1)] and self.u[5-t]!=self.u[(5-t)+1])] \
		          for b in \
		          [t for t in range(-5,7) \
		          if (self.d[t-1]!=self.d[t] and self.d[5+t]!=self.d[((5+t)+1)%12])]]
		    # Remove (0,0) from valid turns
			self.valid_twists.remove((0,0))
		
	# Slice is reserved, so using / to slice
	def dash(self):
		s1=self.u[6:12][::-1]
		s2=self.d[6:12][::-1]
		self.u=self.u[0:6]+s2
		self.d=self.d[0:6]+s1
		self.fix_twists()
		
# Function to find the path between two given states (s and final)
# It's currently bruteforce and recursive (eew!) and it's not finished
def find_state(s,path,depth):
	global final
	# allstates stores all the states we've been through so we don't
	# repeat ourselves if we find a state we've been in before
	global allstates
	#print path
	# If we found a solution return the path we have so far with (0,0)
	# so it counts as a move (when we a long path, it's for the last /
	if s == final:
		path.append((0,0))
		return path
	# If we run too deep, we return an empty list	
	if depth == MAX_DEPTH:
		return []
	# Check if the current state is one we've been on before
	if (s.u,s.d) not in allstates:
		allstates.append((s.u,s.d))
	else:
		# Not too happy about this, as we can reach here from a better
		# position but I'm not sure what we can do to improve
		return []
	# We have a new position, we do the following for every possible turn 
	for t in s.valid_twists:
		# New variable so we can keep s intact. 		
		new = s.copy()
		new.turn(t)
		# Checking if we have a AUF/ADF's solutions
		if new == final:
			path.append(t)
			return path
		# Add this position to the global list of positions
		allstates.append((new.u,new.d))
		# Slice

		new.dash()
		# Record the move in a new path so we keep the current path
		# intact and move on to find a new solution
		# by calling the function one level down in depth		
		newpath = copy.copy(path)
		newpath.append(t)
		res = find_state(new,newpath,depth+1)
		# We have returned from the function call so we either have :
		# the empty set, which didn't find anything for this 
				
		if res == []:
			# so we carry on with the cycle
			continue
			# if we found a solution, we return it (as path)
		else:
			# Found a solution. Return the resulting path to it.
			return res
	# We ran out of turns here so we return nothing.		
	return []		

	
#Just a test
# Final position is solved
# b is (3,0) of solved
		
final = sq1state()
# 
b = sq1state('dd4aa18hh7gg','ee5ff63cc2bb')

#allstates = []
#x = find_state(b,[],0)
#print x	
