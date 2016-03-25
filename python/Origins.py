#!/usr/bin/python
__author__ = 'jowu'

# 0-3 versionId
# 0-7 typeId
# 0-1023 objId
# 0-15 actionId
import sys, getopt, os,  os.path,  re,  codecs
from xml.dom import minidom
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import xml.dom.minidom
from biplist import *

s_enmyeName = \
[
    'arachnomancer_miniSpider', \
    'arachnomancer_spider', \
    'arachnomancer', \
    'bandersnatch', \
    'bloodServant', \
    'bloodsydianGnoll', \
    'bloodsydianWarlock', \
    'zealot', \
    'dark_spitters', \
    'drider', \
    'ettin', \
    'fungusRider_medium', \
    'fungusRider_small', \
    'fungusRider', \
    'gloomy', \
    'gnoll_blighter', \
    'gnoll_burner', \
    'gnoll_gnawer', \
    'gnoll_reaver', \
    'gollem', \
    'grim_devourers', \
    'harraser', \
    'hyena', \
    'knocker', \
    'mantaray', \
    'gnollBerzerker', \
    'mountedAvenger', \
    'ogre_mage', \
    'perython', \
    'rabbit', \
    'razorboar', \
    'redcap', \
    'satyrHoplite', \
    'satyr', \
    'scourger', \
    'scourger_shadow', \
    'screecher_bat', \
    'shadow_champion', \
    'shadow_spawn', \
    'son_of_mactans', \
    'sword_spider', \
    'tarantula', \
    'theBeheader', \
    'twilight_avenger', \
    'twilight_bannerbearer', \
    'twilight_evoker', \
    'twilight_heretic', \
    'webspitterSpider', \
]

s_towerName = \
[
    'archer', \
    'artillery_henge', \
    'artillery_thrower', \
    'artillery_tree', \
    'mage', \
    'barrack', \
    'forest', \
    'bladeSinger' \
    'stun_big', \
    'stun_small' \
]

s_allyName = \
[
    'roadRunner',
    'pixie', \
    'mercenary_draw', \
    'ewok', \
    'reinforce', \
    'rabbit', \
    # 'bladeSinger', \
    # 'forestKeeper', \
    # 'barrack_soldier', \
    # 'artillery_henge_bear', \
    'babyAshbite', \
    'reinforce', \
    # 'reinforce_A1', \
    # 'reinforce_A2', \
    # 'reinforce_A3', \
    # 'reinforce_B0', \
    # 'reinforce_B1', \
    # 'reinforce_B2', \
    # 'reinforce_B3', \
    # 'reinforce_C0', \
    # 'reinforce_C1', \
    # 'reinforce_C2', \
    # 'reinforce_C3', \
]

s_heroName = \
[
    'archer_hero', \
    'bravebark', \
    'alleria', \
    'arivan', \
    'bolverk', \
    'bruce', \
    'denas', \
    'durax', \
    'regson', \
    'fallen_angel', \
    'faustus', \
    'lynn', \
    'xin', \
    'phoenix', \
    'catha', \
    'razzAndRaggs', \
    'veznan', \
    'wilburg', \
    'malik' \
]

s_bossName = [
    'hee-haw', \
    'malicia', \
    'bajnimen', \
    'ainyl', \
    'boss_godieth', \
    'bossHiena', \
    'drow_queen', \
    'spiderQueen' \
    'boss_godieth' \
    'theBeheader' \
]

class  XmlFilter:
    def __init__(self):
        print("--XmlFilter--")
        self.enemyNames = []
    def isExist(self, name):
        for n in self.enemyNames:
            #print ("%s vs %s" %(n, name));
            if (n == name):
                return True

    def addEnemy(self, file):
        dom = minidom.parse(file)
        #print file
        creeps = dom.getElementsByTagName("creep")
        for creep in creeps:
            if not self.isExist(creep.childNodes[0].data):
                self.enemyNames.append(creep.childNodes[0].data)

    def extractEnemyNameFromWaves(self, path):
        for f in os.listdir(path):
            formatName = f[f.rfind('.') + 1:]
            #print formatName
            if ('heroic' in f):
                continue;
            if ('xml' != formatName):
                continue;
            file = os.path.join(path, f)
            self.addEnemy(file)
        for name in self.enemyNames:
            print name


    def generateAnimationId(self):
        doc = minidom.parse('animation.xml')
        for child in doc.childNodes:
            print child

