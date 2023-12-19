package lab3

/**
 * Клас який відображає твіти.
 */
class Tweet(val user: String, val text: String, val retweets: Int) {
  override def toString: String = s"$user: $text [$retweets]"
}

/**
 * Це множина об'єктів типу `Tweet` у вигляді бінарного дерева. Кожна гілка має дві дочірні гілки (два `TweetSet`).
 * Для цього дерева завжди виконується наступне правило: для кожної гілки `a`,
 * всі елементи в лівій дочірній гілці менші ніж твіт в `a`. А елементи в правій, відповідно, більші.
 *
 * Зауважимо, що вищевказана структура вимагає від нас можливості порівнювати два твіти.
 * В цій імплементації, рівність/порядок твітів базується на тексті твітів
 * (див `def add`). Таким чином, `TweetSet` не може містити двох однакових твітів з однаковим текстом.
 *
 *
 * Перевагою використання двійкових дерев для відображення множин елементів є швидкість їх пошуку в наборі.
 */

abstract class TweetSet {

  /**
   * Цей метод отримує предикат як вхідний аргументи і повертає підмножину
   * всіх елементів з оригінальної множини, для яких даний предикат є істинним.
   *
   * Питання: чи можемо ми реалізувати цей метод тут, чи він повинен залишитися абстрактним
   * і бути реалізованим в підкласах?
   **/
  def filter(p: Tweet => Boolean): TweetSet = filterAcc(p,  Empty)

  /**
   * Це метод-хелпер для filter який містить акумуляту для твітів.
   */
  def filterAcc(p: Tweet => Boolean, acc: TweetSet): TweetSet

  /**
   * Повертає новий `TweetSet`, який є обєднанням `this` і `that`.
   *
   * Питання: чи можемо ми реалізувати цей метод тут, чи він повинен залишитися абстрактним
   * і бути реалізованим в підкласах?
   */
  def union(that: TweetSet): TweetSet = filterAcc(t => true, that)

  /**
   * Повертає твіт, який має найбільшу кількість ретвітів.
   *
   * Виклик `mostRetweeted` на пустій множині повинен повертати помилку `java.util.NoSuchElementException`.
   *
   * Питання: чи можемо ми реалізувати цей метод тут, чи він повинен залишитися абстрактним
   * і бути реалізованим в підкласах?
   */
  def mostRetweeted: Tweet

  def mostRetweetedAcc(acc: Tweet): Tweet

  /**
   * Повертає список, який містить всі твіти з множини, відсортовані в низхідному порядку по кількості ретвітів.
   *
   * Підказка: метод `remove` над TweetSet буде дуже корисним.
   * Питання: чи можемо ми реалізувати цей метод тут, чи він повинен залишитися абстрактним
   * і бути реалізованим в підкласах?
   */
  def descendingByRetweet: TweetList

  /**
   * Наступні методи вже реалізовані
   */

  /**
   * Повертає новий `TweetSet` який містить всі елементи з this і елемент `tweet` якщо такого немає в this.
   *
   * Якщо `this.contains(tweet)`, ми отримуємо this.
   */
  def add(tweet: Tweet): TweetSet

  /**
   * Повертає новий `TweetSet` який не містить `tweet`.
   */
  def remove(tweet: Tweet): TweetSet

  /**
   * Перевіряє, чи `tweet` міститься в `TweetSet`.
   */
  def contains(tweet: Tweet): Boolean

  /**
   * Цей елементи отроимує функцію як аргумент і застосовує її ко кожного елемента множини.
   */
  def foreach(f: Tweet => Unit): Unit
}

object Empty extends TweetSet {
  def filterAcc(p: Tweet => Boolean, acc: TweetSet): TweetSet = acc

  def mostRetweeted: Tweet = throw new NoSuchElementException("mostRetweeted on empty set")

  def mostRetweetedAcc(acc: Tweet) = acc

  def descendingByRetweet: TweetList = Nil
  /**
   * Наступні методи вже реалізовані
   */

  def contains(tweet: Tweet): Boolean = false

  def add(tweet: Tweet): TweetSet = new NonEmpty(tweet, Empty, Empty)

  def remove(tweet: Tweet): TweetSet = this

  def foreach(f: Tweet => Unit): Unit = ()
}

class NonEmpty(elem: Tweet, left: TweetSet, right: TweetSet) extends TweetSet {

  def filterAcc(p: Tweet => Boolean, acc: TweetSet): TweetSet = {
    if (p(elem)) right.filterAcc(p, left.filterAcc(p, acc.add(elem)))
    else right.filterAcc(p, left.filterAcc(p, acc))
  }

  def mostRetweeted: Tweet = mostRetweetedAcc(elem)

  def mostRetweetedAcc(acc: Tweet): Tweet = {
    if (elem.retweets > acc.retweets) right.mostRetweetedAcc(left.mostRetweetedAcc(elem))
    else right.mostRetweetedAcc(left.mostRetweetedAcc(acc))
  }

  def descendingByRetweet: TweetList = new Cons(mostRetweeted, remove(mostRetweeted).descendingByRetweet)

  /**
   * Наступні методи вже реалізовані
   */

  def contains(x: Tweet): Boolean =
    if (x.text < elem.text) left.contains(x)
    else if (elem.text < x.text) right.contains(x)
    else true

  def add(x: Tweet): TweetSet = {
    if (x.text < elem.text) new NonEmpty(elem, left.add(x), right)
    else if (elem.text < x.text) new NonEmpty(elem, left, right.add(x))
    else this
  }

  def remove(tw: Tweet): TweetSet =
    if (tw.text < elem.text) new NonEmpty(elem, left.remove(tw), right)
    else if (elem.text < tw.text) new NonEmpty(elem, left, right.remove(tw))
    else left.union(right)

  def foreach(f: Tweet => Unit): Unit = {
    f(elem)
    left.foreach(f)
    right.foreach(f)
  }
}

trait TweetList {
  def head: Tweet

  def tail: TweetList

  def isEmpty: Boolean

  def foreach(f: Tweet => Unit): Unit =
    if (!isEmpty) {
      f(head)
      tail.foreach(f)
    }
}

object Nil extends TweetList {
  def head = throw new java.util.NoSuchElementException("head of EmptyList")

  def tail = throw new java.util.NoSuchElementException("tail of EmptyList")

  def isEmpty = true
}

class Cons(val head: Tweet, val tail: TweetList) extends TweetList {
  def isEmpty = false
}


object GoogleVsApple {
  val google = List("android", "Android", "galaxy", "Galaxy", "nexus", "Nexus")
  val apple = List("ios", "iOS", "iphone", "iPhone", "ipad", "iPad")

  // Метод exists на списках і contains на стрічках будуть корисними
  def filterTweetsByKeysInText(keys: List[String]): TweetSet = TweetLoader.allTweets.filter(t => google.exists(e => t.text.contains(e)))

  lazy val googleTweets: TweetSet = filterTweetsByKeysInText(google)
  lazy val appleTweets: TweetSet = filterTweetsByKeysInText(apple)

  /**
   * Список всіх твітів, в яких згадуються якісь із ключових слів з  apple чи google,
   * відсортований за кількістю ретвітів.
   */
  lazy val trending: TweetList = googleTweets.union(appleTweets).descendingByRetweet
}

object Main {
  def main(args: Array[String]): Unit = {
    GoogleVsApple.trending foreach println
    // Очікуваний вивід:
    // gizmodo: Warning: Security bug c... [290]
    // CNET: How to switch from iPhone ... [131]
    // gadgetlab: #Apple #iPhone5 batte... [121]
    // ...
  }
}