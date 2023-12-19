package lab1

import scala.annotation.tailrec

object Lab1 {
  def pascal(col: Int, row: Int): Int = {
    if(col < 0 || row < 0 || col > row + 1) 0
    else if (col == 0 || col == row) 1
    else pascal(col, row - 1) + pascal(col - 1, row - 1)
  }


  def balance(chars: List[Char]): Boolean = {
    @tailrec
    def dege4ki_tuda_duge4ki_suda(chars: List[Char], openCount: Int): Boolean = {
      if (chars.isEmpty) openCount == 0
      else {
        val currentChar = chars.head
        val tail = chars.tail

        if (currentChar == '(') dege4ki_tuda_duge4ki_suda(tail, openCount + 1)
        else if (currentChar == ')') {
          if (openCount < 1) false
          else dege4ki_tuda_duge4ki_suda(tail, openCount - 1)
        }
        else dege4ki_tuda_duge4ki_suda(tail, openCount)
      }
    }
    dege4ki_tuda_duge4ki_suda(chars, 0)
  }


  def countChange(money: Int, coins: List[Int]): Int = {
    if (money == 0) 1
    else if (money < 0 || coins.isEmpty) 0
    else countChange(money - coins.head, coins) + countChange(money, coins.tail)
  }
}