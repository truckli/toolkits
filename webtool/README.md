

---



## Instructions: 

### Data format:

* format 1:

The first line of the data file consists of  column names which will not reappear in other lines.
From 2nd line to the last line is data lines.
A data line is like this:

>  3	http://hi.baidu.com/lfzxk/item/c0001131d3789486c3cf2954	qid:1 2 5 7 8	


In this case, features can be names like mOuterInlinkCount, mIsBadPage, etc ...

* format 2:

Each feature value is preceded by a feature number. Feature numbers reveal nothing about the meaning of this feature.
All lines are data lines like this:

> 3 qid:1 http://ios.d.cn/review/view-7683.html 1:0 2:0 3:0 4:0 5:0 6:0 7:0 8:0 9:0 10:0 ... 

In this case, features can be either a name (mOuterInlinkCount, mIsBadPage, etc) or a number (2, 5, etc) ...

### Data file name:

It is an absoluate path in the server where this app is running. Default to be the very folder where this app is.

### Caching:

If "Use no caching" checkbox is not checked, previous query result is returned without incurring time-consuming data analyzing.


### How to modify this tool:

You can find the script behind this app with **netstat**, and modify the code. This app is written with [tornado](http://www.tornadoweb.cn/).