class PListReader:
    def __init__(self):
        print('--PListFilter--')

    def checkType(self, name):
        for enemy in s_enmyeName:
            if ( enemy in name):
                return "ENEMY"
        for hero in s_heroName:
            if (hero in name):
                return "HERO"
        for tower in s_towerName:
            if (tower in name):
                return "TOWER"
        for ally in s_allyName:
            if (ally in name):
                return "ALLY"
        for boss in s_bossName:
            if (boss in name):
                return "BOSS"
        return "COMMON"

    def extractPrefix(self, path):
        prefixs = []
        for f in os.listdir(path):
            formatName = f[f.rfind('.') + 1:]
            if ('animation' not in f):
                continue;
            if ('plist' != formatName):
                continue;
            name = os.path.join(path, f)
            plistAnimation = readPlist(name)
            regPrefix='\'prefix\': \'([a-zA-Z-_0-9]+)\''
            reobj = re.compile(regPrefix)
            out = reobj.findall(str(plistAnimation))
            
            unsetOut = set(out)
            for prefix in unsetOut:
                prefixs.append(prefix)
        return set(prefixs)

    def extractAnimationID(self, path):
        doc = Document()
        xmlRoot = doc.createElement('animations')
        doc.appendChild(xmlRoot)
        for f in os.listdir(path):
            formatName = f[f.rfind('.') + 1:]
            if ('animation' not in f):
                continue;
            if ('plist' != formatName):
                continue;
            name = os.path.join(path, f)
            plistAnimation = readPlist(name)
            animationDict = plistAnimation['animations']

            for (animation, info) in animationDict.items():
                print "animation name: " + animation
                print info
                animationNode = doc.createElement('animation')
                descriptNode = doc.createElement('descript')
                prefixNode = doc.createElement('prefix')
                toIndexNode = doc.createElement('toIndex')
                fromIndexNode = doc.createElement('fromIndex')
                catagoryNode = doc.createElement('catagory')

                descript = doc.createTextNode(animation)
                prefix = doc.createTextNode(info['prefix'])
                catagory = doc.createTextNode(self.checkType(animation))
                if (info.has_key('fromIndex') and info.has_key('toIndex')):
                    fromIndex = doc.createTextNode(str(info['fromIndex']))
                    toIndex = doc.createTextNode(str(info['toIndex']))
                    print "prefix: " + info['prefix'] + ", fromIndex: " + str(info['fromIndex']) + ", toIndex: " + str(info['toIndex'])
                else:
                    fromIndex = doc.createTextNode('-1')
                    toIndex = doc.createTextNode('-1')
                    print "=============================================================================="

                animationNode.appendChild(prefixNode)
                animationNode.appendChild(descriptNode)
                animationNode.appendChild(toIndexNode)
                animationNode.appendChild(fromIndexNode)
                animationNode.appendChild(catagoryNode)

                prefixNode.appendChild(prefix)
                descriptNode.appendChild(descript)
                toIndexNode.appendChild(toIndex)
                fromIndexNode.appendChild(fromIndex)
                catagoryNode.appendChild(catagory)

                xmlRoot.appendChild(animationNode)

            f = open('animation.xml', 'w')
            f.write(doc.toprettyxml(indent= ''))
            f.close()


    def getActionsWithGivenFolder(self, path):
        if not os.path.exists(path):
            print ("path not exists !!!!")
            return
        reg = "_[0-9]{4}.png";
        actions = []
        for f in os.listdir(path):
            sourceF = os.path.join(path, f)
            if os.path.isfile(sourceF) and re.search(reg, f):
                #print sourceF[0 : sourceF.rfind('_')]
                actions.append(f[0 : f.rfind('_')])
        return set(actions)

    def splitsImageFormAnimation(self, tdRes, path, targetPath):
        prefixs = pr.extractPrefix(tdRes)
        for f in os.listdir(path):
            sourceF = os.path.join(path, f)
            if os.path.isdir(sourceF):
                acts = self.getActionsWithGivenFolder(sourceF)
                for act in acts:
                    print act
                    targetFolder = os.path.join(targetPath, f)
                    if not os.path.exists(targetFolder):
                        os.mkdir(targetFolder)

                    if act in prefixs:
                        # move all png to animations floder
                        cmd = 'mv '
                        cmd += sourceF + "/"
                        cmd += act;
                        cmd += "* "
                        cmd += targetFolder
                        print "cmd is :" + cmd
                        os.system(cmd)

                    
                    #     # move all png to animations floder
                    #     cmd = 'cp '
                    #     cmd += sourceF + "/"
                    #     cmd += act;
                    #     cmd += "* "
                    #     cmd += targetFolder
                    #     print "cmd is :" + cmd
                        #os.system(cmd)
                    #print act
            print "=============================================" + path + "====" + f  

    def detachAnimationFromRes(self):
        print('detachAnimationFromRes')




if __name__ == '__main__':
    #imagepath = "E:\Origins"
    #targetPath = "C:\Animations"
    tdRes = "/Users/jowu/workspace/TowerDefense/Resources"
    imagepath = "/Users/jowu/Documents/Images"
    targetPath = "/Users/jowu/Documents/Animations"
    # test xml filter
    xf = XmlFilter();
    # xf.extractEnemyNameFromWaves(path)

    # plist reader
    pr = PListReader();
    # splite animation
    #pr.splitsImageFormAnimation(tdRes, imagepath, targetPath)
    # extract id
    #pr.extractAnimationID(tdRes)

    xf.generateAnimationId();




