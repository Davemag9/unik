package LinkedList

class LinkedList[A] {
  class Node(var data: A, var next: Option[Node] = None)
  private var head: Option[Node] = None

  def add(element: A): Unit = {
    val newNode = new Node(element)
    if (head.isEmpty) {
      head = Some(newNode)
    } else {
      var current = head
      while (current.get.next.isDefined) {
        current = current.get.next
      }
      current.get.next = Some(newNode)
    }
  }

  def reverse(): Unit = {
    var prev: Option[Node] = None
    var current = head
    while (current.isDefined) {
      val nextNode = current.get.next
      current.get.next = prev
      prev = current
      current = nextNode
    }
    head = prev
  }

  def ++(otherList: LinkedList[A]): LinkedList[A] = {
    var current = otherList.head
    while (current.isDefined) {
      this.add(current.get.data)
      current = current.get.next
    }
    this
  }

  def insertionSort(implicit ordering: Ordering[A]): Unit = {
    def insertSorted(sorted: Option[Node], data: A, ordering: Ordering[A]): Option[Node] = {
      val newNode = new Node(data)
      if (sorted.isEmpty || ordering.gteq(sorted.get.data, data)) {
        newNode.next = sorted
        return Some(newNode)
      }
      var current = sorted
      while (current.get.next.isDefined && ordering.lt(current.get.next.get.data, data)) {
        current = current.get.next
      }
      newNode.next = current.get.next
      current.get.next = Some(newNode)
      sorted
    }

    var sorted: Option[Node] = None
    var current = head
    while (current.isDefined) {
      val next = current.get.next
      sorted = insertSorted(sorted, current.get.data, ordering)
      current = next
    }
    head = sorted
  }

  def bubbleSort(ordering: Ordering[A]): Unit = {
    var swapped: Boolean = true

    while (swapped) {
      var current = head
      swapped = false

      while (current.isDefined && current.get.next.isDefined) {
        val nextNode = current.get.next
        if (ordering.gt(current.get.data, nextNode.get.data)) {
          val temp = current.get.data
          current.get.data = nextNode.get.data
          nextNode.get.data = temp
          swapped = true
        }
        current = current.get.next
      }
    }
  }

  def mergeSort(implicit ordering: Ordering[A]): Unit = {
    def mergeSortInternal(list: Option[Node], ordering: Ordering[A]): Option[Node] = {

      def merge(left: Option[Node], right: Option[Node]): Option[Node] = {
        (left, right) match {
          case (Some(l), None) => Some(l)
          case (None, Some(r)) => Some(r)
          case (Some(l), Some(r)) =>
            if (ordering.lteq(l.data, r.data)) {
              l.next = merge(l.next, Some(r))
              Some(l)
            } else {
              r.next = merge(Some(l), r.next)
              Some(r)
            }
//          case _ => None
        }
      }

      def FloydSplit(n: Option[Node]): (Option[Node], Option[Node]) = {
        var slow = n
        var fast = n
        var prev: Option[Node] = None

        while (fast.isDefined && fast.get.next.isDefined) {
          prev = slow
          slow = slow.get.next
          fast = fast.get.next.get.next
        }

        val left = n
        val right = slow
        prev.get.next = None
        (left, right)
      }

      list match {
        case Some(_) =>
          if (list.get.next.isEmpty) list
          else {
            val (left, right) = FloydSplit(list)
            merge(mergeSortInternal(left, ordering), mergeSortInternal(right, ordering))
          }
//        case None => None
      }
    }

    head = mergeSortInternal(head, ordering)
  }

