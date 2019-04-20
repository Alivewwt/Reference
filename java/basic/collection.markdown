### 容器

#### ArrayList与LinkedList异同

1. 是否保证线程安全：ArrayList与LinkedList都是不同步的，也就是不保证线程安全；
2. 底层数据结构：ArrayList底层使用的是Object数组；L inkedList底层使用的是双向数据结构（JDK1.6为循环链表，JDK1.7取消了循环。）；
3. 插入盒删除是否受元素位置的影响：（1）ArrayList采用数组存储，所以插入和删除元素复杂度受元素位置的影响；（2）LinkedList采用链表存储，所以插入，删除元素时间复杂度不受元素位置的影响，都是近似$O(1)$而数组近似$O(n)$;
4. 是否支持快速访问：LinkedList不支持高效的随机元素访问，而ArrayList支持。快速随机访问就是通过元素的序号快速获取元素对象方法；
5. 内存空间占用：ArrayList的空间浪费主要体现在在List列表的结尾会预留一定的容量空间，而LinkedList的空间花费则体现在它的每一个元素都需要消耗比ArrayList更多的空间。

ArrayList实现了RandomAccess接口，而LinkedList没有实现。为什么呢？我觉得还是和底层数据结构有关！ArrayList底层是数组，而LinkedList底层是链表。数组天然支持随机访问，时间复杂度为$O(1)$，所以称为快速随机访问。链表需要遍历到特定位置才能访问特定位置的元素，时间复杂度为$O(n)$，所以不支持快速随机访问。ArrayList实现了RandomAccess接口，就表明了它具有快速随机访问功能。RandomAccess接口只是标识，并不是说ArrayList实现RandomAccess接口才具有快速随机访问功能的。

**下面总结一下List的遍历方式选择**：

1. 实现了RandomAccess接口的list，优先选择普通for循环 ，其次foreach,
2. 未实现RandomAccess接口的ist， 优先选择iterator遍历（foreach遍历底层也是通过iterator实现的），大size的数据，千万不要使用普通for循环

#### ArrayList与Vector区别

Vector类的所有方法都是同步的。可以由两个线程安全地访问一个Vector对象、但是一个线程访问Vector的话代码要在同步操作上耗费大量的时间。

Arraylist不是同步的，所以在不需要保证线程安全时时建议使用Arraylist。

#### HashMap的底层实现

**JDK1.8之前**

JDK1.8 之前 HashMap 底层是 **数组和链表** 结合在一起使用也就是 **链表散列**。**HashMap 通过 key 的 hashCode 经过扰动函数处理过后得到 hash 值，然后通过 (n - 1) & hash 判断当前元素存放的位置（这里的 n 指的是数组的长度），如果当前位置存在元素的话，就判断该元素与要存入的元素的 hash 值以及 key 是否相同，如果相同的话，直接覆盖，不相同就通过拉链法解决冲突。**

**所谓扰动函数指的就是 HashMap 的 hash 方法。使用 hash 方法也就是扰动函数是为了防止一些实现比较差的 hashCode() 方法 换句话说使用扰动函数之后可以减少碰撞**

**JDK 1.8 HashMap 的 hash 方法源码:**

>```java
>  static final int hash(Object key) {
>      int h;
>      // key.hashCode()：返回散列值也就是hashcode
>      // ^ ：按位异或
>      // >>>:无符号右移，忽略符号位，空位都以0补齐
>      return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
>  }
>```

对比一下JDK1.7的hashmap的hash方法源码。

>```java
>static int hash(int h) {
>    // This function ensures that hashCodes that differ only by
>    // constant multiples at each bit position have a bounded
>    // number of collisions (approximately 8 at default load factor).
>
>    h ^= (h >>> 20) ^ (h >>> 12);
>    return h ^ (h >>> 7) ^ (h >>> 4);
>}
>```

所谓"拉链法"就是：将链表和数组相结合。也就是说创建一个链表数组，数组中每一格就是一个链表。若遇到哈希冲突，则将冲突的值加到链表中。

![1](./img/collections/1.png)

