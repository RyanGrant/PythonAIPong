"""
Michael Holt
CSCI 315
Assignment 3
backprop.py
"""

import numpy as np
import pickle
import time

class Backprop(object):

    def __init__(self, n, h, m, weightscale = 1):
        # Want to get weights between a small interval around 0
        self.weights_IH = np.random.randn(n + 1, h)*weightscale
        self.weights_HO = np.random.randn(h + 1, m)*weightscale
        self.n = n
        self.m = m
        self.h = h
        
    def __str__(self):
        return "A backprop network with " + str(self.n) + " inputs, " + \
               str(self.h) + " hidden units, and " + \
               str(self.m) + " outputs."

    def test(self, I):
        # Need to append a 1 to I for the bias term
        # No longer using a linear classifier
        H_net = np.dot(np.append(I,[1]), self.weights_IH)
        # Call the squashing function on our above H_net, a 1 x h matrix
        H = self.squash(H_net)
        # Append the bias
        H_1 = np.append(H, 1)
        # H_1 is a 1 x (h+1) and we multiply by a (h+1) x m to make
        # a 1 x m O_net
        O_net = np.dot(H_1,self.weights_HO)
        # O is still 1 x m
        O = self.squash(O_net)
        return O.astype('float')

    def squash(self, x):
        return 1 / (1 + np.exp(-x))
   
    '''
    train takes an list of inputs I, a corresponding list of outputs
    T, a number of iterations niter, and a small positive value eta to
    represent the learning rate
    '''
    def train(self, I, T, niter=1000, eta=0.5, mu=0):

        assert len(I) == len(T)

        # Initialize the previous weight changes to 0
        delta_W_IH_prev = 0
        delta_W_HO_prev = 0

        lyst_of_rms = []
        lyst_of_H = []
        lyst_of_O = []
        
        for i in range(niter):
            
            # Initialize weight changes to zeros
            delta_W_IH = np.zeros((self.n+1, self.h))
            delta_W_HO = np.zeros((self.h+1, self.m))

            # Initialize RMS error to 0
            rmserr = 0

            # P is number of patterns
            p = len(I)

            for j in range(p):
                
                H_net = np.dot(np.append(I[j],1), self.weights_IH)
                
                # Call the squashing function on our above H_net, a 1 x h matrix
                H = self.squash(H_net)
                
                # H_1 is a 1 x (h+1) and we multiply by a (h+1) x m to make
                # a 1 x m O_net
                O_net = np.dot(np.append(H, 1),self.weights_HO)
                
                # O is still 1 x m
                O = self.squash(O_net)
                lyst_of_H.append(H[0])
                lyst_of_O.append(O[0])
                
                # delta_O is (1 x m)(1 x m) [Hadamard product]
                E = T[j] - O
                
                delta_O = E * (O*(1-O))
                
                # accumulate RMS error
                rmserr += sum(E*E)
                
                # Back propagation
                delta_H = np.dot(delta_O, self.weights_HO.T)[:-1]
                
                delta_H = delta_H * (H*(1-H))
            
                # Learning
                delta_W_IH += np.outer(np.append(I[j],1), delta_H)
                delta_W_HO += np.outer(np.append(H, 1), delta_O)

            # Compute mean and take square root to get actual RMS error 
            rmserr = np.sqrt(rmserr/(p*self.m))

            # Store the values of two weights and the RMS error for graphing
            # Part 4.4
            if self.h >= 1:
                lyst_of_rms.append((rmserr, self.weights_HO[0]))
            
            # Average the weight changes over the patterns
            delta_W_IH /= p
            delta_W_HO /= p

            # Update weights with batch learning and momentum
            self.weights_IH += (eta*delta_W_IH) + (mu*delta_W_IH_prev)
            self.weights_HO += (eta*delta_W_HO) + (mu*delta_W_HO_prev)

            # Update the previous weight changes for momentum next time
            delta_W_IH_prev = np.copy(delta_W_IH)
            delta_W_HO_prev = np.copy(delta_W_HO)
            
            print("\tCompleted " + str(i+1) + " / " + str(niter) + "  Error = " + str(rmserr))
            
        print("Done training!\n")

    '''
    save will save the current weights and time it took to train using pickling
    '''
    def save(self, fileName):
        fileObj = open(fileName, 'wb')
        pickle.dump(self.weights_IH, fileObj)
        pickle.dump(self.weights_HO, fileObj)
        fileObj.close()

    '''
    load will load in a set of weights using pickling
    '''
    def load(self, fileName):
        fileObj = open(fileName, 'rb')
        try:
            while True:
                self.weights_IH = pickle.load(fileObj)
                self.weights_HO = pickle.load(fileObj)
        except: fileObj.close()
    

