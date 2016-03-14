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
    'forestKeeper', \
    'bladeSinger' \
]

s_allyName = \
[
    'catapult', \
    'ewok', \
    'reinforce' \
    ''
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

    def readAnimationPlists(self, path):
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
                print (action)
                #print ("formIndex %d toIndex %d prefix %s" %(action['fromIndex'], action['toIndex'], action['prefix']))





if __name__ == '__main__':
    path = "E:\Origins"
    # test xml filter
    # xf = XmlFilter();
    # xf.extractEnemyNameFromWaves(path)

    # test plist reader
    pr = PListReader();
    # pr.readAnimationPlists(path)