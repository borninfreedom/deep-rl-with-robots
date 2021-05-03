# Python Knowledge
## [Python中的作用域、global与nonlocal](https://note.qidong.name/2017/07/python-legb/)
## [Delgan/loguru](https://github.com/Delgan/loguru), this is a great python log module, it is much greater than python built in logging module.
## [wandb](https://wandb.ai/site),Developer tools for machine learning. Build better models faster with experiment tracking, dataset .
## logging usage
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    filename='./logs/client1-{}.log'.format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),
    filemode='w')
logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
stream_handler = logging.StreamHandler()

stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


# in the codes.
# logger.info()
# logger.debug()
```

## Notes from fluent python.
### 特殊方法
*  Python 2.6 开始，namedtuple 就加入到 Python 里，用以构建只有少数属性但是没有方法的对象，比如数据库条目
* bool(x) 的背后是调用 x.__bool__() 的结果,如果不存在 __bool__ 方法，那么 bool(x) 会尝试调用 x.__len__()。若返回 0，则 bool 会返回 False；否则返回 True。

```python
from math import hypot
class Vector:
 def __init__(self, x=0, y=0): 
    self.x = x
    self.y = y
 def __repr__(self):
    return 'Vector(%r, %r)' % (self.x, self.y) 
 def __abs__(self):
    return hypot(self.x, self.y)
 def __bool__(self):
    return bool(abs(self))
 def __add__(self, other):
    x = self.x + other.x
    y = self.y + other.y
    return Vector(x, y)
 def __mul__(self, scalar):
    return Vector(self.x * scalar, self.y * scalar)
 ```
# Python tricks for algorithms and data structure
## string to char and char to string
```python
a="string"
b=list(a)
#b=['s', 't', 'r', 'i', 'n', 'g']
c=''.join(b)
#c='string'
```

## the extend method is more convenience than append
## Be good at map function, [Python map() 函数](https://www.runoob.com/python/python-func-map.html)