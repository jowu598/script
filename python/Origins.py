__author__ = 'jowu'

# 0-3 versionId
# 0-7 typeId
# 0-1023 objId
# 0-15 actionId
import sys, getopt, os,  os.path,  re,  codecs
from xml.dom import minidom
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
    'gnoll', \
    # 'gnoll_blighter', \
    # 'gnoll_burner', \
    # 'gnoll_gnawer', \
    # 'gnoll_reaver', \
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
    'babyAshbite', \
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
    'catapult', \
    'ewok', \
    'reinforce' \
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

    def readAnimationPlists(self, path):
        animations = []
        for f in os.listdir(path):
            formatName = f[f.rfind('.') + 1:]
            if ('animation' not in f):
                continue;
            if ('plist' != formatName):
                continue;
            name = os.path.join(path, f)
            out = readPlist(name)
            actions = out['animations']
            for action in actions:
                #print ("formIndex %d toIndex %d prefix %s" %(action['fromIndex'], action['toIndex'], action['prefix']))
                # is enemy ?
                ret = self.checkType(action)
                print action + "=" + ret
                # print ("%s is  %s", %(action ret))
            animations.append(actions)
        return animations

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

    def scanFolderForActions(self, path, animations):
        targetPath = "C:\Animations"
        for f in os.listdir(path):
            sourceF = os.path.join(path, f)
            if os.path.isdir(sourceF):
                acts = self.getActionsWithGivenFolder(sourceF)
                for act in acts:
                    print act
                    targetFolder = os.path.join(targetPath, f)
                    if not os.path.exists(targetFolder):
                        os.mkdir(targetFolder)
                    if act in animations:
                        # move all png to animations floder
                        cmd = 'mv'
                        cmd += act
                        cmd += "* "
                        cmd += targetFolder
                        print cmd
                    #print act
            print "=============================================" + path




    def detachAnimationFromRes(self):
        print('detachAnimationFromRes')



if __name__ == '__main__':
    path = "E:\Origins"
    # test xml filter
    # xf = XmlFilter();
    # xf.extractEnemyNameFromWaves(path)

    # test plist reader
    pr = PListReader();
    animations = pr.readAnimationPlists(path)
    pr.scanFolderForActions("C:\Images", animations)