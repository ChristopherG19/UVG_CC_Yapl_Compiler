'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
    Laboratorio#1
'''

class Node():
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.leftChild = left
        self.rightChild = right
        
