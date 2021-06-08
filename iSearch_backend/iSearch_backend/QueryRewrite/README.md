### 查询改写模块
#### 本模块包含自动纠错（中文）和查询关键词优化两个部分


- 查看所需要的包请查看requirements.txt
- 调用请使用QueryRewrite类的normal_extract和comprehensive_extrac两个方法
- 一个例子：
```python
from QueryRewrite import QueryRewrite

# 输入你的停用词文件位置、词频词典位置、所有doc的位置、模型位置以及中文词典的位置
qr = QueryRewrite(stopwords_path='./resources/stopwords.txt', file_path="./files", dict_path="./resources/word_freq.json", model_path='./model/word2vec.model', cn_dict_path="./resources/cn_dict.txt")
print('Query: 元气森林白讨含糖量！')
print('normal mode:', qr.normal_extract('元气森林白讨含糖量！'))
print('advanced mode:', qr.comprehensive_extract('元气森林白讨含糖量！'))
```
- 结果如下：
```
Query: 元气森林白讨含糖量！
normal mode: 元气 森林 白桃 含糖 含糖量
advanced mode: ('元气森林白桃含糖量！', 
['零糖', '无糖', '草本', '气泡', '冰博克', '椰子', '零卡', '糖浆', '牛乳', '含酒精', '椰子油', '苏打', '水在', '奶昔', '薯片', '果饮', '酒味', '燃茶', '醇厚', '龟苓膏', '纯牛奶', '山楂', '樱桃', '低卡', 
'果味', '果茶', '植物蛋白', '咸辣', '芝士', '乳茶', '桂花', '乌龙茶', '少糖', '燕麦', '麦片', '味', '奶油', '乳饮料', '胶原蛋白', '小瓶', '海苔', '酸辣', '脂', '低糖', '肉桂', '油柑', '焦糖', '搅打', '玉米须', '黄油', '咸', '爽口', '米酒', '罐装', '咸甜', '如白桃味', '茶中', '酸奶', '陈皮',
'芝芝', '黑糖', '清凉', '茶饮料', '锡兰', '小苏打', '果肉', '青梅', '粽子', '白砂', '蛋黄', '齁', '高蛋白', '溶', '配料', '芋圆', '旺仔', '巧克力', '二厂', '碳酸', '酥', '蘸', '膨化', '饼干', '起泡', '香草', '肉饼', '蔗糖', '抗糖', '水等', 
'醇香', '袋装', '必如', '桃桃', '味全', '香味', '果汁', '甘露', '酸辣粉', '葡', '冰博克厚'], 
'元气 森林 白桃 含糖 含糖量 零糖 无糖 草本')
```

#### 更新了自动补全功能
- 请使用AutoComplete的normal_complete和comprehensive_complete
- 一个例子：
```python
from AutoComple import AutoComplete

# 输入词频词典路径和模型路径
ac = AutoComplete('./QueryRewrite/resources/word_freq.json', './QueryRewrite/model/word2vec.model')
print('Query: 太晚读')
print(ac.normal_complete('太晚读'))
print(ac.comprehensive_complete('太晚读'))
```
- 结果如下：
```python
Query: 太晚读
normal mode: ['太晚读者', '太晚读书', '太晚读取', '太晚读懂', '太晚读完', '太晚读物', '太晚读写', '太晚读过', '太晚读数', '太晚读书会']
advanced mode: ['太晚读过', '太晚读完', '太晚读书会', '太晚读懂', '太晚读书', '太晚读写', '太晚读者', '太晚读取', '太晚读物', '太晚读数']
```