**JDK1.8之后**

相比于之前的版本，JDK1.8之后在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为8）时，将链表转化为红黑树，以减少搜索时间。

#### HashMap和Hashtable的区别

1. 线程是否安全：HashMap是非线程安全的，hashtable是线程安全的；hashtable内部方法基本都经过synchronized修饰；
2. 效率：因为线程安全的问题，hashmap要比hashtable效率要高一点。另外，hashtable基本被淘汰，不要在代码中使用它；
3. 对Null key 和Null value的支持：hashmap中，null可以作为键，这样的键只有一个，可以有一个或多个键所对应的值为null。但在hashtable中put进的键值只要有一个null，直接抛出NullPointException；
4. 初始容量大小和每次扩容容量大小的不同：（1）创建是如果不指定容量初始值，hashtabel默认初始大小为11，之后每次扩充，容量变为原来的2n+1.hashmap默认的初始化大小为16.之后每次扩充，容量变为原来的2倍。（2）创建是如果给定了容量初始值，那么hashtable会直接使用你给定的大小，而hashmap会将其扩充为2的幂次方大小；
5. 底层数据结构：JDK1.8以后的hashmap在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为8）时，链表转化为红黑树，以减少搜索时间，hashtable没有这样的机制。

#### HashMap的长度为什么是2的幂次方

为了能让 HashMap 存取高效，尽量较少碰撞，也就是要尽量把数据分配均匀。我们上面也讲到了过了，Hash 值的范围值-2147483648到2147483647，前后加起来大概40亿的映射空间，只要哈希函数映射得比较均匀松散，一般应用是很难出现碰撞的。但问题是一个40亿长度的数组，内存是放不下的。所以这个散列值是不能直接拿来用的。用之前还要先做对数组的长度取模运算，得到的余数才能用来要存放的位置也就是对应的数组下标。这个数组下标的计算方法是“ `(n - 1) & hash` ”。（n代表数组长度）。这也就解释了 HashMap 的长度为什么是2的幂次方。

**这个算法应该如何设计呢？**

我们首先可能会想到采用%取余的操作来实现。但是，重点来了：**“取余(%)操作中如果除数是2的幂次则等价于与其除数减一的与(&)操作（也就是说 hash%length==hash&(length-1)的前提是 length 是2的 n 次方；）。”** 并且 **采用二进制位操作 &，相对于%能够提高运算效率，这就解释了 HashMap 的长度为什么是2的幂次方。**

#### Hashmap多线程操作导致死循环问题

主要问题在于并发下的rehash会造成元素之间会形成一个循环链表。不过，JDK1.8后解决了这个问题，但是还是不建议在多线程下使用Hashmap,因为多线程下使用hashmap还是会存在其它问题比如数据丢失，并发环境下推荐使用ConcurrentHashMap.

#### HashSet和HashMap区别

如果你看过 HashSet 源码的话就应该知道：HashSet 底层就是基于 HashMap 实现的。（HashSet 的源码非常非常少，因为除了 clone() 方法、writeObject()方法、readObject()方法是 HashSet 自己不得不实现之外，其他方法都是直接调用 HashMap 中的方法。）

![2](./img/collections/2.png)

#### ConcurrentHashMap和Hashtable的区别

ConcurrentHashMap和Hashtable的区别主要体现在实现线程安全的方式上不同。

