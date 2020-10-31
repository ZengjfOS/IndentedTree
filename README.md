## README

将缩进文本转换为缩进树，实现Linux下的tree命令的效果

## input

```
* title
  * program 1
    * text 1
  * program 2
    * text 2
    * program 3
      * text 3
      * program 4
        * text 4
    * program 5
      * text 5
  * program 6
    * text 6
```


## output

```
* title
  ├── program 1
  │   └── text 1
  ├── program 2
  │   ├── text 2
  │   ├── program 3
  │   │   ├── text 3
  │   │   └── program 4
  │   │       └── text 4
  │   └── program 5
  │       └── text 5
  └── program 6
      └── text 6
```
