# -*- coding:utf-8 -*-
# Author:YEAR
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def addTwoNumbers(l1, l2):
    """
    :type l1: ListNode
    :type l2: ListNode
    :rtype: ListNode
    """
    jinwei=False
    cNode1=l1
    cNode2=l2
    rListNode=ListNode(0)
    crNode=rListNode
    while True:
        #cVal1=cNode1 is not None?cNode1.val:0
        #cVal2=cNode2 is not None?cNode2.val:0
        cVal1=cNode1.val if cNode1 is not None else 0
        cVal2=cNode2.val if cNode2 is not None else 0
        nodeSum=cVal1+cVal2+crNode.val
        if nodeSum < 10:
            crNode.val=nodeSum
            crNode.next=ListNode(0)
        else:
            crNode.val=nodeSum-10
            crNode.next=ListNode(1)
        cNode1=cNode1.next if cNode1 is not None else None
        cNode2=cNode2.next if cNode2 is not None else None
        if cNode1==None and cNode2==None:
            if crNode.next.val==0:
                crNode.next=None
            return rListNode
        else:
            crNode = crNode.next


def showResult(node):
    while True:
        print(node.val,end='-')
        node=node.next
        if node==None :
            return

if __name__=="__main__":
    a3=ListNode(3)
    a2=ListNode(4)
    a1=ListNode(2)
    a1.next=a2
    a2.next=a3

    b3=ListNode(4)
    b2=ListNode(6)
    b1=ListNode(5)
    b1.next=b2
    b2.next=b3

    c1=ListNode(1)
    c2=ListNode(8)
    c1.next=c2

    d1=ListNode(0)

    showResult(addTwoNumbers(c1,d1))


