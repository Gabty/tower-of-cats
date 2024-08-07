import json
import os

from stack import Stack # literally my stack :>
# specifically for tower of hanoi leaderboard ....
class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
    
    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self.__insert(self.root, data)
    
    def __insert(self, root, data):
        if root.data['score'] > data['score']:
            if root.left:
                self.__insert(root.left, data)
            else:
                root.left = Node(data)
        else:
            if root.right:
                self.__insert(root.right, data)
            else:
                root.right = Node(data)
    def display(self): # left to right
        if self.root:
            for i in self.inorder(self.root):
                print(i)
    
    def inorder(self, root): # left to right only for debug lolz
        if root:
            yield from self.inorder(root.left)
            yield root.data
            yield from self.inorder(root.right)
    

    
    def reverse_inorder(self, root):
        if root:
            yield from self.reverse_inorder(root.right)
            yield root.data
            yield from self.reverse_inorder(root.left)
    
    # uses list for output
    def get_first_values(self,n):
        result = []
        i = 0
        for x in self.reverse_inorder(self.root):
            if i == n:
                break
            result.append(x)
            i +=1 
        return result
    def size(self, root):
        if root:
            return 1 + self.size(root.left) + self.size(root.right)
        else:
            return 0
    
    def __len__(self):
        return self.size(self.root)

    
    @staticmethod # independent method
    def load_json():
        bst = BinaryTree()
        if not os.path.exists('leaderboard.json'):
            open('leaderboard.json', 'w+').write('[]')
            return bst
        with open('leaderboard.json', 'r+') as fl:
            data = json.load(fl)
        for i in data:
            bst.insert(i)
        return bst
if __name__ == '__main__':
    root = BinaryTree()

    root.insert({"score": 8})
    root.insert({"score": 4})
    root.insert({"score": 6})
    root.insert({"score": 9})

    print(root.get_first_values(7))