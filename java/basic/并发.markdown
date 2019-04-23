### synchronized的三种使用方式

+ 修饰实例方法，作用于当前对象实例加锁，进入同步代码需要获取当前对象实例的锁
+ 修饰静态方法，作用于当前类对象加锁，进入同步代码前要获得当前类对象的锁。也就是给当前类加锁，会作用于类的所有对象实例，因为静态成员不属于任何一个实例对象，是类成员（ static 表明这是该类的一个静态资源，不管new了多少个对象，只有一份，所以对该类的所有对象都加了锁）。所以如果一个线程A调用一个实例对象的非静态 synchronized 方法，而线程B需要调用这个实例对象所属类的静态 synchronized 方法，是允许的，不会发生互斥现象，**因为访问静态 synchronized 方法占用的锁是当前类的锁，而访问非静态 synchronized 方法占用的锁是当前实例对象锁**。
+ 修饰代码块，指定加锁对象，对给定对象加锁，进入同步代码库前要获得给定对象的锁。和 synchronized 方法一样，synchronized(this)代码块也是锁定当前对象的。synchronized 关键字加到 static 静态方法和 synchronized(class)代码块上都是是给 Class 类上锁。这里再提一下：synchronized关键字加到非 static 静态方法上是给对象实例上锁。另外需要注意的是：尽量不要使用 synchronized(String a) 因为JVM中，字符串常量池具有缓冲功能！

下面已一个常见的面试题为例讲解一下synchronized关键字的具体使用。

面试中面试官经常会说："单例模式了解嘛？来给我手写一下，给我解释一下双重检验锁方式实现单例模式的原理呗！"

#### 双重校验锁对象单例（线程安全）

>```java
>public class Singleton {
>
>    private volatile static Singleton uniqueInstance;
>
>    private Singleton() {
>    }
>
>    public static Singleton getUniqueInstance() {
>       //先判断对象是否已经实例过，没有实例化过才进入加锁代码
>        if (uniqueInstance == null) {
>            //类对象加锁
>            synchronized (Singleton.class) {
>                if (uniqueInstance == null) {
>                    uniqueInstance = new Singleton();
>                }
>            }
>        }
>        return uniqueInstance;
>    }
>}
>```

另外，需要注意 uniqueInstance 采用 volatile 关键字修饰也是很有必要。

uniqueInstance 采用 volatile 关键字修饰也是很有必要的， uniqueInstance = new Singleton(); 这段代码其实是分为三步执行：

+ 为uniqueInstance分配内存空间
+ 初始化uniqueInstance
+ 将uniqeInstance指向分配的内存地址

但是由于 JVM 具有指令重排的特性，执行顺序有可能变成 1->3->2。指令重排在单线程环境下不会出现问题，但是在多线程环境下会导致一个线程获得还没有初始化的实例。例如，线程 T1 执行了 1 和 3，此时 T2 调用 getUniqueInstance() 后发现 uniqueInstance 不为空，因此返回 uniqueInstance，但此时 uniqueInstance 还未被初始化。

使用volatile可以禁止JVM的指令重排，保证在多线程环境下也能正常运行。

**synchronized关键字底层原理属于JVM层面**

**synchronized同步语句块的情况**

>```java
>public class SynchronizedDemo {
>	public void method() {
>		synchronized (this) {
>			System.out.println("synchronized 代码块");
>		}
>	
>```

通过 JDK 自带的 javap 命令查看 SynchronizedDemo 类的相关字节码信息：首先切换到类的对应目录执行 `javac SynchronizedDemo.java` 命令生成编译后的 .class 文件，然后执行`javap -c -s -v -l SynchronizedDemo.class`。

![1](./img/thread/1.png)

从上面我们可以看出:

**synchronized同步语句块的实现使用的是monitorenter和monitorexit指令**，**其中 monitorenter 指令指向同步代码块的开始位置，monitorexit 指令则指明同步代码块的结束位置。** 当执行 monitorenter 指令时，线程试图获取锁也就是获取 monitor(monitor对象存在于每个Java对象的对象头中，synchronized 锁便是通过这种方式获取锁的，也是为什么Java中任意对象可以作为锁的原因) 的持有权.当计数器为0则可以成功获取，获取后将锁计数器设为1也就是加1。相应的在执行 monitorexit 指令后，将锁计数器设为0，表明锁被释放。如果获取对象锁失败，那当前线程就要阻塞等待，直到锁被另外一个线程释放为止。

**synchronized修饰方法的情况**

>public class SynchronizedDemo2{
>
>​			public synchronized void method(){
>
>​						System.out.println("Synchronized 方法");
>
>}
>
>}

![2](./img/thread/2.png)

synchronized 修饰的方法并没有 monitorenter 指令和 monitorexit 指令，取得代之的确实是 ACC_SYNCHRONIZED 标识，该标识指明了该方法是一个同步方法，JVM 通过该 ACC_SYNCHRONIZED 访问标志来辨别一个方法是否声明为同步方法，从而执行相应的同步调用。

在 Java 早期版本中，synchronized 属于重量级锁，效率低下，因为监视器锁（monitor）是依赖于底层的操作系统的 Mutex Lock 来实现的，Java 的线程是映射到操作系统的原生线程之上的。如果要挂起或者唤醒一个线程，都需要操作系统帮忙完成，而操作系统实现线程之间的切换时需要从用户态转换到内核态，这个状态之间的转换需要相对比较长的时间，时间成本相对较高，这也是为什么早期的 synchronized 效率低的原因。庆幸的是在 Java 6 之后 Java 官方对从 JVM 层面对synchronized 较大优化，所以现在的 synchronized 锁效率也优化得很不错了。JDK1.6对锁的实现引入了大量的优化，如自旋锁、适应性自旋锁、锁消除、锁粗化、偏向锁、轻量级锁等技术来减少锁操作的开销。

### synchronized和volatile的区别

两个关键字的比较

+ volatile关键字是线程同步的轻量级实现，所以volatile 性能肯定是比synchronized关键字要好。但是volatile关键字只能用于banal而synchronized关键字可以修饰方法以及代码块。synchronized关键字在JavaSE1.6之后进行了主要包括为了减少获得锁和释放锁带来的性能消耗而引入的偏向锁和轻量级锁以及其它各种优化之后执行效率有了显著提升，实际开发中使用synchronized关键字的场景还是多一点。
+ 多线程访问volatile关键字不好发生阻塞，而synchronized关键字可能会发生阻塞。
+ volatile关键字能够保证数据的可见性，但不能保证数据的原子性。synchronized关键字两者都能保证。
+ volatile关键字主要用于解决变量在多个线程之间的可见性，而synchronized关键字解决的是多个线程之间访问资源的同步性。



























