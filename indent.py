#!/usr/bin/env python3

def findIndexs(level, start, end, inLines, columnInterval):

    count = 0
    indexs = []

    for line in inLines:
        # level * columnInterval: 当前行本身缩进
        # (level - 1) * columnInterval: 额外添加的行缩进，目前是每个level添加2个空格，为了更方便的阅读
        if (len(line) > level * columnInterval and line[level * columnInterval + (level - 1) * columnInterval] == "*"):
            indexs.append(count)

        count += 1

    return indexs

def drawFunctionCallNet(level, start, end, inLines, columnInterval, debug):
    if debug:
        print("------------level %d--------------" % level)
        print(level)
        print(start)
        print(end)
        print(columnInterval)

        for line in inLines:
            print("".join(line))

    # 截取查找子索引的数据
    innerInLines = inLines[start + 1:end]
    # 查找子索引数组
    indexs = findIndexs(level + 1, start, end, innerInLines, columnInterval)
    if debug:
        print(indexs)

    if len(indexs) > 0:
        # 额外添加的行缩进，目前是每个level添加2个空格，为了更方便的阅读
        for row in range(0, len(innerInLines)):
            innerInLines[row].insert(2 * level * columnInterval, " ")
            innerInLines[row].insert(2 * level * columnInterval, " ")

        # 绘制当前的标记的列，range是前闭后开，所以要+1，因为前面为每个level增加了2个空格，替换字符位置是(2 * level + 1) * columnInterval为基准
        for row in range(0, indexs[-1] + 1):
            innerInLines[row][(2 * level + 1) * columnInterval] = "│"

        # 绘制当前标记的行，由于需要替换掉*号，所以行范围需要range内要+1，由于前面额外的每个level添加了2个空格，所以要以(2 * level + 1) * columnInterval为基准
        for column in indexs:
            for interval in range(0, columnInterval + 1):
                if interval == 0:
                    if column == indexs[-1]:
                        innerInLines[column][(2 * level + 1) * columnInterval] = "└"
                    else:
                        innerInLines[column][(2 * level + 1) * columnInterval] = "├"
                else:
                    innerInLines[column][(2 * level + 1) * columnInterval + interval] = "─"
            
        # 添加尾缀，便于递归
        indexs.append(len(innerInLines))
        # 开始递归，level递增，重新截取递归处理的行数据
        for index in range(0, len(indexs) - 1):
            if debug:
                print(str(indexs[index]) + ", " + str(indexs[index + 1]))
            nextinnerInLines = innerInLines[indexs[index]: indexs[index + 1]]
            drawFunctionCallNet(level + 1, 0, len(nextinnerInLines), nextinnerInLines, columnInterval, debug)

    else:
        return

    if level == 0:
        for line in inLines:
            print("".join(line))


if __name__ == "__main__" :
    inLines = []
    maxLevel = 0
    columnInterval = 2
    countLine = 0
    debug = False

    with open('indent.txt', 'r') as inFile:
        for line in inFile.readlines():

            line = line.replace("\n", "")
            if len(line) > 0:
                inLines.append(list(line))

                currentLevel = line.find("*")
                if currentLevel > maxLevel:
                    maxLevel = currentLevel

                countLine += 1

        maxLevel //= columnInterval

    if debug:
        print(maxLevel)

    # 前闭后开
    drawFunctionCallNet(0, 0, countLine, inLines, columnInterval, debug)

    with open("output.txt", "wb+") as outFile:
        for line in inLines:
            outFile.write(bytes("".join(line) + "\n", 'utf-8'))