  def quickSort(implicit ordering: Ordering[A]): Unit = {
    def quickSortAcc(start: Option[Node], end: Option[Node]): Unit = {
      if (start != end) {
        val pivot = partition(start, end)
        quickSortAcc(start, pivot)
        if (pivot.isDefined && pivot.get.next.isDefined) {
          quickSortAcc(pivot.get.next, end)
        }
      }
    }

    def partition(start: Option[Node], end: Option[Node]): Option[Node] = {
      val pivot = start.get.data
      var i = start
      var j = start.get.next
      while (j != end) {
        if (ordering.compare(j.get.data, pivot) <= 0) {
          i = if (i.isDefined) i.get.next else None
          swap(i, j)
        }
        j = j.get.next
      }
      if (i.isDefined) {
        swap(i, start)
      }
      i
    }

    def swap(node1: Option[Node], node2: Option[Node]): Unit = {
      val temp = node1.get.data
      node1.get.data = node2.get.data
      node2.get.data = temp
    }

    quickSortAcc(head, None)
  }

  def printList(): Unit = {
    var current = head
    while (current.isDefined) {
      print(current.get.data + " ")
      current = current.get.next
    }
    println("\n")
  }
}

object Main {
  def main(args: Array[String]): Unit = {

    val intList = new LinkedList[Int]
    intList.add(5)
    intList.add(3)
    intList.add(8)
    intList.add(1)

    println("Integer list:")
    intList.printList()

    intList.reverse()
    println("Reversed integer list:")
    intList.printList()

    val intList2 = new LinkedList[Int]
    intList2.add(12)
    intList2.add(6)
    println("Another list:")
    intList2.printList()
    intList ++ intList2
    println("Integer list after marge with another list:")
    intList.printList()

    val sortedAscList = new LinkedList[Int]
    sortedAscList ++ intList // create a copy
    sortedAscList.insertionSort(Ordering.Int)
    println("Integer list after Insertion Sort:")
    sortedAscList.printList()

    val bubbleSortedDescList = new LinkedList[Int]
    bubbleSortedDescList ++ intList
    bubbleSortedDescList.bubbleSort(Ordering.Int)
    println("Integer list after Bubble Sort:")
    bubbleSortedDescList.printList()

    val mergeSortedAscList = new LinkedList[Int]
    mergeSortedAscList ++ intList
    mergeSortedAscList.mergeSort(Ordering.Int)
    println("Integer list after Merge Sort:")
    mergeSortedAscList.printList()

    val quickSortedDescList = new LinkedList[Int]
    quickSortedDescList ++ intList
    quickSortedDescList.quickSort(Ordering.Int)
    println("Integer list after Quick Sort:")
    quickSortedDescList.printList()

    println("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    val stringList = new LinkedList[String]
    stringList.add("ab")
    stringList.add("bc")
    stringList.add("cd")
    stringList.add("de")
    stringList.add("ef")
    stringList.add("fg")

    println("String list:")
    stringList.printList()

    stringList.reverse()
    println("Reversed string list:")
    stringList.printList()

    val sortedDescListString = new LinkedList[String]
    sortedDescListString ++ stringList
    sortedDescListString.insertionSort(Ordering[String].reverse)
    println("String list after Insertion Sort:")
    sortedDescListString.printList()

    val bubbleSortedAscListString = new LinkedList[String]
    bubbleSortedAscListString ++ stringList
    bubbleSortedAscListString.bubbleSort(Ordering[String].reverse)
    println("String list after Bubble Sort:")
    bubbleSortedAscListString.printList()

    println("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    val charList = new LinkedList[Char]
    charList.add('a')
    charList.add('b')
    charList.add('c')
    charList.add('d')
    charList.add('e')
    charList.add('f')

    println("Char list:")
    charList.printList()

    val mergeSortedDescListChar = new LinkedList[Char]
    mergeSortedDescListChar ++ charList
    mergeSortedDescListChar.mergeSort(Ordering[Char].reverse)
    println("Char list after Merge Sort:")
    mergeSortedDescListChar.printList()

    val quickSortedAscListChar = new LinkedList[Char]
    quickSortedAscListChar ++ charList
    quickSortedAscListChar.quickSort(Ordering[Char].reverse)
    println("Char list after Quick Sort:")
    quickSortedAscListChar.printList()
  }
}