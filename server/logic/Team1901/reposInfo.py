# -*- coding: utf-8 -*-
import ssl
import requests
import os
import json
import pprint

repos = ['cxsjclassroom/webserver', 'octocat/Hello-World', 'apache/hive', 'apache/cassandra', 'apache/camel', 'apache/commons-lang']


def getContributorsCount(repo):
    url = 'https://api.github.com/repos/' + repo + '/stats/contributors'
    contributorsInfo = readURL('Repositories/contributors_count/%s' % repo, url)
    contributorsInfo = contributorsInfo and json.loads(contributorsInfo)

    for contributor in contributorsInfo:
        print("Contributor: %s, count:  %s \n" % (contributor['author']['login'], contributor['total']))


def getCommitsCountByCmd(name):
    gitClone(name)
    projectPath = os.path.abspath('data/gitRepo/%s' % name)  # 保存的路径
    cmd = 'git rev-list --all --count>commit.txt'
    cwd = os.getcwd()  # 记录当前目录
    os.chdir(projectPath)  # 跳转到需要保存代码库的路径
    if gitClone(name) is True:
        result = os.system(cmd)  # 执行shell命令
        os.chdir(cwd)  # 跳转回到当前目录
        return str(result)

    os.chdir(cwd)  # 跳转回到当前目录
    return False


def getRepoInfo():
    info = {}
    for repo in repos:
        repo_url = 'https://api.github.com/repos/%s' % repo  # 确定url
        repoInfo = readURL('Repositories/reposInfo/%s' % repo, repo_url)  # 访问url得到数据
        repoInfo = repoInfo and json.loads(repoInfo)  # 将数据类型转换
        branchInfo = readURL('Repositories/branchInfo/%s' % repo, repoInfo['branches_url'].replace('{/branch}', ''))
        branchInfo = branchInfo and json.loads(branchInfo)
        commitsInfo = readURL('Repositories/commitsInfo/%s' % repo, repoInfo['commits_url'].replace('{/sha}', ''))
        commitsInfo = commitsInfo and json.loads(commitsInfo)
        contributorsInfo = readURL('Repositories/commitsInfo/%s' % repo, repoInfo['contributors_url'])
        contributorsInfo = contributorsInfo and json.loads(contributorsInfo)
        # releasesInfo = readURL('Repositories/releasesInfo/%s' % repo, repoInfo['releases_url'].replace('{/id}', ''))
        # releasesInfo = releasesInfo and json.loads(releasesInfo)
        JMHurl = 'https://api.github.com/search/code?q=org.openjdk.jmh+in:file+language:java+repo:%s' % repo
        jmhInfo = readURL('Repositories/jmhInfo/%s' % repo, JMHurl)
        jmhInfo = jmhInfo and json.loads(jmhInfo)
        # getContributorsCount(repo)
        getCommitsCountByCmd(repo)
        f = open('data/gitRepo/%s/commit.txt' % repo)
        commits_counts = f.read()
        f.close()

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
            'contributors_count': len(contributorsInfo),
            # 'releases_count': len(releasesInfo),
            'commits_count': commits_counts,
            'JMH_count': jmhInfo['total_count']
        }
    gitClone(repo)
    gitLog(repo)
    gitJmh(repo)
    return info


def gitClone(name):
    projectPath = os.path.abspath('data/gitRepo/%s' % name)  # 保存的路径
    not os.path.isdir(projectPath) and os.makedirs(projectPath)
    if os.path.exists(projectPath):
        return True

    cmd = 'git clone http://github.com/%s.git %s' % (name, projectPath)
    cwd = os.getcwd()  # 记录当前目录
    os.chdir(projectPath)  # 跳转到需要保存代码库的路径
    result = os.system(cmd)  # 执行shell命令
    os.chdir(cwd)  # 跳转回到当前目录
    if result != 0:
        return False
    return True


def gitJmh(name):
    JMHurl = 'https://api.github.com/search/code?q=org.openjdk.jmh+in:file+language:java+repo:%s' % name
    jmhInfo = readURL('Repositories/jmhInfo/%s' % name, JMHurl)
    jmhInfo = jmhInfo and json.loads(jmhInfo)
    projectPath = os.path.abspath('data/gitRepo/%s' % name)
    cwd = os.getcwd()  # 记录当前目录
    os.chdir(projectPath)  # 跳转到需要保存代码库的路径
    file1 = r'jmh1.txt'
    file2 = r'jmh2.txt'
    if os.path.exists(file1) and os.path.exists(file2):
        os.remove(file1)
        os.remove(file2)
    for i, item in enumerate(jmhInfo['items']):
        cmd = 'git shortlog -s -n head %s>temp.txt ' % item['path']
        result = os.system(cmd)  # 执行shell命令
        with open('temp.txt', 'r')as fa:
            contest = fa.read()
            with open(file1, 'a+')as f:
                f.write(contest + '\n')

    os.remove('temp.txt')
    for i, item in enumerate(jmhInfo['items']):
        cmd = 'git log --pretty=format:"%h|%ce|%cd" ' + str(item['path']) + ' > temp.txt'
        result = os.system(cmd)  # 执行shell命令
        with open('temp.txt', 'r')as fb:
            contest = fb.read()
            with open(file2, 'a+')as f:
                f.write(contest + '\n')

    os.remove('temp.txt')
    os.chdir(cwd)  # 跳转回到当前目录
    return result


def gitLog(name):
    projectPath = os.path.abspath('data/gitRepo/%s' % name)  # 保存的路径
    cmd = 'git log --pretty=format:"%h -%an,%ar: %s">log.txt'
    cwd = os.getcwd()  # 记录当前目录
    os.chdir(projectPath)  # 跳转到需要保存代码库的路径
    if gitClone(name) is True:
        result = os.system(cmd)  # 执行shell命令
        os.chdir(cwd)  # 跳转回到当前目录
        return result

    os.chdir(cwd)  # 跳转回到当前目录
    return False


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
