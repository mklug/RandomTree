# RandomTree

This repository contains a library of functions for uniformly sampling binary trees and ordered trees (trees where the children are an ordered list) with a given number of nodes.  This is done efficiently either by Remy's method of growing a binary tree randomly node-by-node (and then using a bijection to ordered trees if desired) or by using the Fischer-Yates algorithm together with the cycle lemma to uniformly randomly generate modified Dyck paths and then converting these to trees.  Both algorithms are implemented here.
