#-*- coding: utf-8 -*-

from app import route, response, redirect, config

import logic.Team1901.reposInfo as a
repos = ['cxsjclassroom/webserver',"octocat/Hello-World"]

@route('/hello.py.html')
def projectInfo():
    info = a.getRepoInfo()
#将info返回给页面
    return response(projectInfo=info)

#显示部分信息的新界面
@route('/diy.py.html')
def diyInfo():
    info = a.getRepoInfo()
    return response(projectInfo=info)


@route('/commits.py.html')
def commits():
    info = a.getRepoInfo()
#将info返回给页面
    return response(projectInfo=info)
