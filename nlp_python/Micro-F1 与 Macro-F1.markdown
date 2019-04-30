### 数据

| 预测 | 真实 |
| :--: | :--: |
|  A   |  A   |
|  A   |  A   |
|  B   |  A   |
|  C   |  A   |
|  B   |  B   |
|  B   |  B   |
|  C   |  B   |
|  B   |  C   |
|  C   |  C   |

可以看出，上表是一份样本量为9，类别为3的含标注结果的三分类预测样本

### F1 score

$$
F1 = 2*\frac{precision*recall}{precision+recall}
$$

下面计算各个类别的准召：

对于类别A：

|  TP  |  FN  |
| :--: | :--: |
|  2   |  2   |
|  FP  |  TN  |
|  0   |  ～  |

$$
precision = 2/(2+0)=100\%
$$

$$
recall =2/(2+2)=50\%
$$

对于类别B

|  TP  |  FN  |
| :--: | :--: |
|  2   |  1   |
|  FP  |  TN  |
|  2   |  ～  |

$$
precision = 2/(2+2) =50\%\\
recall =2/(2+1)=67\%
$$

对于类别C

|  TP  |  FN  |
| :--: | :--: |
|  1   |  1   |
|  FP  |  TN  |
|  2   |  ～  |

$$
precision =1/(1+2)=33\%\\
recall =1/(1+1)=50\%
$$

TN对于准召的计算而言是不想要的，因此上面的表格中未统计该值。

下面调用sklearn的api进行验证：

>from sklearn.metrics import classification_report
>
>print(classification_report([0,0,0,0,1,1,1,2,2], [0,0,1,2,1,1,2,1,2]))
>
>```python
>           precision    recall  f1-score   support
>
>          0       1.00      0.50      0.67         4
>          1       0.50      0.67      0.57         3
>          2       0.33      0.50      0.40         2
>
>avg / total       0.69      0.56      0.58         9
>```

可以看出，各个类别的准召计算完全一致。

### Micro F1

Micro f1不需要区分类别，直接使用总体样本的准召计算f1 score.

该样本的混淆矩阵如下：

|  TP  |  FN  |
| :--: | :--: |
|  5   |  4   |
|  FP  |  TN  |
|  4   |  ～  |

$$
precision = 5/(5+4)=0.5556\\
recall = 5/(5+4)=0.5556 \\
F1 = 2*(0.5556*0.5556)/(0.5556+0.5556)=0.5556
$$

下面调用sklearn的api进行验证

>from sklearn.metrics import f1_score
>
>F1_score([0,0,0,0,1,1,1,2,2], [0,0,1,2,1,1,2,1,2],average='micro')
>
>0.555555556

可以看出，计算结果也是一致的（精度保留问题）

### Macro F1

不同于micro f1,macro f1需要先计算每一个类别的准召及其f1 score，然后通过求平均值得到在整个样本上的 f1 score.

类别A的：
$$
F_{1A}=2*\frac{1*0.5}{1+0.5}=0.6667
$$
类别B的：
$$
F_{1B}=2*\frac{0.5*0.67}{0.5+0.67}=0.57265
$$
类别C的：
$$
F_{1C}=2*\frac{0.33*0.5}{0.33+0.5}=0.39759
$$
整体的f1值为上面三者的平均值：
$$
F1=(0.6667+0.57265+0.39759)/3=0.546
$$
调用sklearn的api进行验证：

```python
from sklearn.metrics import f1_score
f1_score([0,0,0,0,1,1,1,2,2], [0,0,1,2,1,1,2,1,2],average="macro")
0.546031746031746
```



