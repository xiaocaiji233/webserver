#-*- coding: utf-8 -*-
import ssl
import requests
import os
import json
import pprint

repos = ['cxsjclassroom/webserver',"octocat/Hello-World"]

def getRepoInfo():
    info = {}
    for repo in repos:
        repo_url = 'https://api.github.com/repos/%s' % repo  # 确定url
        repoInfo = readURL('Repositories/reposInfo/%s' % (repo), repo_url)  # 访问url得到数据
        repoInfo = repoInfo and json.loads(repoInfo)  # 将数据类型转换
        branchInfo = readURL('Repositories/branchInfo/%s' % (repo), repoInfo['branches_url'].replace('{/branch}', ''))
        branchInfo = branchInfo and json.loads(branchInfo)
        pprint.pprint(branchInfo)
        commitsInfo = readURL('Repositories/commitsInfo/%s' % (repo), repoInfo['commits_url'].replace('{/sha}', ''))
        commitsInfo = commitsInfo and json.loads(commitsInfo)
        pprint.pprint(commitsInfo)

        # 提取想要的信息保存在info中
        info[repo] = {
            "stargazers_count": repoInfo['stargazers_count'],
            'watchers_count': repoInfo['watchers_count'],
            'created_at': repoInfo['created_at'],
            'size': repoInfo['size'],
            'forks_count': repoInfo['forks_count'],
            'open_issues': repoInfo['open_issues'],
            'branches': list(branchInfo),
            'branches_count': len(branchInfo),
            'branches_name': list(map(lambda b: b['name'], branchInfo)),
            'commits': commitsInfo,
            'commits_count': len(commitsInfo),

        }
    return info
# 读取url的信息，并建立缓存
def readURL(cache, url):
# 看看该url是否访问过
    cache = 'data/cache/%s' % cache
    if os.path.isfile(cache):
      with open(cache, 'r') as f:
        content = f.read()
      return content

    content = requests.get(url).content.decode()

# 把文件内容保存下来，以免多次重复访问url，类似于缓存
    folder = cache.rpartition('/')[0]
    not os.path.isdir(folder) and os.makedirs(folder)
    with open(cache, 'w') as f:
      f.write(content)
    return content

