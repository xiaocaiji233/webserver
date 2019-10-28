#-*- coding: utf-8 -*-

from app import route, response, redirect, config

import logic.Team1901.reposInfo as a
repos = ['cxsjclassroom/webserver',"octocat/Hello-World"]
@route('/hello.py.html')

def projectInfo(cookies):
    info = a.getRepoInfo()
#将info返回给页面
    return response(projectInfo=info)



