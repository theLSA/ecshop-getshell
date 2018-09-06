ecshop-getshell.py-ecshop rce getshell漏洞检测工具<br><br>
========

# 概述<br>
ecshop 2.x rce getshell漏洞，漏洞文件为user.php，由于$arr[id]和$arr[num]没有过滤导致SQL注入，进而可getshell，详情参考[ecshop2.x远程代码执行漏洞重现及分析](http://www.lsablog.com/networksec/penetration/ecshop2-x-rce-analysis/)<br>
本工具支持单url，批量检测该漏洞。<br><br>

# 快速开始<br>
python ecshop-getshell.py -h<br>
![](https://github.com/theLSA/ecshop-getshell/raw/master/demo/ecshoprce04.png)
<br>

单url检测：python ecshop-getshell.py -u "http://www.aaa.com/user.php?act=logni"<br>
![](https://github.com/theLSA/ecshop-getshell/raw/master/demo/ecshoprce02.png)
<br>

批量检测：python ecshop-getshell.py -f urls.txt -t 7 -s 6<br>
![](https://github.com/theLSA/ecshop-getshell/raw/master/demo/ecshoprce03.png)
<br><br>

# 反馈<br>
[issues](https://github.com/theLSA/ecshop-getshell/issues)
<br>
gmail：lsasguge196@gmail.com<br>
QQ邮箱：2894400469@qq.com<br>
