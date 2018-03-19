# -*- coding: utf-8 -*-  
'''
Created on 2017年3月17日

@author: sujingqiao
'''
import pdb
import traceback
import copy
import sys
from utils.util import Util
from _abcoll import Set
from configs  import config
sys.setrecursionlimit(10000)
import logging
import collections
from itertools import combinations as COMB

WAN = 0

TONG = 1

TIAO = 2

FENG = 3

class MaJiang():
    
    def __init__(self):
        #整扑状态
        self.zheng_pu_status = [0,0,0,0]
        #赖子数
        self.lai_zi_count = 0
        #
        self.is_258_jiang = False
        
        self.is_bu_3_tiao = False

        self.is_bu_zfb = False
        
        self.is_13_yao = False

        self.check_kan = False
        
        self.four_a_count = 0
        
        self.wan_list =[]
        
        self.tong_list = []
        
        self.tiao_list = []
        
        self.feng_list = []
        
        self.resultMap = set()
        
        self.isHuRenYi = False
        
        self.curCalcType = -1
        
        self.wanResultList = []
        
        self.tongResultList = []
        
        self.tiaoResultList = []
        
        self.fengResultList = []
        
        self.chiPaiList = []
        
        self.pengPaiList = []
        
        self.gangPaiList = []
        
        self.anGangPaiList = []
        
        self.shengPaiList = []
    
        self.menqing = False

        self.subs = []

        self.lcnt = 0

        self.orig = None

        self.kanCtx = []
    
    def clean(self):
        #整扑状态
        self.zheng_pu_status = [0,0,0,0]
        #赖子数
        self.lai_zi_count = 0
        #
        self.is_258_jiang = False
        
        self.is_258_ying_jiang = False
        
        self.is_bu_3_tiao = False

        self.is_bu_zfb = False
        
        self.is_13_yao = False
        
        self.check_kan = False

        self.four_a_count = 0
        
        self.wan_list =[]
        
        self.tong_list = []
        
        self.tiao_list = []
        
        self.feng_list = []
        
        self.resultMap = set()
        
        self.isHuRenYi = False
        
        self.curCalcType = -1
        
        self.wanResultList = []
        
        self.tongResultList = []
        
        self.tiaoResultList = []
        
        self.fengResultList = []
        
        self.chiPaiList = []
        
        self.pengPaiList = []
        
        self.gangPaiList = []
        
        self.anGangPaiList = []
        
        self.shengPaiList = []

        self.menqing = False

        self.subs = []

        self.lcnt = 0

        self.orig = None
        
        self.kanCtx = []

    def dump(self, fname=''):
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        logging.info(fname + ' -> MaJiang.DUMP  {} {} {} {}'.format(self.lai_zi_count,
                       tiles, self.is_bu_zfb, self.is_258_jiang))

    def set_lai_zi_count(self, lai_shu):
        """
        #设置赖子数
        """
        self.lai_zi_count = lai_shu
        
    def addChiPai(self,  value) :
        self.chiPaiList = value


    def addPengPai(self,  value) :
        self.pengPaiList = value

    def addGangPai(self,  value) :
        self.gangPaiList = value 
        
    def addAnGangPai(self,  value) :
        self.anGangPaiList = value 
        
    def set_bu_3_tiao(self, bu_3_tiao):
        """
        #设置赖子数
        """
        self.is_bu_3_tiao = bu_3_tiao

    def set_is_13_yao(self, isyao):
        self.is_13_yao = isyao
        
    def set_bu_zfb(self, isbu):
        """
        #设置中发白可吃
        """
        self.is_bu_zfb = isbu
        
    def set_is_258_jiang(self, status):
        """
        #设置258将
        """
        self.is_258_jiang = status
        
    def set_is_258_ying_jiang(self, status):
        """
        #设置258硬将
        """
        self.is_258_ying_jiang = status

    def set_check_kan(self, status):
        self.check_kan = status

    def check_zfb_bu(self, paiId):
        if not self.is_bu_zfb:
            return False

        if not (paiId >= 35 and paiId <= 37):
            return False
        
        return True
        
    def quFourPai(self, _list):
        a_list = copy.copy(_list)
        four_a_count = 0
        for a in a_list :
            if _list.count(a) == 4 :
                _list.remove(a)
                _list.remove(a)
                _list.remove(a)
                _list.remove(a)
                four_a_count += 1
        return four_a_count, _list
        

    def countOver4(self, paiId, pais):
        tmp = self.wan_list + self.tiao_list + self.tong_list + self.feng_list 
        tmp += [paiId] + pais
        if tmp.count(paiId) > 4:
            return True
        else:
            return False 
        
    def get_qidui_type(self, paiId, laizi):
        logging.info('get_qidui_type: ENTER {} {} {}'.format(paiId, laizi, self.lai_zi_count))

        pais = self.wan_list + self.tiao_list + self.tong_list + self.feng_list 
        if (len(pais) + self.lai_zi_count) < 13:
            return False, None

        if paiId != laizi:
            pais.append(paiId) 
        else:
            self.lai_zi_count += 1

        pai_info = collections.Counter(pais)
        counter = [[],[],[],[]]
        for paiId, cnt in pai_info.items():
            counter[cnt-1].append(paiId)

        logging.info('get_qidui_type: {} {} {}'.format(self.lai_zi_count, pais, counter))
        if (len(counter[2]) + len(counter[0])) > self.lai_zi_count:
            return False, None

        self.four_a_count = len(counter[3])
        self.four_a_count += len(counter[2])
        self.lai_zi_count -= len(counter[2])
        self.lai_zi_count -= len(counter[0])
        assert(self.lai_zi_count%2 == 0)
        self.four_a_count += min(len(counter[1])+len(counter[0]), self.lai_zi_count/2) 
        logging.info('get_qidui_type: four_a_count= {}'.format(self.four_a_count))

        count = len(counter[3])
        if count == 3 :
            return True, config.CHAO_SHUANG_HAO_HUA_QI_XIAO_DUI
        elif count == 2 :
            return True, config.CHAO_HAO_HUA_QI_XIAO_DUI
        elif count == 1 :
            return True, config.HAO_HUA_QI_XIAO_DUI
        else:
            return True, config.QI_XIAO_DUI

    def check_hao_qidui(self, paiId, laizi):
        ok, typeid = self.get_qidui_type(paiId, laizi)
        if ok and typeid != config.QI_XIAO_DUI:
            return True
        return False

    def isHu7Dui(self) :
        self.shengPaiList = []
        if len(self.chiPaiList) > 0 or len(self.pengPaiList) > 0 or len(self.gangPaiList) > 0 or len(self.anGangPaiList) > 0 : 
            return False
        self.four_a_count = 0
        
        four_wan_count, wan_list2 = self.quFourPai(copy.copy(self.wan_list))
        four_tiao_count, tiao_list2 = self.quFourPai(copy.copy(self.tiao_list))
        four_tong_count, tong_list2 = self.quFourPai(copy.copy(self.tong_list))
        four_feng_count, feng_list2 = self.quFourPai(copy.copy(self.feng_list))
        
        self.four_a_count = four_wan_count + four_tiao_count + four_tong_count + four_feng_count
        
        danWan = self.quDui(wan_list2)
        danTiao = self.quDui(tiao_list2)
        danTong = self.quDui(tong_list2)
        danFen = self.quDui(feng_list2)
        if danWan + danTiao + danTong + danFen <= 1 and self.lai_zi_count == 4 :
                self.four_a_count += 1
        m_types = {}
        qing_yi_se = Util.check_qing_yi_se(self.wan_list + self.tiao_list + self.tong_list + self.feng_list)
        aaa_list = Util.getPaiAAA(self.wan_list + self.tiao_list + self.tong_list + self.feng_list)
        m_isting = False 
        if (danWan + danTiao + danTong + danFen < self.lai_zi_count + 1 ) or (danWan + danTiao + danTong + danFen == self.lai_zi_count + 1) :
            m_isting = True
            if danWan + danTiao + danTong + danFen < self.lai_zi_count + 1 :
                m_types[config.QI_XIAO_DUI] = [True, []]
            elif danWan + danTiao + danTong + danFen == self.lai_zi_count + 1 :
                m_types[config.QI_XIAO_DUI] = [False, self.shengPaiList]
            if len(aaa_list) > 0 :
                    m_types[config.HAO_HUA_QI_XIAO_DUI] = [False, aaa_list]
            if self.four_a_count == 1 :
                if self.lai_zi_count == 4 and danWan + danTiao + danTong + danFen < self.lai_zi_count + 1 : 
                    m_types[config.HAO_HUA_QI_XIAO_DUI] = [True, []]
                m_types[config.HAO_HUA_QI_XIAO_DUI] = [False, self.shengPaiList]
                if len(aaa_list) > 0 :
                    m_types[config.SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, aaa_list]
            elif self.four_a_count == 2 :
                if self.lai_zi_count == 4 and danWan + danTiao + danTong + danFen < self.lai_zi_count + 1 : 
                    m_types[config.HAO_HUA_QI_XIAO_DUI] = [True, []]
                m_types[config.SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, self.shengPaiList]
                if len(aaa_list) > 0 :
                    m_types[config.CHAO_SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, aaa_list]
            elif self.four_a_count == 3 :
                if self.lai_zi_count == 4 and danWan + danTiao + danTong + danFen < self.lai_zi_count + 1 :
                    m_types[config.CHAO_SHUANG_HAO_HUA_QI_XIAO_DUI] = [True, []]
                m_types[config.CHAO_SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, self.shengPaiList]
            
            if qing_yi_se > 0 :
                qingPaiList = []
                if qing_yi_se == 1 :
                    qingPaiList = [1,2,3,4,5,6,7,8,9]
                elif qing_yi_se == 2 :
                    qingPaiList = [11,12,13,14,15,16,17,18,19]
                elif qing_yi_se == 3 :
                    qingPaiList = [21,22,23,24,25,26,27,28,29]
                    
                m_types[config.QING_QI_XIAO_DUI] = [False, self.shengPaiList]
                m_hu_pai = []
                for a in qingPaiList :
                    if a in self.shengPaiList :
                        m_hu_pai.append(a)
                if len(aaa_list) > 0 :
                    m_types[config.QING_HAO_HUA_QI_XIAO_DUI] = [False, aaa_list]
                    
                if self.four_a_count == 1 :
                    m_types[config.QING_HAO_HUA_QI_XIAO_DUI] = [False, m_hu_pai]
                    if len(aaa_list) > 0 :
                        m_types[config.QING_SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, aaa_list]
                elif self.four_a_count == 2 :
                    if len(aaa_list) > 0 :
                        m_types[config.QING_CHAO_SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, aaa_list]
                    if self.lai_zi_count == 4 and danWan + danTiao + danTong + danFen < self.lai_zi_count + 1 : 
                        m_types[config.QING_HAO_HUA_QI_XIAO_DUI] = [True, []]
                    m_types[config.QING_SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, m_hu_pai]
                elif self.four_a_count == 3 :
                    if self.lai_zi_count == 4 and danWan + danTiao + danTong + danFen < self.lai_zi_count + 1 : 
                        m_types[config.QING_SHUANG_HAO_HUA_QI_XIAO_DUI] = [True, []]
                    m_types[config.QING_CHAO_SHUANG_HAO_HUA_QI_XIAO_DUI] = [False, m_hu_pai]
        return m_isting, m_types
        
        
        
    def quDui(self, _list) :
        count = len(_list)
        if count <= 0 : 
            return 0
        isHaveDui = False
        _list.sort()
        pai = 0
        index = 0
        for p in _list :
            if index + 1 != len(_list) and p == _list[index + 1] :
                isHaveDui = True
                pai = p
                break
            index += 1

        if isHaveDui : 
            _list.remove(pai)
            _list.remove(pai)
            return self.quDui(_list)
        else :
            self.shengPaiList += _list
            return count
        
    def set_pais(self, psi_list):
        for paiId in psi_list :
            if paiId > 0 and paiId < 10 :
                self.wan_list.append(paiId)
            elif paiId > 10 and paiId < 20 :
                self.tong_list.append(paiId)
            elif paiId > 20 and paiId < 30 :
                self.tiao_list.append(paiId)
            elif paiId > 30 and paiId < 40 :
                self.feng_list.append(paiId)
        #排序
        self.wan_list.sort()
        self.tong_list.sort()
        self.tiao_list.sort()
        self.feng_list.sort()
        #设置整扑状态

        if (len(self.wan_list)+len(self.tong_list)+len(self.tiao_list)
            +len(self.feng_list) >= 13):
            self.menqing = True

        if self.check_zheng_pu(self.wan_list) :
            self.zheng_pu_status[WAN] = 1
        if self.check_zheng_pu(self.tong_list) :
            self.zheng_pu_status[TONG] = 1
        if self.check_zheng_pu(self.tiao_list) :
            self.zheng_pu_status[TIAO] = 1
        if self.check_zheng_pu(self.feng_list) :
            self.zheng_pu_status[FENG] = 1

    def get_simple_paiId(self, laizi=0):
        if self.zheng_pu_status[WAN] == 0: 
            return self.wan_list.pop(-1)
        if self.zheng_pu_status[TONG] == 0: 
            return self.tong_list.pop(-1)
        if self.zheng_pu_status[TIAO] == 0: 
            return self.tiao_list.pop(-1)
        if self.zheng_pu_status[FENG] == 0:
            return self.feng_list.pop(-1)

        if self.zheng_pu_status[WAN] == 1 and len(self.wan_list) > 0:
            return self.wan_list.pop(-1)
        if self.zheng_pu_status[TONG] == 1 and len(self.tong_list) > 0:
            return self.tong_list.pop(-1)
        if self.zheng_pu_status[TIAO] == 1 and len(self.tiao_list) > 0:
            return self.tiao_list.pop(-1)
        if self.zheng_pu_status[FENG] == 1 and len(self.feng_list) > 0:
            return self.feng_list.pop(-1)
        # 手牌只有癞子， 一定胡了
        return laizi
        
    def check_zheng_pu(self, _list):
        _list.sort()
        if len(_list) % 3 == 0 :
            pai_list = copy.copy(_list)
            return self.qu_zheng_pu(pai_list)
        else :
            return False
        
    def qu_zheng_pu(self, pai_list):
        if len(pai_list) == 0 :
            return True
        else :
            if Util.check_AAA(pai_list[:3]) :
                pai_list = Util.del_paiList(pai_list[:3], pai_list)
                return self.qu_zheng_pu(pai_list)
            else :
                if pai_list[0] < 30 and self.is_bu_3_tiao == False : #判断是否为风 
                    if pai_list[0] + 1 in pai_list and pai_list[0] + 2 in pai_list : #ABC
                        pai_list = Util.del_paiList([pai_list[0], pai_list[0] + 1,pai_list[0] + 2], pai_list)
                        return self.qu_zheng_pu(pai_list)

        return False
 
    def dedup(self, alist):
        res = []
        for r in alist:
            if sorted(r) not in res:
                res.append(sorted(r))
        
        logging.info('dedup:{} {} '.format(alist, res))
        return res

    def encode(self, alist):
        res1 = set()
        for r in alist:
            sp =''
            for pid in sorted(r):
                logging.info('ENC {} {} {} '.format(r, pid, alist))
                
                sp += '%02d'%pid
            res1.add(sp)
        return res1

    def encode1(self, tl):
        sp = ''
        for pid in tl:
            sp += '%02d'%pid
        return sp

    def get_optim_repls(self, td, varg=None):#typedict

        logging.info('get_optim_repls:enter {} loop {} '.format(varg, td))
        self.optim = {}
        self.optim['max'] = 0
        self.optim['fanxin'] ={}
        at = []

        for t in td.values():
            for tt in t:
                at.append(tt)

        for a in at:
            val = 0
            tmp = set()
            for k, tds in td.items():
                if a in tds and k[0] not in tmp:
                    val += k[1]
                    tmp.add(k[0])
            if val > self.optim['max']:
                self.optim['max'] = val
                self.optim['fanxin'] ={}
            if val >= self.optim['max']:
                self.optim['fanxin'][self.encode1(a)] = tmp 
         
        logging.info('get_optim_repls:finally {} loop {} '.format(varg, self.optim))
        return self.optim 

    def not_feng(self, paiId):
        '''
        if not self.is_bu_zfb:
           return False
        '''
        return paiId not in [31,32,33,34]

    def chou_jiang(self, _type):
        self.curCalcType = _type
        self.wanResultList = []
        self.tongResultList = []
        self.tiaoResultList = []
        self.fengResultList = []
        if self.zheng_pu_status[_type] == 0 or self.is_258_jiang :
            pai_list = []
            if _type == WAN :
                pai_list = copy.copy(self.wan_list)
            elif _type == TONG :
                pai_list = copy.copy(self.tong_list)
            elif _type == TIAO :
                pai_list = copy.copy(self.tiao_list)
            elif _type == FENG :
                pai_list = copy.copy(self.feng_list)
            else :
                return False
            jiang = 0
            index = 0
            for paiId in pai_list :
                _state = True
                if self.is_258_jiang :
                    _state =  paiId < 30 and (paiId % 10 == 2 or paiId % 10 == 5 or paiId % 10 == 8)
                if paiId != jiang and _state :
                    jiang = paiId
                    bupai_list = []
                    if len(pai_list) > index + 1 and pai_list[index + 1] == jiang :
                        pai_list1 = copy.copy(pai_list)
                        pai_list2 = Util.del_paiList([pai_list1[index], pai_list1[index + 1]], pai_list1)
                        self.startCalc(pai_list2, bupai_list)
                    else :
                        pai_list1 = copy.copy(pai_list)
                        pai_list2 = Util.del_paiList([jiang], pai_list1)
                        bupai_list.append(jiang)
                        self.startCalc(pai_list2, bupai_list)
                index += 1
            return True
        else :
            return False

    def chou3tiao(self, _list, bupai_list):
        pai_list = copy.copy(_list)
        if Util.check_AAA(pai_list[:3]) :
            pai_list = Util.del_paiList(pai_list[:3], pai_list)
            self.startCalc(pai_list, bupai_list)

     
    def choulong(self, _list, bupai_list): 
        pai_list = copy.copy(_list)
        if pai_list[0] < 30 : #判断是否为风 
            if pai_list[0] + 1 in pai_list and pai_list[0] + 2 in pai_list : #ABC
                pai_list = Util.del_paiList([pai_list[0], pai_list[0] + 1,pai_list[0] + 2], pai_list)
                self.startCalc(pai_list, bupai_list)
                
    def jian1(self, _list, bupai_list):
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list)
        if pai_list[0] + 2 in pai_list :
            bupai_list1.append(pai_list[0] + 1)
            pai_list = Util.del_paiList([pai_list[0],pai_list[0] + 2], pai_list)
            self.startCalc(pai_list, bupai_list1)
    
    def zuobu1(self, _list, bupai_list):
        pai_list = copy.copy(_list) 
        bupai_list1 = copy.copy(bupai_list)
        if pai_list[0] % 10 != 1 and pai_list[0] + 1 in pai_list :
            bupai_list1.append(pai_list[0] - 1)
            pai_list = Util.del_paiList([pai_list[0],pai_list[0] + 1], pai_list)
            self.startCalc(pai_list, bupai_list1)
        
    def youbu1(self, _list, bupai_list):
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list) 
        if pai_list[0] % 10 < 8 and pai_list[0] + 1 in pai_list :
            bupai_list1.append(pai_list[0] + 2)
            pai_list = Util.del_paiList([pai_list[0],pai_list[0] + 1], pai_list)
            self.startCalc(pai_list, bupai_list1)
                   
    def buYuanZhang(self, _list, bupai_list):
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list)
        paiID = pai_list[0]
        pai_list = Util.del_paiList([paiID], pai_list)
        if paiID in pai_list :
            bupai_list1.append(paiID)
            pai_list = Util.del_paiList([paiID], pai_list)
            self.startCalc(pai_list, bupai_list1)
    
    def zuobu2(self, _list, bupai_list):
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list) 
        if pai_list[0] % 10 >= 3 :
            bupai_list1.append(pai_list[0] - 1)
            bupai_list1.append(pai_list[0] - 2)
            pai_list = Util.del_paiList([pai_list[0]], pai_list)
            self.startCalc(pai_list, bupai_list1)
        
    def youbu2(self, _list, bupai_list):
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list) 
        if pai_list[0] % 10 < 8 :
            bupai_list1.append(pai_list[0] + 1)
            bupai_list1.append(pai_list[0] + 2)
            pai_list = Util.del_paiList([pai_list[0]], pai_list)
            self.startCalc(pai_list, bupai_list1)
            
    def zuoyoubu2(self, _list, bupai_list):
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list) 
        if pai_list[0] % 10 < 9 and pai_list[0] % 10 > 1 :
            bupai_list1.append(pai_list[0] + 1)
            bupai_list1.append(pai_list[0] - 1)
            pai_list = Util.del_paiList([pai_list[0]], pai_list)
            self.startCalc(pai_list, bupai_list1)    
                   
    def buYuanZhang2(self, _list, bupai_list):
        pai_list = copy.copy(_list) 
        bupai_list1 = copy.copy(bupai_list)
        paiID = pai_list[0]
        pai_list = Util.del_paiList([paiID], pai_list)
        bupai_list1.append(paiID)
        bupai_list1.append(paiID)
        self.startCalc(pai_list, bupai_list1)
                    
    def calc(self, _list, bupai_list): 
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list)
        if len(pai_list) < 3 :
            return 
        else :
            self.chou3tiao(pai_list, bupai_list1)
            if self.is_bu_3_tiao == False :
                self.choulong(pai_list, bupai_list1)
        
    def calc1(self, _list, bupai_list): 
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list) 
        if len(pai_list) < 2 :
            return 
        else :
            if pai_list[0] < 30 and self.is_bu_3_tiao == False : #判断是否为风 
                self.jian1(pai_list, bupai_list1)
                self.zuobu1(pai_list, bupai_list1)
                self.youbu1(pai_list, bupai_list1)
            self.buYuanZhang(pai_list, bupai_list1)
        
    def calc2(self, _list, bupai_list):         
        pai_list = copy.copy(_list)
        bupai_list1 = copy.copy(bupai_list)   
        if pai_list[0] < 30 and self.is_bu_3_tiao == False : #判断是否为风 
            self.zuobu2(pai_list, bupai_list1)
            self.youbu2(pai_list, bupai_list1)
            self.zuoyoubu2(pai_list, bupai_list1)
        self.buYuanZhang2(pai_list, bupai_list1) 
                     
    def startCalc(self, _list, bupai_list): 
        if len(_list) <= 0 :
            if self.curCalcType == WAN :
                self.wanResultList.append(bupai_list)
            elif self.curCalcType == TONG :
                self.tongResultList.append(bupai_list)
            elif self.curCalcType == TIAO :
                self.tiaoResultList.append(bupai_list)
            elif self.curCalcType == FENG :
                self.fengResultList.append(bupai_list)
            else :
                return False
        else :
            self.calc(_list, bupai_list)
            if len(bupai_list) + 1 <= self.lai_zi_count + 1 :
                self.calc1(_list, bupai_list)
            if len(bupai_list) + 2 <= self.lai_zi_count + 1 :
                self.calc2(_list, bupai_list)
                
    def check_ting(self):
        
        self.resultMap = set()
        isTing = False
        self.isHuRenYi = False
        bupai_list = []
        tmp_wanResultList = []
        tmp_tongResultList = []
        tmp_tiaoResultList = []
        tmp_fengResultList = []
        #都是整扑 多余的牌是癞子
        if self.is_258_jiang != True and self.lai_zi_count >= 1 :
            if self.zheng_pu_status[WAN] == 1 and \
                self.zheng_pu_status[TONG] == 1 and \
                self.zheng_pu_status[TIAO] == 1 and \
                self.zheng_pu_status[FENG] == 1 :
                self.isHuRenYi = True
                return True
        if True :
            bupai_list = []
            if self.zheng_pu_status[WAN] == 0 :
                self.curCalcType = WAN
                self.startCalc(self.wan_list, bupai_list)
            else :
                self.wanResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[TONG] == 0 :
                self.curCalcType = TONG
                self.startCalc(self.tong_list, bupai_list)
            else :
                self.tongResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[TIAO] == 0 :
                self.curCalcType = TIAO
                self.startCalc(self.tiao_list, bupai_list)
            else :
                self.tiaoResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[FENG] == 0 :
                self.curCalcType = FENG
                self.startCalc(self.feng_list, bupai_list)
            else :
                self.fengResultList.append(bupai_list)
                
            state = self.resultFenXi(self.wanResultList, self.tongResultList, self.tiaoResultList, self.fengResultList, True)
            if state :
                isTing = state
        if self.isHuRenYi == True :
            return True
        else :
            tmp_wanResultList = self.wanResultList
            tmp_tongResultList = self.tongResultList
            tmp_tiaoResultList = self.tiaoResultList
            tmp_fengResultList = self.fengResultList
        
        if self.chou_jiang(WAN) :#万
            state = self.resultFenXi(self.wanResultList, tmp_tongResultList, tmp_tiaoResultList, tmp_fengResultList)
            if state :
                isTing = state
        if self.isHuRenYi == True :
            return True

        if self.chou_jiang(TONG) :#TONG
            state = self.resultFenXi(tmp_wanResultList, self.tongResultList, tmp_tiaoResultList, tmp_fengResultList)
            if state :
                isTing = state
                
        if self.isHuRenYi == True :
            return True
        
        if self.chou_jiang(TIAO) :
            state = self.resultFenXi(tmp_wanResultList, tmp_tongResultList, self.tiaoResultList, tmp_fengResultList)
            if state :
                isTing = state
                
        if self.isHuRenYi == True :
            return True
        
        if self.chou_jiang(FENG) :
            state = self.resultFenXi(tmp_wanResultList, tmp_tongResultList, tmp_tiaoResultList, self.fengResultList)
            if state :
                isTing = state
                
        if self.isHuRenYi == True :
            return True
        return  isTing
            
    def resultFenXi(self, m_wanResultList, m_tongResultList, m_tiaoResultList, m_fengResultList, isZheng=False):
        wanMin = 99
        tongMin = 99
        tiaoMin = 99
        fengMin = 99
        wanSet = set()
        tongSet = set()
        tiaoSet = set()
        fengSet = set()
        if len(m_wanResultList) > 0 and len(m_tongResultList) > 0 and \
            len(m_tiaoResultList) > 0 and len(m_fengResultList) > 0 :
            
            for _list in m_wanResultList :
                if len(_list) <= wanMin :
                    if len(_list) < wanMin :
                        wanMin = len(_list)
                        wanSet = set()
                    wanSet = wanSet | set(_list)
                        
            for _list in m_tongResultList :
                if len(_list) <= tongMin :
                    if len(_list) < tongMin :
                        tongMin = len(_list)
                        tongSet = set()
                    tongSet = tongSet | set(_list)
                    
            for _list in m_tiaoResultList :
                if len(_list) <= tiaoMin :
                    if len(_list) < tiaoMin :
                        tiaoMin = len(_list)
                        tiaoSet = set()
                    tiaoSet = tiaoSet | set(_list)
                    
            for _list in m_fengResultList :
                if len(_list) <= fengMin :
                    if len(_list) < fengMin :
                        fengMin = len(_list)
                        fengSet = set()
                    fengSet = fengSet | set(_list)
        if wanMin + tongMin + tiaoMin + fengMin < self.lai_zi_count :
            if isZheng  : #将牌 胡牌类型
                if self.is_258_jiang :
                    self.resultMap |= wanSet | tongSet | tiaoSet |fengSet 
                    self.resultMap |= set([2,5,8,12,15,18,22,25,28])
                    return True
                else :
                    self.resultMap = set()
                    self.isHuRenYi = True
                    return True
            else :
                self.resultMap = set()
                self.isHuRenYi = True
                return True
        elif wanMin + tongMin + tiaoMin + fengMin <= self.lai_zi_count + 1 :
            self.resultMap |= wanSet | tongSet | tiaoSet |fengSet
            return True
        
        return False

    def check_3N(self):
        
        self.resultMap = set()
        isTing = False
        self.isHuRenYi = False
        bupai_list = []
        wanMin = 99
        tongMin = 99
        tiaoMin = 99
        fengMin = 99
        wanSet = set()
        tongSet = set()
        tiaoSet = set()
        fengSet = set()
        #都是整扑 多余的牌是癞子

        if True :
            bupai_list = []
            if self.zheng_pu_status[WAN] == 0 :
                self.curCalcType = WAN
                self.startCalc(self.wan_list, bupai_list)
            else :
                self.wanResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[TONG] == 0 :
                self.curCalcType = TONG
                self.startCalc(self.tong_list, bupai_list)
            else :
                self.tongResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[TIAO] == 0 :
                self.curCalcType = TIAO
                self.startCalc(self.tiao_list, bupai_list)
            else :
                self.tiaoResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[FENG] == 0 :
                self.curCalcType = FENG
                self.startCalc(self.feng_list, bupai_list)
            else :
                self.fengResultList.append(bupai_list)
        
        if (len(self.wanResultList) > 0 and len(self.tongResultList) > 0 and 
            len(self.tiaoResultList) > 0 and len(self.fengResultList) > 0) :
            
            for _list in self.wanResultList :
                if len(_list) <= wanMin :
                    if len(_list) < wanMin :
                        wanMin = len(_list)
                        wanSet = set()
                    wanSet = wanSet | set(_list)
                        
            for _list in self.tongResultList :
                if len(_list) <= tongMin :
                    if len(_list) < tongMin :
                        tongMin = len(_list)
                        tongSet = set()
                    tongSet = tongSet | set(_list)
                    
            for _list in self.tiaoResultList :
                if len(_list) <= tiaoMin :
                    if len(_list) < tiaoMin :
                        tiaoMin = len(_list)
                        tiaoSet = set()
                    tiaoSet = tiaoSet | set(_list)
                    
            for _list in self.fengResultList :
                if len(_list) <= fengMin :
                    if len(_list) < fengMin :
                        fengMin = len(_list)
                        fengSet = set()
                    fengSet = fengSet | set(_list)

        if wanMin + tongMin + tiaoMin + fengMin == self.lai_zi_count:
            return True

        return False
    
    def get_laizi_subs(self):
        pl = []
        for l in self.subs:
            l.sort()
            pl.append(l)

        result = [] 
        for p in pl:
            if p not in result:
                result.append(p)

        return result

    def remove_pai(self, paiId, laizi):
        
        if paiId == laizi:
            self.lai_zi_count -= 1
        elif paiId > 0 and paiId < 10:
            self.wan_list.remove(paiId)
        elif paiId > 10 and paiId < 20:
            self.tong_list.remove(paiId)
        elif paiId > 20 and paiId < 30:
            self.tiao_list.remove(paiId)
        elif paiId > 30 and paiId < 40: 
            self.feng_list.remove(paiId)

    def get_13yao_tings(self):
        #13幺听口
        if not self.is_13_yao:
            return []

        repl = []
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        if len(tiles)+self.lai_zi_count < 13:
            return []

        yao = [1,9,11,19,21,29]
        yao += [i for i in range(31,38)]
        if len(set(tiles)-set(yao)) > 0:#非幺
            return []

        if len(set(yao) - set(tiles)) > self.lai_zi_count + 1:#缺牌
            return []

        if len(set(yao) - set(tiles)) == self.lai_zi_count + 1:
            return list(set(yao)-set(tiles))
        else:#见幺胡
            return yao

    def get_7dui_tings(self, isrepl=False):
        pais = self.wan_list + self.tiao_list + self.tong_list + self.feng_list 
        if (len(pais) + self.lai_zi_count) < 13:
            return []

        pai_info = collections.Counter(pais)
        counter = [[],[],[],[]]
        for paiId, cnt in pai_info.items():
            counter[cnt-1].append(paiId)

        if (len(counter[2]) + len(counter[0])) <= self.lai_zi_count+1:
            if isrepl and self.lai_zi_count > len(counter[2])+len(counter[0]):
                return [0] #见字胡

            return counter[2] + counter[0]

        return []

    def refill(self):
        cnt = self.lai_zi_count
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        bu_zfb = self.is_bu_zfb
        is258 = self.is_258_jiang
        kan = self.check_kan
        self.clean()
        self.set_bu_zfb(bu_zfb)
        self.set_is_258_jiang(is258)
        self.set_check_kan(kan)
        self.set_pais(tiles)
        self.set_lai_zi_count(cnt)

    def get_ting_nodes(self, laizi, iskai):
        tiles = set(self.wan_list+self.tong_list+self.tiao_list+self.feng_list)
        
        logging.info('get_ting_nodes: {}'.format(tiles))
        nodes = []
        self0 = copy.deepcopy(self)
        for tile in tiles:
            self = copy.deepcopy(self0)
            self.remove_pai(tile, laizi)
            self.refill()
            node={}
            tmp = set()
            node['dropTile'] = tile
            node['nodes'] = []
            if self.check_ting():
                for t in self.resultMap:
                    tmp.add(t)
                    node['nodes'].append([t, 1])

            self = copy.deepcopy(self0)
            self.remove_pai(tile, laizi)
            for tt in self.get_7dui_tings():
                if tt not in tmp:
                    node['nodes'].append([tt, 1])

            if self.is_13_yao:
                self = copy.deepcopy(self0)
                self.remove_pai(tile, laizi)
                for ty in self.get_13yao_tings():
                    if ty not in tmp:
                        node['nodes'].append([ty, 1])

            if len(node['nodes']) > 0:
                if not iskai and laizi != 0 and [laizi, 1] not in node['nodes']:
                    node['nodes'].insert(0, [laizi, 1])
                nodes.append(node)

        return nodes 
    
    def can_angang(self, paiId, laizi, bupai):
        self0 = copy.deepcopy(self)
        if not self.check_ting():
            return True
        
        renhu = self.isHuRenYi
        res = self.resultMap
        self = copy.deepcopy(self0)
        for _ in range(4):
            self.remove_pai(paiId)
        
        self.set_pais([bupai])
        if not self.check_ting():
            return False

        if renhu != self.isHuRenYi or res != self.resultMap:
            return False
        return True

    def get_laizi_resmap2(self, pais, mo):
        #pdb.set_trace()
        self = copy.deepcopy(mo)
        if self.lai_zi_count == 0:
            mo.subs.append(pais)
            return

        self.lai_zi_count -= len(pais)
        self.set_pais(pais)
        if self.check_ting():
            for i in self.resultMap:
                if len(pais) + 1 == self.orig.lai_zi_count:
                    mo.subs.append(pais + [i])
                else:
                    self.get_laizi_resmap(pais + [i], mo)

    def get_laizi_resmap(self, pais, mo):
        if self.lai_zi_count == 0:
            mo.subs.append(pais)
            return

        self = copy.deepcopy(mo)
        self.lai_zi_count -= 1
        self.set_pais(pais)
        self.refill()

        if self.check_ting():
            for i in self.resultMap:
                if self.countOver4(i, pais):
                    continue
                if len(pais) + 1 == mo.orig.lai_zi_count:
                    mo.subs.append(pais + [i])
                else:
                    self.get_laizi_resmap(pais + [i], mo)

    # cover 1, no laizi; 2, with laizi
    def get_laizi_replace(self, paiId, laizi=None):
        repl = []
        mom = copy.deepcopy(self)
        if paiId == laizi:
            self.lai_zi_count += 1
        else:
            self.set_pais([paiId])

        if self.lai_zi_count == 0:
            return [[]]
        
        self.lai_zi_count -= 1
        self.refill()
        mo = copy.deepcopy(self)
        moo = copy.deepcopy(mo)
        moo.orig = mom

        if self.check_ting():
            if self.isHuRenYi:
                self.resultMap = set([r for r in range(1,38)])

            for p in self.resultMap:
                mo.get_laizi_resmap([p], moo)
            
            subs = moo.get_laizi_subs()
            repl = self.dedup(subs)
          
        self = copy.deepcopy(mom)
        tmp = self.check_7dui_repl(paiId, laizi)
        if len(tmp)>0:
            repl.extend(tmp)

        logging.info('get_laizi_replace: ret {}'.format(repl))
        if self.check_kan:
            res = self.check_max_kan_(repl)
            if len(res) > 0:
                self.kanCtx.append(res.pop(-1))
                self.kanCtx.append(res)

        return repl

    #牌型还原
    def qu0(self, handpais, res):
        if len(handpais) == 0:
            self.subs.append(res)
            self.subs = self.dedup(self.subs)
            return
        else:
            self.qu1(handpais, res)
            self.qu2(handpais, res) 

    def qu1(self, handpais0, res0):
        res = copy.copy(res0)
        pai_list = copy.copy(handpais0)
        paiId = pai_list[0]
        if pai_list.count(paiId)>=3 :
            pai_list = Util.del_paiList([paiId]*3, pai_list)
            res.append([paiId]*3)   
            self.qu0(pai_list, res)


    def qu2(self, handpais0, res0):
        res = copy.copy(res0)
        pai_list = copy.copy(handpais0)
        paiId = pai_list[0]
        if (paiId < 30 or self.check_zfb_bu(paiId)) and self.is_bu_3_tiao == False:
            if paiId+1 in pai_list and paiId+2 in pai_list: #ABC
                pai_list = Util.del_paiList([paiId, paiId+1,paiId+2], pai_list)
                res.append([paiId, paiId+1, paiId+2])    
                self.qu0(pai_list, res)
 

    def product(self, alist):

        repl = []
        if len(alist) == 1:
            for r in alist[0]:
                repl.append(r)
        elif len(alist) == 2:
            for r in alist[0]:
                for r1 in alist[1]:
                    repl.append(r + r1)
        elif len(alist) == 3:
            for r in alist[0]:
                for r1 in alist[1]:
                    for r2 in alist[2]:
                        repl.append(r+r1+r2)

        elif len(alist) == 4:
            for r in alist[0]:
                for r1 in alist[1]:
                    for r2 in alist[2]:
                        for r3 in alist[3]:
                            repl.append(r+r1+r2+r3)
        else:
            repl = [[]]

        return repl

    def check_gouzhang(self, paiId, laizi, cpg, repl):
        #够张
        self.set_pais(cpg + repl)
        if paiId != laizi:
            self.set_pais([paiId])

        return max(len(self.wan_list),len(self.tong_list),len(self.tiao_list)) >= 8 

    def check_queyimeng(self, paiId, laizi, cpg, repl):
        #缺一门
        self.set_pais(cpg + repl)
        if paiId != laizi:
            self.set_pais([paiId])

        res = [len(self.wan_list), len(self.tong_list), len(self.tiao_list)]
        res.sort()
        return res[0] == 0 


    def check_13yao2(self, paiId, laizi):
        #13幺
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1

        repl = []
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        logging.info('check_13yao2:0 {} {}'.format(tiles, paiId))
        if len(tiles)+self.lai_zi_count < 14:
            return []

        yao = [1,9,11,19,21,29]
        yao += [i for i in range(31,38)]
        if len(set(tiles)-set(yao)) > 0:#非幺
            return []

        if len(set(yao) - set(tiles)) > self.lai_zi_count:#缺牌
            return []

        tmp = list(set(yao) - set(tiles))
        if len(set(yao) - set(tiles)) < self.lai_zi_count:# only lack 1
            for t in yao:
                repl.append(tmp + [t])
        else:
            repl.append(tmp)

        logging.info('check_13yao2:{} {}'.format(tiles, repl))
        return repl   

    def check_hunyise(self, paiId, laizi, cpg):
        #混一色
        self.dump('check_hunyise')

        self.set_pais(cpg)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        lens = [len(self.wan_list),len(self.tong_list),len(self.tiao_list)]
        lens.sort()
        return lens[-2] == 0 and len(self.feng_list) != 0
        
    def check_hunyise_dh(self, paiId, laizi, cpg):
        #混一色 #大汗版本
        self.dump('check_hunyise_dh')

        self.set_pais(cpg)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        lens = [len(self.wan_list),len(self.tong_list),len(self.tiao_list)]
        lens.sort()
        return lens[-2] == 0 and len(self.feng_list) != 0 and lens[-1] > 0
        
    def check_qingyise(self, paiId, laizi, cpg):
        #清一色
        self.set_pais(cpg)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        lens = [len(self.wan_list),len(self.tong_list),len(self.tiao_list)]
        lens.sort()
        logging.info('check_qingyise: {} '.format(lens))
        return lens[-2] == 0 and len(self.feng_list) == 0

    def check_yitiaolong2(self, paiId, laizi, chi=[]):
        #一条龙 (最多4张癞子)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1

        self.set_pais(chi)
        res = []
        repl = []
        if len(set(self.wan_list)) >= 5: #
            if self.lai_zi_count < (9-len(set(self.wan_list))):
                return repl
            
            self.lai_zi_count -= (9-len(set(self.wan_list))) 
            res = Util.del_paiList(list(set(self.wan_list)),[r for r in range(1,10)])
            self.wan_list = Util.del_paiList(list(set(self.wan_list)), self.wan_list)
        elif len(set(self.tong_list)) >= 5: #
            if self.lai_zi_count < (9-len(set(self.tong_list))):
                return repl
            
            self.lai_zi_count -= (9-len(set(self.tong_list))) 
            res = Util.del_paiList(list(set(self.tong_list)),[r for r in range(11,20)])
            self.tong_list = Util.del_paiList(list(set(self.tong_list)), self.tong_list)
        elif len(set(self.tiao_list)) >= 5: #
            if self.lai_zi_count < (9-len(set(self.tiao_list))):
                return repl
            
            self.lai_zi_count -= (9-len(set(self.tiao_list))) 
            res = Util.del_paiList(list(set(self.tiao_list)),[r for r in range(21,30)])
            self.tiao_list = Util.del_paiList(list(set(self.tiao_list)), self.tiao_list)
        else:
            return repl

        cnt = self.lai_zi_count
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        self.clean()
        self.set_pais(tiles)
        self.set_lai_zi_count(cnt)

        if self.can_hu():
            self.refill()
            pid = self.get_simple_paiId(laizi) #assert pid != 0
            subs = self.get_laizi_replace(pid, laizi)
            if len(subs) > 0:
                for m in subs:
                    repl.append(res+m)
         
        logging.info('yitiaolong2: ret {}'.format(repl))
        return self.dedup(repl)

    def check_7dui_repl(self, paiId, laizi):
        logging.info('check_7dui_repl: enter {} {}'.format(paiId, laizi))
        repl = []
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1

        self.refill()
        lzcnt = self.lai_zi_count
        if lzcnt == 0:
            paiId = self.get_simple_paiId(laizi)
            res = self.get_7dui_tings(True)
            if len(res) == 1 and paiId in res:
                repl = [[]]
        else:
            self.lai_zi_count -= 1
            res = self.get_7dui_tings(True)
            if len(res) > 0 and lzcnt >= len(res):
                #lzcnt-len(res) MUST 0 or 2
                #assert(lzcnt-len(res) in [0,2])
                if res == [0]:
                    res = []
 
                if (lzcnt - len(res)) == 2:
                    for pid in range(1,38):
                        if self.countOver4(pid, res+[pid]):
                            continue
                        repl.append(res+[pid]*2)

                elif (lzcnt - len(res)) == 4:
                    for pid in range(1,38):
                        if self.countOver4(pid, res+[pid]):
                            continue
                        for pid1 in range(1,38):
                            if self.countOver4(pid1, res+[pid,pid,pid1]):
                                continue
                        repl.append(res + [pid,pid1]*2)
        
        return repl

    def check_penghu2(self, paiId, laizi):
        pais = self.wan_list + self.tiao_list + self.tong_list + self.feng_list 

        if paiId != laizi:
            pais.append(paiId) 
        else:
            self.lai_zi_count += 1

        repl = []
        pai_info = collections.Counter(pais)
        counter = [[],[],[],[]]
        for paiId, cnt in pai_info.items():
            counter[cnt-1].append(paiId)

        logging.info('check_penghu: {} {} {}'.format(self.lai_zi_count, pais, counter))
        # 14张牌 
        if len(counter[3]) > 0 or len(counter[0]) > 5:
            return []

        # for Jiang
        if len(counter[1]) > 0:
            if self.lai_zi_count < (len(counter[1]) - 1):# 1 -> jiang
                logging.info('check_penghu: {} {}'.format(self.lai_zi_count, 1))
                return []

            self.lai_zi_count -= len(counter[1]) -1

            if self.lai_zi_count < 2*len(counter[0]):
                logging.info('check_penghu: {} {}'.format(self.lai_zi_count, 2))
                return []

            #1 pair -> jiang
            tmp1 = []
            for pid in counter[0]:
                tmp1 += [pid]*2

            for pid in counter[1]:
                tmp2 = copy.copy(counter[1])
                tmp2.remove(pid)
                repl.append(tmp2 + tmp1)

            #2 single -> jiang
            tmp2 = [] 
            for pid in counter[1]:
                tmp2 += [pid]

            for pid in counter[0]:
                tmp1 = []
                tmp3 = copy.copy(counter[0])
                tmp3.remove(pid)
                for p in tmp3:
                    tmp1 += [p]*2
                repl.append(tmp2+[pid]+tmp1)

        else:
            if len(counter[0]) > 0:
                self.lai_zi_count -= 1 # 1-> Jiang
                if self.lai_zi_count < 2*(len(counter[0]) - 1): 
                    logging.info('check_penghu: {} {}'.format(self.lai_zi_count, 3))
                    return []

                self.lai_zi_count -= 2*(len(counter[0]) -1)

            for pid in counter[0]:
                tmp1 = []
                tmp2 = copy.copy(counter[0])
                tmp2.remove(pid)
                for p in tmp2:
                    tmp1 += [p]*2
                repl.append([pid]+tmp1)
       
        #repl = [r for r in repl if paiId not in r] #?
        logging.info('check_penghu2: ret {}'.format(repl))
        return self.dedup(repl)

    # from pair to triple
    def check_huka2(self, paiId, laizi):
        logging.info('check_huka: SELF=> {} '.format(self.__dict__))
        if paiId != laizi:
            return self.check_huka_(paiId, laizi)
        else:
            return self.check_huka_laizi_(paiId, laizi)
            

    def get_huka_star(self):
        tiles = []
        pais = set()
        trip = set()
        #trip = set([paiId-1, paiId, paiId+1])
        for paiId in range(2,9):
            trip = set([paiId-1, paiId, paiId+1])
            pais = trip - set(self.wan_list)
            if self.lai_zi_count >= len(pais):
                tiles.append(paiId)

        for paiId in range(12,19):
            trip = set([paiId-1, paiId, paiId+1])
            pais = trip - set(self.tong_list)
            if self.lai_zi_count >= len(pais):
                tiles.append(paiId)

        for paiId in range(22,29):
            trip = set([paiId-1, paiId, paiId+1])
            pais = trip - set(self.tiao_list)
            if self.lai_zi_count >= len(pais):
                tiles.append(paiId)

        trip = set([35,36,37])
        pais = trip - set(self.feng_list)
        if self.lai_zi_count >= len(pais):
            tiles.extend(list(trip))

        return tiles

    def can_hu(self):
        self.dump('can_hu')
        self.refill()
        pid = self.get_simple_paiId()
        if pid == 0:
            return True 

        if self.check_ting():
            return self.isHuRenYi or pid in self.resultMap
        else:
            return False

    # 胡卡  
    # from point to triple 
    def check_huka_(self, paiId, laizi):
        logging.info('check_huka_: enter {} {} {}'.format(self.__dict__,paiId,laizi))
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = []
        if paiId in [1,11,21,31,41,9,19,29,31,32,33,34]:
            return repl

        pais = set()
        trip = set([paiId-1, paiId, paiId+1])
        if paiId > 0 and paiId < 10:
            pais = trip - set(self.wan_list)
            self.wan_list = Util.del_paiList(list(trip-set(pais)), self.wan_list)
        elif paiId > 10 and paiId < 20:
            pais = trip - set(self.tong_list)
            self.tong_list = Util.del_paiList(list(trip-set(pais)), self.tong_list)

        elif paiId > 20 and paiId < 30:
            pais = trip - set(self.tiao_list)
            self.tiao_list = Util.del_paiList(list(trip-set(pais)), self.tiao_list)

        elif paiId in [35,36,37]:
            trip = set([35,36,37])
            pais = trip - set(self.feng_list)
            self.feng_list = Util.del_paiList(list(trip-set(pais)), self.feng_list)
        else:
            return repl

        if self.lai_zi_count >= len(pais):
            self.lai_zi_count -= len(pais)
        else:
            return repl
         
        self0 = copy.deepcopy(self)
        if self.can_hu():
            self = copy.deepcopy(self0)
            pid = self.get_simple_paiId(laizi)
            subs = self.get_laizi_replace(pid, laizi)
            if len(subs) > 0:
                for m in subs:
                    repl.append(list(pais) + m)

        logging.info('check_huka2: ret {}'.format(repl))
        return self.dedup(repl)

    # from pair to triple 
    def check_huka_laizi_(self, paiId, laizi):
        logging.info('check_huka: SELF=> {} '.format(self.__dict__))
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
       
        repl = []
        tiles = self.get_huka_star()
        self.lai_zi_count -= 1
        self0 = copy.deepcopy(self)
        for tile in tiles:
            self = copy.deepcopy(self0)
            tmp = self.check_huka_(tile, laizi)
            if len(tmp) > 0:
                for tl in tmp:
                    repl.append([tile] + tl)
            #else: can not huka

        return self.dedup(repl)

    # 胡卡 无癞子      
    def check_huka1(self, paiId, laizi):
        logging.info('check_huka: SELF=> {} '.format(self.__dict__))
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = []
        if paiId in [1,11,21,31,41,9,19,29,31,32,33,34]:
            return repl

        trip = [paiId-1, paiId, paiId+1]
        if paiId > 0 and paiId < 10 and paiId in self.wan_list:
            if (paiId-1) in self.wan_list and (paiId+1) in self.wan_list:
                self.wan_list = Util.del_paiList(trip, self.wan_list)
            else:
                return repl
        elif paiId > 10 and paiId < 20 and paiId in self.tong_list:
            if (paiId-1) in self.tong_list and (paiId+1) in self.tong_list:
                self.tong_list = Util.del_paiList(trip, self.tong_list)
            else:
                return repl

        elif paiId > 20 and paiId < 30 and paiId in self.tiao_list:
            if (paiId-1) in self.tiao_list and (paiId+1) in self.tiao_list:
                self.tiao_list = Util.del_paiList(trip, self.tiao_list)
            else:
                return repl

        elif paiId in [35,36,37] and paiId in self.feng_list:
            pais = [35,36,37]
            pais.remove(paiId)
            if pais[0] in self.feng_list and pais[1] in self.feng_list:
                self.feng_list = Util.del_paiList(pais, self.feng_list)
            else:
                return repl
        else:
            return repl

        self.refill()
        pid = self.get_simple_paiId()
        if pid == 0:
            return self.get_renyi_repl() 

        subs = self.get_laizi_replace(pid, laizi)
        repl = subs
         
        logging.info('check_huka1: ret {}'.format(repl))
        return self.dedup(repl)

    def check_hubian2(self, paiId, laizi):
        if paiId != laizi:
            return self.check_hubian_(paiId, laizi)
        else:
            return self.check_hubian_laizi_(paiId, laizi)

    # 胡卡 自摸癞子 
    # from pair to triple 
    def check_hubian_laizi_(self, paiId, laizi):
        repl = []
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
       
        tiles = self.get_hubian_star()
        self.lai_zi_count -= 1
        self0 = copy.deepcopy(self)
        for tile in tiles:
            self = copy.deepcopy(self0)
            tmp = self.check_hubian_(tile, laizi)
            if len(tmp) > 0:
                for tl in tmp:
                    repl.append([tile] + tl)
            
        return self.dedup(repl)

    def check_hubian_(self, paiId, laizi):
        repl = []
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        if paiId not in [3,13,23,33,7,17,27,35]:
            return repl

        pais = set()
        trip = set()
        if paiId%10 == 3:
            trip = set([paiId, paiId-2, paiId-1])
        else:
            trip = set([paiId, paiId+1, paiId+2])

        if paiId > 0 and paiId < 10:
            pais = trip - set(self.wan_list)
            self.wan_list = Util.del_paiList(list(trip-set(pais)), self.wan_list)

        elif paiId > 10 and paiId < 20:
            pais = trip - set(self.tong_list)
            self.tong_list = Util.del_paiList(list(trip-set(pais)), self.tong_list)

        elif paiId > 20 and paiId < 30:
            pais = trip - set(self.tiao_list)
            self.tiao_list = Util.del_paiList(list(trip-set(pais)), self.tiao_list)

        elif paiId == 35:
            trip = set([35,36,37])
            pais = trip - set(self.feng_list)
            self.feng_list = Util.del_paiList(list(trip-set(pais)), self.feng_list)
        else:
            return repl
        
        if self.lai_zi_count >= len(pais):
            self.lai_zi_count -= len(pais)
        else:
            return repl
         
        self0 = copy.deepcopy(self)
        if self.can_hu():
            self = copy.deepcopy(self0)
            pid = self.get_simple_paiId(laizi)
            subs = self.get_laizi_replace(pid, laizi)
            if len(subs) > 0:
                for m in subs:
                    repl.append(list(pais)+m)
            else:
                repl.append(list(pais))
         
        return self.dedup(repl)


    def get_renyi_repl(self):
        return [[i] for i in range(1,38)]

    def get_diff_slots(self, dna, _list):

        done = []
        tmp1 = copy.copy(dna) 
        for i in _list:
            if i in tmp1:
                done.append(i)
                tmp1.remove(i) 

        tmp2 = copy.copy(_list)
        for j in dna: 
            if j in tmp2:
                tmp2.remove(j)

        return tmp1, done

            
    def check_diff_(self, paiId, laizi, dna):

        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1

        res = []
        repl = []

        self0 = copy.deepcopy(self)
        need, done = self.get_diff_slots(map(lambda x:x, dna), self.wan_list)
        if self.lai_zi_count >= len(need): 
            res.append([need, done])

        need, done = self.get_diff_slots(map(lambda x:x+10, dna), self.tong_list)
        if self.lai_zi_count >= len(need): 
            res.append([need, done])

        need, done = self.get_diff_slots(map(lambda x:x+20, dna), self.tiao_list)
        if self.lai_zi_count >= len(need): 
            res.append([need, done])
            
        logging.info('check_diff_:{} {} {}'.format(res, paiId, dna))
        if len(res) == 0:
            return repl

        for [rpl, slots] in res:
            self = copy.deepcopy(self0)
            logging.info('check_diff_:loop {} {}'.format(rpl, slots))
            tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
            tiles = Util.del_paiList(slots, tiles)
            lzcnt = self.lai_zi_count
            self.clean()
            self.set_pais(tiles)
            self.set_lai_zi_count(lzcnt - len(rpl))

            if self.can_hu():
                self.dump('')
                pid = self.get_simple_paiId(laizi)
                if pid == 0:
                    return self.get_renyi_repl()

                subs = self.get_laizi_replace(pid, laizi)
                if len(subs) > 0:
                    repl.append([rpl, subs])

        return repl

    def contains(self, llb, la):
        if len(la) == 0 or sorted(la) in sorted(llb):
            return True, la 
 
        for lb in llb:
            if len(lb) > len(la) and set(la).issubset(set(lb)):
                return True, lb
    
        return False, []

    def isSubset(self, la, lb):
        if len(lb) > len(la) and set(la).issubset(set(lb)):
            return True
        return False

    def isCover3N(self, takes, tiles):

        takes.sort(key=lambda x:x[1], reverse=True)
        for tk in takes:
            if self.isSubset(tk[0], tiles):
                for p in tk[0]:
                    tiles.remove(p)

        return len(tiles) == 2 and tiles[0] == tiles[1]

    def check_quanda2_(self, paiId, laizi):
        #全大
        repl = self.check_DNA_(paiId, laizi, [[7,8,9]])
        if len(repl) > 0:
            tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
            if self.isCover3N(self.fxTakes, tiles):
                return repl
        return repl
        
    def check_quanzhong2_(self, paiId, laizi):
        #全中
        repl = self.check_DNA_(paiId, laizi, [[4,5,6]])
        if len(repl) > 0:
            tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
            if self.isCover3N(self.fxTakes, tiles):
                return repl
        return repl
        
    def check_quanxiao2_(self, paiId, laizi):
        #全小
        repl = self.check_DNA_(paiId, laizi, [[1,2,3]])
        if len(repl) > 0:
            tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
            if self.isCover3N(self.fxTakes, tiles):
                return repl
        return repl
        

    def check_dalian2(self, paiId, laizi):

        dnas = [range(1, 7),range(4, 10)]
        return self.check_DNA_(paiId, laizi, dnas)
        
    def check_xiaolian2(self, paiId, laizi):

        dnas = [range(2, 8),range(3, 9)]
        return self.check_DNA_(paiId, laizi, dnas)
        
    def check_laoshao2(self, paiId, laizi):

        dnas = [range(1, 4) + range(7, 10)]
        return self.check_DNA_(paiId, laizi, dnas)
        

    def check_DNA_(self, paiId, laizi, dnas):

        repl = []
        self0 = copy.deepcopy(self)

        for dna in dnas:
            rep = []
            res = self.check_diff_(paiId, laizi, dna)

            if len(res) > 0:
                hits = 0
                if len(repl) > 0:
                    hits = repl.pop(-1)
     
                logging.info('check_DNA_:lp {} {}'.format(repl, res))
                if len(res) > 1:
                    for rdna, rlefts in res:
                        for rdna1, rlefts1 in res:
                            if rdna1 != rdna:
                                ok, r = self.contains(rlefts, rdna1)
                                ok1, r1 = self.contains(rlefts1, rdna) 
                                if ok and ok1:
                                    rep.append(rdna + r)

                    if len(rep) > 0:
                        rep = self.dedup(rep)
                        if hits == 2:
                            repl.extend(rep)
                            repl.append(2)# 最后一个元素hits
                            continue
                        else: 
                            repl = rep 
                            repl.append(2)
                            continue

                if hits < 2: 
                    for rd, rlfs in res:
                        for rlf in rlfs:
                            rep.append(rd + rlf)
                    
                    repl = self.dedup(rep)
                    logging.info('check_DNA_: lp1 {} '.format(rep, repl))
                    repl.append(1)
                elif len(repl) > 0:
                    repl.append(hits)
 
            self = copy.deepcopy(self0)
            logging.info('check_DNA_: loop {} '.format(repl))
        logging.info('check_DNA_:  {} '.format(repl))
        return repl
                            

    #无癞子
    def get_kan_count(self, rep):
        cnt = 0
        self.set_pais(rep)
        for _type in [WAN,TONG,TIAO,FENG]:
            tiles = self.get_ctype_tiles(_type)
            cnt += self.get_kan_cnt2_(tiles)

        return cnt

    def get_kan_cnt2_(self, tiles):

        mcnt = 0
        if self.check_zheng_pu(tiles):
            mcnt = self.get_kan_cnt_(tiles)
        else:
            pai_info = collections.Counter(tiles)
            for paiId, cnt in pai_info.items():
                if cnt >= 2:
                    for _ in xrange(2):
                        tiles.remove(paiId)

                    cnt = self.get_kan_cnt_(tiles)
                    if cnt > mcnt:
                        mcnt = cnt
                    tiles.extend([paiId]*2)

        return mcnt

    def get_kan_cnt_(self, tiles):

        count = 0 
        subject = []
        pai_info = collections.Counter(tiles)
        for paiId, cnt in pai_info.items():
            if cnt >= 3:
                subject.append(paiId)

        for sj in subject:
            for _ in xrange(3):
                tiles.remove(sj)

            if self.check_zheng_pu(tiles): 
                cnt = self.get_kan_cnt_(tiles)
                if (cnt + 1) > count:
                    count = cnt + 1

            tiles.extend([sj]*3)
       
        return count
            
    #无癞子
    def get_yibangao_cnt(self, rep):
        cnt = 0
        self.set_pais(rep)
        for _type in [WAN,TONG,TIAO,FENG]:
            tiles = self.get_ctype_tiles(_type)
            cnt += self.get_ybg_cnt_(tiles)

        return cnt

    def get_kan_cnt_(self, tiles):

        count = 0 
        subject = []
        pai_info = collections.Counter(tiles)
        for paiId, cnt in pai_info.items():
            if cnt >= 3:
                subject.append(paiId)
        for sj in subject:
            for _ in xrange(3):
                tiles.remove(sj)

            if self.check_zheng_pu(tiles): 
                cnt = self.get_kan_cnt_(tiles)
                if (cnt + 1) > count:
                    count = cnt + 1
            tiles.extend([sj]*3)
       
        return count
    
    def get_all_ABC(self, tiles):
        abc = []
        for t in sorted(tiles):      
            if t+1 in tiles and t+2 in tiles:
                abc.append([t,t+1,t+2])

        return abc 

    #yibangao 
    def get_ybg_cnt_(self, tiles):

        if len(tiles) < 6:
            return 0

        count = 0
        subject = []
        pai_info = collections.Counter(tiles)
        for paiId, cnt in pai_info.items():
            if cnt >= 2:
                subject.append(paiId)

        abc = self.get_all_ABC(subject) 
        for o in abc:
            for i in o: 
                for _ in xrange(2):
                    tiles.remove(i)

            if self.check_zheng_pu(tiles): 
                cnt = self.get_ybg_cnt_(tiles)
                if cnt != -1 and (cnt + 1) > count:
                    count = cnt + 1
            else:
                tmp = copy.deepcopy(tiles)
                for t in tiles:
                    if tiles.count(t) >= 2:
                        [tmp.remove(t) for _ in xrange(2)]

                        if self.check_zheng_pu(tmp): 
                            cnt = self.get_ybg_cnt_(tmp)
                            if cnt != -1 and (cnt + 1) > count:
                                count = cnt + 1

                        tmp.extend([t]*2)
                        
            tiles.extend(o*2)
      
        return count
            
    def get_paiId_ctype(self, paiId):
        return paiId/10
       
    def get_ctype_tiles(self, _type): 
        pai_list = []
        if _type == WAN :
            pai_list = copy.copy(self.wan_list)
        elif _type == TONG :
            pai_list = copy.copy(self.tong_list)
        elif _type == TIAO :
            pai_list = copy.copy(self.tiao_list)
        elif _type == FENG :
            pai_list = copy.copy(self.feng_list)

        return pai_list
 
         
    def check_max_kan2(self, paiId, laizi):

        reps =self.get_laizi_replace(paiId, laizi)   
        return self.check_max_kan_(reps) 
        
 
    def check_max_kan_(self, reps):
         
        maxcnt = 0
        repl = []
        self0 = copy.deepcopy(self)
        for rep in reps:
            cnt = self.get_kan_count(rep) 
            if cnt > maxcnt:
                maxcnt = cnt
                repl = [rep]
            elif cnt == maxcnt:
                repl.append(rep)

            self = copy.deepcopy(self0)

        if maxcnt > 0:
            repl.append(maxcnt)# count 在repl最后1项
        else:
            repl = []

        return repl 

    def check_yibangao2(self, paiId, laizi):

        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
   
        self0 = copy.deepcopy(self)
        reps =self.get_laizi_replace(paiId, laizi)   
         
        maxcnt = 0
        repl = [] 
        for rep in reps:
            self = copy.deepcopy(self0)
            cnt = self.get_yibangao_cnt(rep) 
            if cnt > maxcnt:
                maxcnt = cnt
                repl = [rep]
            elif cnt == maxcnt:
                repl.append(rep)
        
        if maxcnt > 0:
            repl.append(maxcnt)# count 在repl最后1项
        else:
            repl = []

        return repl

    def check_siguiyi_(self, paiId):
        
        ctype = self.get_paiId_ctype(paiId)
        tiles = self.get_ctype_tiles(ctype)
        if tiles.count(paiId) < 4:
            return False

        if self.check_zheng_pu(tiles):
            return True
        else: 
            pai_info = collections.Counter(tiles)
            for pp, cnt in pai_info.items():
                if cnt >= 2:
                    for _ in xrange(2):
                        tiles.remove(pp)

                    if self.check_zheng_pu(tiles):
                        return True
                    tiles.extend([pp, pp])

        return False
         
    def get_AAAA_set(self):
        res = set()
        for ctype in [WAN,TONG,TIAO,FENG]:
            tiles = self.get_ctype_tiles(ctype)
            for t in tiles:
                if tiles.count(t) == 4:
                    res.add(t)
        return res
        
    def check_siguiyi2(self, paiId, laizi):
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1

        self0 = copy.deepcopy(self)
        reps =self.get_laizi_replace(paiId, laizi)   
         
        repl = []
        if paiId != laizi: 
            for rep in reps:
                self = copy.deepcopy(self0)
                self.set_pais(rep)
                if self.check_siguiyi_(paiId):
                    repl = [rep]
                    break
        else: 
            for rep in reps:
                self = copy.deepcopy(self0)
                self.set_pais(rep)
                for pp in set(rep)&self.get_AAAA_set():
                    if self.check_siguiyi_(pp):
                        repl = [rep]
                    break
                    
        return repl 

    def check_dandiao2(self, paiId, laizi):

        repl = []
        if paiId != laizi:
            return self.check_dandiao2_(paiId)
        else:
            self.lai_zi_count += 1
            self0 = copy.deepcopy(self)
            tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list

            for tile in set(tiles):
                self = copy.deepcopy(self0)
                self.remove_pai(tile, laizi)
                self.lai_zi_count -= 1 
                self.refill()
                tmp2 = self.check_3N2()
                if len(tmp2)>0:
                    for r in tmp2:
                        repl.append([tile] + r)
        
        return repl                        

    def check_dandiao2_(self, paiId):
        logging.info('check_dandiao: SELF=> {} '.format(self.__dict__))
        
        repl = []
        tmp = []
        if paiId > 0 and paiId < 10:
            if paiId in self.wan_list: 
                self.wan_list.remove(paiId)
            elif self.lai_zi_count > 0:
                self.lai_zi_count -= 1
                tmp = [paiId]
            else:
                return repl

        elif paiId > 10 and paiId < 20:
            if paiId in self.tong_list: 
                self.tong_list.remove(paiId)
            elif self.lai_zi_count > 0:
                self.lai_zi_count -= 1
                tmp = [paiId]
            else:
                return repl

        elif paiId > 20 and paiId < 30:
            if paiId in self.tiao_list: 
                self.tiao_list.remove(paiId)
            elif self.lai_zi_count > 0:
                self.lai_zi_count -= 1
                tmp = [paiId]
            else:
                return repl
        elif paiId > 30 and paiId < 40: 
            if paiId in self.feng_list:
                self.feng_list.remove(paiId)
            elif self.lai_zi_count > 0:
                self.lai_zi_count -= 1
                tmp = [paiId]
            else:
                return repl
        else:
            return repl

        self.refill()
        tmp2 = self.check_3N2()
        if len(tmp2)>0:# [[]] -> no laizi
            for r in tmp2:
                repl.append(tmp + r)

        return self.dedup(repl)

    def check_3N2(self):
        
        self.resultMap = set()
        isTing = False
        self.isHuRenYi = False
        bupai_list = []
        wanMin = 99
        tongMin = 99
        tiaoMin = 99
        fengMin = 99
        wanSet = set()
        tongSet = set()
        tiaoSet = set()
        fengSet = set()
        #都是整扑 多余的牌是癞子

        if True :
            bupai_list = []
            if self.zheng_pu_status[WAN] == 0 :
                self.curCalcType = WAN
                self.startCalc(self.wan_list, bupai_list)
            else :
                self.wanResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[TONG] == 0 :
                self.curCalcType = TONG
                self.startCalc(self.tong_list, bupai_list)
            else :
                self.tongResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[TIAO] == 0 :
                self.curCalcType = TIAO
                self.startCalc(self.tiao_list, bupai_list)
            else :
                self.tiaoResultList.append(bupai_list)
                
            bupai_list = []
            if self.zheng_pu_status[FENG] == 0 :
                self.curCalcType = FENG
                self.startCalc(self.feng_list, bupai_list)
            else :
                self.fengResultList.append(bupai_list)
        
        repl = []
        wanList = []
        tongList = []
        tiaoList = []
        fengList = []
        allList = []
        if (len(self.wanResultList) > 0 and len(self.tongResultList) > 0 and 
            len(self.tiaoResultList) > 0 and len(self.fengResultList) > 0) :
            
            for _list in self.wanResultList :
                if len(_list) <= wanMin :
                    if len(_list) < wanMin :
                        wanMin = len(_list)
                        wanSet = set()
                        wanList = []
                    wanSet = wanSet | set(_list)
                    wanList.append(_list)
            if wanMin > 0:
                allList.append(wanList) 
                        
            for _list in self.tongResultList :
                if len(_list) <= tongMin :
                    if len(_list) < tongMin :
                        tongMin = len(_list)
                        tongSet = set()
                        tongList = []
                    tongSet = tongSet | set(_list)
                    tongList.append(_list) 
            if tongMin > 0:
                allList.append(tongList)
 
            for _list in self.tiaoResultList :
                if len(_list) <= tiaoMin :
                    if len(_list) < tiaoMin :
                        tiaoMin = len(_list)
                        tiaoSet = set()
                        tiaoList = []
                    tiaoSet = tiaoSet | set(_list)
                    tiaoList.append(_list) 
            if tiaoMin > 0:
                allList.append(tiaoList) 
                    
            for _list in self.fengResultList :
                if len(_list) <= fengMin :
                    if len(_list) < fengMin :
                        fengMin = len(_list)
                        fengSet = set()
                        fengList = []
                    fengSet = fengSet | set(_list)
                    fengList.append(_list) 
            if fengMin > 0:
                allList.append(fengList) 

        if wanMin + tongMin + tiaoMin + fengMin <= self.lai_zi_count:
            repl = self.product(allList)

        #repl is []-> not hu
        return self.dedup(repl)

    def check_sanjiegao(self, paiId, laizi):
        #一色三同顺，一色三节高 
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] >= 3:
            for tk in self.fxTakes:
                if tk[1] == repl[-1]:
                    for p in sorted(set(tk[0])):
                        if p+1 in tk[0] and p+2 in tk[0]:
                            repl.pop(-1)
                            return repl
                    repl = []

        return repl

    def get_jiang_pai(self, tiles):
        jiangs = []
        pai_info = collections.Counter(tiles)
        for paiId, cnt in pai_info.items():
            if cnt >= 2:
                for _ in xrange(2):
                    tiles.remove(paiId)

                if self.check_zheng_pu(tiles):
                    jiangs.append(paiId)

                tiles.extend([paiId]*2)
        return jiangs
        
    def get_hu_paixins(self, tiles):
        px = []
        pai_info = collections.Counter(tiles)
        for paiId, cnt in pai_info.items():
            if cnt >= 2:
                for _ in xrange(2):
                    tiles.remove(paiId)

                self.qu0(tiles, [])
                if len(self.subs) > 0:
                    for s in self.subs:
                        it = []
                        it.append([paiId]*2)
                        it.extend(s)
                        px.append(it)
                tiles.extend([paiId]*2)
        return px
        

    def check_xiaosixi(self, paiId, laizi):
        #小四喜
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] >= 3:
            for tk in self.fxTakes:
                if tk[1] == repl[-1]:
                    cnt = 0
                    for p in sorted(set(tk[0])):
                        if p > 30 and p < 35:
                            cnt += 1
                    if cnt >= 3:
                        tiles = (self.wan_list + self.tong_list + 
                                   self.tiao_list + self.feng_list)
                        left = [i for i in tiles if i not in tk[0]]
                        for j in self.get_jiang_pai(left):
                            if j > 30 and p < 35:
                                repl.pop(-1)
                                return repl
                    repl = []

        return repl

    def check_dasixi(self, paiId, laizi):
        #大四喜
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] == 4:
            for tk in self.fxTakes:
                if tk[1] == repl[-1]:
                    cnt = 0
                    for p in sorted(set(tk[0])):
                        if p > 30 and p < 35:
                            cnt += 1
                    if cnt == 4:
                        repl.pop(-1)
                        return repl

                    repl = []

        return repl

    def check_xiaosanyuan(self, paiId, laizi):
        #小三元
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] >= 2:
            for tk in self.fxTakes:
                if tk[1] == repl[-1]:
                    cnt = 0
                    for p in sorted(set(tk[0])):
                        if p > 34:
                            cnt += 1
                    if cnt >= 2:
                        tiles = (self.wan_list + self.tong_list + 
                                   self.tiao_list + self.feng_list)
                        left = [i for i in tiles if i not in tk[0]]
                        for j in self.get_jiang_pai(left):
                            if j > 34:
                                repl.pop(-1)
                                return repl
                    repl = []

        return repl

    def check_dasanyuan(self, paiId, laizi):
        #大三元
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] >= 3:
            for tk in self.fxTakes:
                if tk[1] == repl[-1]:
                    cnt = 0
                    for p in sorted(set(tk[0])):
                        if p > 34:
                            cnt += 1
                    if cnt == 3:
                        repl.pop(-1)
                        return repl
                    repl = []

        return repl


    def check_ziyise(self, paiId, laizi):
        #字一色
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = []       
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for p in set(tiles):
            if p < 30:
                return repl

        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] == 4:
            repl.pop(-1)

        return repl

    def check_sibugao(self, paiId, laizi):
        #一色四步高
        
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = []       
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for p in self.get_jiang_pai(tiles): 
            for _ in xrange(2):
                tiles.remove(p)
            if min(tiles)/10 == max(tiles)/10 and min(tiles) + 5 == max(tiles):
                for i in range(min(tiles)+1,max(tiles)):
                    if tiles.count(i) != 2:
                        continue
                repl = [[]]
                break

        return repl

    def check_sanjiegao(self, paiId, laizi):
        #三色三节高
        
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] >= 3:
            for tk in self.fxTakes:
                if tk[1] == repl[-1]:
                    if len(set([p/10 for p in set(tk[0]) if p < 30])) < 3:
                        return repl

                    pp = [p%10 for p in sorted(set(tk[0]))]
                    if len(pp) == 3:
                        if pp[0]+1 in pp and pp[0]+2 in pp:
                            repl.pop(-1)
                            break
                    elif pp[1]+1 in pp and pp[1]+2 in pp:
                        repl.pop(-1)
                        break
                        
        return repl

    def check_qingyaojiu(self, paiId, laizi):
        #清幺九
        
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = []       
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for p in set(tiles):
            if p < 30 and p%10 not in [1,9]:
                return repl

        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] == 4:
            repl.pop(-1)

        return repl

    def check_qingyaojiu(self, paiId, laizi):
        #混幺九
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = []       
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for p in set(tiles):
            if p < 30 and p%10 not in [1,9]:
                return repl

        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] == 4:
            repl.pop(-1)

        return repl

    def check_shuangke(self, paiId, laizi):
        #全双刻 
        self1 = copy.deepcopy(self)
        if paiId != laizi:
            self.set_pais([paiId])
        else:
            self.lai_zi_count += 1
        
        repl = []       
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for p in set(tiles):
            if p%2 == 1:
                return repl
 
        repl = self1.check_max_kan2(paiId, laizi)
        if len(repl) > 0 and repl[-1] == 4:
            repl.pop(-1)

        return repl

    def check_hundiao_ting(self):
        #金钩听
        if self.lai_zi_count == 0:
            return False
        
        lzcnt = self.lai_zi_count
        self.lai_zi_count -= 1
        self.refill()
        tmp = self.check_3N2()
        if len(tmp) > 0:
            return True

        return False

    def can_shangtai(self, paiId, laizi):
        # 上台
        if self.lai_zi_count < 2:
            return False

        self.lai_zi_count -= 2
        if self.check_3N():
            return True

        return False

    def check_yaojiu(self, paiId, cpg2):
        #幺九
        self.dump('check_yaojiu')
        self.set_pais([paiId])
        for pair in cpg2:
            if (1 not in map(lambda x:x%10, pair) 
                  and 9 not in map(lambda x:x%10, pair)):
                return False

        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        paixins = self.get_hu_paixins(tiles)

        for px in paixins:
            found = True
            for pair in px:
                if (1 not in map(lambda x:x%10, pair) 
                      and 9 not in map(lambda x:x%10, pair)):
                    found = False
                    break

            if found:
                return True

        return False

    def check_5_pais(self, paiId, cpg2):
        #全带五
        self.dump('check_5_pais')
        self.set_pais([paiId])
        for pair in cpg2:
            if 5 not in map(lambda x:x%10, pair):
                return False

        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        paixins = self.get_hu_paixins(tiles)

        for px in paixins:
            found = True
            for pair in px:
                if 5 not in map(lambda x:x%10, pair):
                    continue
 
            if found:
                return True

        return False
                
    def check_zhong_pais(self, paiId, cpg2):
        #中牌，断幺
        self.dump('check_zhong_pais')

        self.set_pais([paiId])
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for pair in cpg2:
            tiles.extend(pair)
       
        for t in tiles:
            if t%10 in [1, 9]:
                return False

        return True 

                
    def check_258_pais(self, paiId, cpg2):
        self.dump('check_258_pais')

        self.set_pais([paiId])
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for pair in cpg2:
            tiles.extend(pair)
       
        for t in tiles:
            if t%10 not in [2,5,8]:
                return False 

        return True

    def check_5c_pais(self, paiId, cpg2):
        #五齐门
        self.dump('check_5c_pais')

        self.set_pais([paiId])
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        for pair in cpg2:
            tiles.extend(pair)
      
        cc = [0,1,2,3]
        jian = False 
        for t in tiles:
            if t < 35:
                if t/10 in cc:
                    cc.remove(t/10)
            elif t > 30 and t < 35:
                jian = True 

        return len(cc) == 0 and jian

    def check_1234_pais(self, paiId, cpg2):
        #小于五
        self.dump('check_1234_pais')

        self.set_pais([paiId])
        tiles = self.wan_list +self.tong_list +self.tiao_list +self.feng_list
        for pair in cpg2:
            tiles.extend(pair)
       
        for t in tiles:
            if t%10 > 4:
                return False 

        return True

    def check_tuibudao(self, paiId, cpg2):
        #推不倒
        self.dump('check_tuibudao')

        self.set_pais([paiId])
        tiles = self.wan_list +self.tong_list +self.tiao_list +self.feng_list
        for pair in cpg2:
            tiles.extend(pair)
       
        for t in tiles:
            if t not in [11,12,13,14,15,18,19,22,24,25,26,28,29,37]:
                return False 

        return True

                
    def check_zuhelong(self, paiId, cpg2):
        #组合龙
        self.dump('check_zuhelong')
        
        if len(cpg2) > 1:
            return False

        self.set_pais([paiId])
        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list

        dnas = [[1,4,7], [2,5,8], [3,6,9]]
        pais = [self.wan_list, self.tong_list, self.tiao_list]

        ctx = [[],[],[]]
        se = set([3,1,2])# 哪个dna
        for i, ts in enumerate(pais): 
            for dna in dnas: 
                if set(dna).issubset(map(lambda x:x%10, ts)) and dna[0] in se:
                    ctx[i].append(map(lambda x:x+10*(ts[0]/10), dna))

            if len(ctx[i]) == 0:
                return False
            elif len(ctx[i]) == 1:
                if ctx[i][0][0]%10 not in se:
                    return False
                else:
                    se.remove(ctx[i][0][0]%10)

                for p in ctx[i][0]:
                    pais[i].remove(p)
                
        if len(se) > 1:
            return False
        if len(se) == 1:
            for i, cx in enumerate(ctx):
                if len(cx) == 2:
                    for p1 in cx:
                        if p1[0]%10 == list(se)[0]:
                            for pp in p1:
                                pais[i].remove(pp)
                                break
                     
        if self.can_hu():
            return True 

        return False

    def check_hualong(self, paiId, cpg2):
        #花龙
        self.dump('check_hualong')
        self.set_pais([paiId])

        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        paixins = self.get_hu_paixins(tiles)

        for i, it in enumerate(paixins):
            it.extend(cpg2)
            paixins[i] = it

        for px in paixins:

            hua = []
            for pair in px:
                if (map(lambda x:x%10, pair) in [[1,2,3],[4,5,6],[7,8,9]]
                      and pair[0]/10 not in map(lambda x:x/10, hua)
                      and pair[0] not in hua):
                    hua.extend(pair) 

            if len(hua) == 9:
                return True 

        return False

    def check_lianliu(self, paiId, cpg2):
        #连六
        self.dump('check_lianliu')
        self.set_pais([paiId])

        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        paixins = self.get_hu_paixins(tiles)

        for i, it in enumerate(paixins):
            for cp in cpg2:
                if cp[0] != cp[1]:
                    it.extend(cpg2)
            paixins[i] = it

        for px in paixins:
            hua = []
            for pair in px:
                if pair[0] != pair[1]:
                    hua.extend(min(pair)) #TODO wild!

            for h in hua:
                if h+3 in hua:
                    return True 

        return False

    def check_xixiangfen(self, paiId, cpg2):
        #喜相逢
        self.dump('check_lianliu')
        self.set_pais([paiId])

        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        paixins = self.get_hu_paixins(tiles)

        for i, it in enumerate(paixins):
            for cp in cpg2:
                if cp[0] != cp[1]:
                    it.extend(cpg2)
            paixins[i] = it

        for px in paixins:
            hua = []
            for pair in px:
                if pair[0] != pair[1]:
                    hua.extend(min(pair)) #TODO wild!

            for h in hua:
                c = range(3)
                c.remove(h/10)
                if cc in c:
                    if h%10 + cc*10 in hua:
                        return True 

        return False

    def check_3tongshun(self, paiId, cpg2):
        #三色三同顺
        self.dump('check_3tongshun')
        self.set_pais([paiId])

        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        paixins = self.get_hu_paixins(tiles)

        for i, it in enumerate(paixins):
            for cp in cpg2:
                if cp[0] != cp[1]:
                    it.append(cp)
            paixins[i] = it

        for px in paixins:
            hua = []
            for pair in px:
                if pair[0] != pair[1]:
                    if len(hua) == 0:
                        hua.append(min(pair))
                    elif (min(pair)%10 == hua[0] 
                            and min(pair)/10 not in map(lambda x:x/10, hua)):
                        hua.append(min(pair))

            if len(hua) == 3:
                return True 

        return False

    def is_ABC(self, pais):
        return len(pais) == 3 and min(pais)+2 == max(pais)

    def check_33bugao(self, paiId, cpg2):
        #三色三步高
        self.dump('check_33bugao')
        self.set_pais([paiId])

        tiles = self.wan_list + self.tong_list + self.tiao_list + self.feng_list
        paixins = self.get_hu_paixins(tiles)

        for i, it in enumerate(paixins):
            for cp in cpg2:
                if cp[0] != cp[1]:
                    it.append(cp)
            paixins[i] = it

        for px in paixins:
            hua = []
            for pair in px:
                if pair[0] != pair[1]:
                    hua.append(min(pair))

                elif (min(pair)%10 not in map(lambda x:x%10, hua)
                        and min(pair)/10 not in hua): 
                    hua.append(min(pair))

            if len(hua) >= 3:
                c = map(lambda x:x/10, hua)
                if len(set(c)) == 3:
                    for cc in set(c):
                        c.remove(cc)

                    if len(c) > 0:
                        hh = []
                        tmp = []
                        for h in hua:
                            if h/10 == c[0]:
                                hh.append(h)
                            else:
                                tmp.append(h)
                        
                        for a in hh:
                            if self.is_ABC(map(lambda x: x%10, tmp+[a])):
                                return True

                    else:
                        if self.is_ABC(map(lambda x: x%10, hua)):
                            return True
        return False


