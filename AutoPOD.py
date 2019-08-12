#!/usr/bin/env python
# coding:utf-8

# """
# @File    : AutoPOP.py
# @Time    : 2019/8/10 0010 20:52
# @Author  : Noah_shan
# @Email   : 451145552@qq.com
# @Software: PyCharm
# """

# """
# TODO:
# 0.使用之前，需要将需要升级的pod库代码更新到目标服务器
# 1.根据配置文件提示出来需要升级的ＰＯＤ库
#     a.添加一个ｙａｍｌ文件，用来处理配置信息：库名称、路径、pod trunk push rule
# 2.用户选择配置库后，填写需要升级的版本号
#     a.根据用户选择的配置项目，cd到目标路径
#     b.根据用填写的 version,执行 git tag version &　git tap push version命令
# ３.根据配置好的pod trunk push rule 执行命令即可
# """

import json
import os
import subprocess

# 将所有的配置文件信息组装到ｔｕｐｌｅ中
def PreProgressJSONData():
    iifile = open("Package.json", "rb")
    filejson = json.load(iifile)
    dependencies = filejson["dependencies"]
    data = dependencies["data"]
    namersult = []
    modulepath = []
    moduleid = []
    chinesename = []
    trunkarr = []
    for i in data:
        namersult.append(i["moduleName"])
        moduleid.append(i["moduleID"])
        chinesename.append(i["moduleCNName"])
        modulepath.append(i["modulePath"])
        trunkarr.append(i["podOrder"])
    # all required infos
    # name, path, id, chinesename, pod order, trunk order
    return namersult, modulepath, moduleid, chinesename, trunkarr


# 将组装好的ｔｕｐｌｅ信息展示给用户，让用户去选择
def AlertTupleInfo2User(infos):
    print('All modules: \n')
    for idx in range(len(infos[0])):
        titleinfo = str(infos[2][idx]) + ". " + infos[0][idx]
        shouldspace = 30 - len(titleinfo)
        eachline = titleinfo + (" " * shouldspace) + infos[3][idx]
        print(eachline)


# 接受用户的输入，根据用户的输入显示进行操作
def ProgressUserInput(tupleinfo):
    name = input('\nSelect one module which u should update. Then press Enter to continue.\n')
    print('\nU should update the module of ' + tupleinfo[0][int(name)])
    return int(name)


# 处理git命令，git tag & push , 用户传入 version , 最后执行pod trunk push 指令
def GitProgress(tupleinfo, selectedidx):
    print('\nGit tag and Git tag push start ...')
    os.getcwd()
    os.chdir(tupleinfo[1][selectedidx])
    os.getcwd()
    trunkorder = tupleinfo[4][selectedidx]
    try:
        # should use input tag version
        taginfo = input('\nInput the module verson u should upload then press Enter 2 continue.'
                        ' \n ! Wraning: don\'t forgot char \'\n')
        tagorderinfo = ['git', 'tag', taginfo]
        gittaporderoutput = subprocess.Popen(tagorderinfo, stdout=subprocess.PIPE).communicate()
        if gittaporderoutput[1] is None:
            print('Pod tag version success.')
            tagpushorderinfo = ['git', 'push', 'origin', taginfo]
            gitpushorderoutput = subprocess.Popen(tagpushorderinfo, stdout=subprocess.PIPE).communicate()
            if gitpushorderoutput[1] is None:
                print('Tag order progress success.')
                print('\nPod trunk start ...')
                trunkoutput = subprocess.Popen([trunkorder], stdout=subprocess.PIPE, shell=True).communicate()
                if trunkoutput[1] is None:
                    print('Pod trunk push success.')
                else:
                    print('Pod trunk push fail.')
            else:
                print('Tag push origin fail.')
        else:
            print('Tag tag progress fail.')
    except Exception as e:
        # catch exceptions
        print('progress tag error...')
        print('error : ', e)


result = PreProgressJSONData()
AlertTupleInfo2User(result)
outselectedidx = ProgressUserInput(result)
GitProgress(result, outselectedidx)