- **底层数据结构：** JDK1.7的 ConcurrentHashMap 底层采用 **分段的数组+链表** 实现，JDK1.8 采用的数据结构跟HashMap1.8的结构一样，数组+链表/红黑二叉树。Hashtable 和 JDK1.8 之前的 HashMap 的底层数据结构类似都是采用 **数组+链表** 的形式，数组是 HashMap 的主体，链表则是主要为了解决哈希冲突而存在的；
- **实现线程安全的方式（重要）：** ① **在JDK1.7的时候，ConcurrentHashMap（分段锁）** 对整个桶数组进行了分割分段(Segment)，每一把锁只锁容器其中一部分数据，多线程访问容器里不同数据段的数据，就不会存在锁竞争，提高并发访问率。 **到了 JDK1.8 的时候已经摒弃了Segment的概念，而是直接用 Node 数组+链表+红黑树的数据结构来实现，并发控制使用 synchronized 和 CAS 来操作。（JDK1.6以后 对 synchronized锁做了很多优化）** 整个看起来就像是优化过且线程安全的 HashMap，虽然在JDK1.8中还能看到 Segment 的数据结构，但是已经简化了属性，只是为了兼容旧版本；② **Hashtable(同一把锁)** :使用 synchronized 来保证线程安全，效率非常低下。当一个线程访问同步方法时，其他线程也访问同步方法，可能会进入阻塞或轮询状态，如使用 put 添加元素，另一个线程不能使用 put 添加元素，也不能使用 get，竞争会越来越激烈效率越低。

HashTable

![3](./img/collections/3.png)

JDK1.7的ConcurrentHashMap:

![4](./img/collections/4.png)

**JDK1.8的ConcurrentHashMap**

![5](./img/collections/5.png)

#### ConcurrentHashMap线程安全的具体实现方式

JDK1.7（上面有示意图）

首先将数据分为一段一段的存储，然后给每一段数据配一把锁，当一个线程占用锁访问其中一个段数据时，其它段的数据也能被其它线程访问。

**ConcurrentHashMap是由Segment数组结构和HashEntry数组结构组成**。

segment实现了ReentrantLock，所以Segment是一种可重入锁，扮演锁的角色。hashEntry用于存储键值对数据。

>```java
>static class Segment<K,V> extends ReentrantLock implements Serializable {
>}
>```

一个 ConcurrentHashMap 里包含一个 Segment 数组。Segment 的结构和HashMap类似，是一种数组和链表结构，一个 Segment 包含一个 HashEntry 数组，每个 HashEntry 是一个链表结构的元素，每个 Segment 守护着一个HashEntry数组里的元素，当对 HashEntry 数组的数据进行修改时，必须首先获得对应的 Segment的锁。

**JDK1.8（上面有示意图）**

ConcurrentHashMap取消了Segment分段锁，采用CAS和synchronized来保证并发安全。数据结构跟HashMap1.8的结构类似，数组+链表/红黑二叉树。Java 8在链表长度超过一定阈值（8）时将链表（寻址时间复杂度为O(N)）转换为红黑树（寻址时间复杂度为O(long(N))）

synchronized只锁定当前链表或红黑二叉树的首节点，这样只要hash不冲突，就不会产生并发，效率又提升N倍。

#### 集合框架总结

1. List
   + ArrayLits: Object数组
   + vector：Object数组
   + LinkedList：双向链表(JDK1.6之前为循环链表，JDK1.7取消了循环)
2. Set
   + HashSet(无序，唯一)：基于HashMap实现的，底层采用HashMap来保存元素。
   + LinkedHashSet:LinkedHashSet 继承与 HashSet，并且其内部是通过 LinkedHashMap 来实现的。有点类似于我们之前说的LinkedHashMap 其内部是基于 Hashmap 实现一样，不过还是有一点点区别的。
   + TreeSet(有序，唯一)：红黑树(自平衡的排序二叉树)。

Map

- **HashMap：** JDK1.8之前HashMap由数组+链表组成的，数组是HashMap的主体，链表则是主要为了解决哈希冲突而存在的（“拉链法”解决冲突）.JDK1.8以后在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为8）时，将链表转化为红黑树，以减少搜索时间
- **LinkedHashMap:** LinkedHashMap 继承自 HashMap，所以它的底层仍然是基于拉链式散列结构即由数组和链表或红黑树组成。另外，LinkedHashMap 在上面结构的基础上，增加了一条双向链表，使得上面的结构可以保持键值对的插入顺序。同时通过对链表进行相应的操作，实现了访问顺序相关逻辑。
- **HashTable:** 数组+链表组成的，数组是 HashMap 的主体，链表则是主要为了解决哈希冲突而存在的
- **TreeMap:** 红黑树（自平衡的排序二叉树）























