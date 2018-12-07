import sys
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, qApp, QMessageBox
from PyQt5 import QtCore, QtGui, uic
import sqlite3
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib import style
import pandas as pd
import os.path
import os

matplotlib.use('Qt5Agg')


# 경로 설정
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


form_class = uic.loadUiType(resource_path("main_window.ui"))[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Exit 버튼
        self.actionExit.triggered.connect(qApp.quit)

        # 초기 탭 2 3,4 사용불가
        self.tab_2.setEnabled(False)
        self.tab_3.setEnabled(False)
        self.tab_4.setEnabled(False)

        # 초기 등록, 삭제 버튼 사용불가
        self.pushRegist.setEnabled(False)
        self.pushErase.setEnabled(False)

        # 로그 파일 없으면 로드 버튼 사용불가
        if os.path.isfile('log.db'):
            pass
        else:
            self.pushLoad.setEnabled(False)

        # 초기 승패 버튼 사용불가
        self.radioWin.setEnabled(False)
        self.radioLose.setEnabled(False)

        # 초기 기간 버튼 사용불가
        self.radioRecordAll.setEnabled(False)
        self.radioRecordNow.setEnabled(False)
        self.radioToday.setEnabled(False)

        # 초기 직업탭 기간 버튼 사용불가
        self.radioJobAll.setEnabled(False)
        self.radioJobPeriod.setEnabled(False)
        self.radioJobOOT.setEnabled(False)
        self.radioJobOOTMini.setEnabled(False)

        # 초기 덱별 승률 탭 버튼 사용불가
        self.radioDeckAll.setEnabled(False)
        self.radioDeckPeriod.setEnabled(False)
        self.radioDeckOOT.setEnabled(False)
        self.radioDeckOOTMini.setEnabled(False)
        self.radioDeckRate.setEnabled(False)
        self.radioDeckVS.setEnabled(False)

        # 초기 덱별 전적 탭 버튼 사용불가
        self.radioDeckRPeriod.setEnabled(False)
        self.radioDeckROOT.setEnabled(False)
        self.radioDeckROOTMini.setEnabled(False)

        # 날짜 위젯 현재 날짜로 초기화
        self.dateEdit.setDate(datetime.today())
        self.dateJobStart.setDate(datetime.today())
        self.dateJobEnd.setDate(datetime.today())
        self.dateDeckStart.setDate(datetime.today())
        self.dateDeckEnd.setDate(datetime.today())
        self.dateDeckRStart.setDate(datetime.today())
        self.dateDeckREnd.setDate(datetime.today())

        # 모드 버튼
        self.radioRecRota.clicked.connect(self.radMod)
        self.radioRecUnli.clicked.connect(self.radMod)

        # 선후공 버튼
        self.radioFirst.clicked.connect(self.radFS)
        self.radioSecond.clicked.connect(self.radFS)

        # 승패 버튼
        self.radioWin.clicked.connect(self.radWinLose)
        self.radioLose.clicked.connect(self.radWinLose)

        # 날짜 버튼
        self.dateEdit.dateChanged.connect(self.dateUpdate)

        # 카드팩 버튼
        self.radioRecordOOT.clicked.connect(self.radRecCCP)
        self.radioRecordOOTMini.clicked.connect(self.radRecCCP)

        # 내 직업 버튼
        self.radioRoyalMy.clicked.connect(self.radioMyjob)
        self.radioWitchMy.clicked.connect(self.radioMyjob)
        self.radioElfMy.clicked.connect(self.radioMyjob)
        self.radioBishopMy.clicked.connect(self.radioMyjob)
        self.radioDragonMy.clicked.connect(self.radioMyjob)
        self.radioNecroMy.clicked.connect(self.radioMyjob)
        self.radioVampMy.clicked.connect(self.radioMyjob)
        self.radioNemeMy.clicked.connect(self.radioMyjob)

        # 내 아키타입 버튼
        self.comboArcheMy.currentIndexChanged.connect(self.cbMyArche)

        # 상대 직업 버튼
        self.radioRoyalOppo.clicked.connect(self.radioOppojob)
        self.radioWitchOppo.clicked.connect(self.radioOppojob)
        self.radioElfOppo.clicked.connect(self.radioOppojob)
        self.radioBishopOppo.clicked.connect(self.radioOppojob)
        self.radioDragonOppo.clicked.connect(self.radioOppojob)
        self.radioNecroOppo.clicked.connect(self.radioOppojob)
        self.radioVampOppo.clicked.connect(self.radioOppojob)
        self.radioNemeOppo.clicked.connect(self.radioOppojob)

        # 상대 아키타입 버튼
        self.comboArcheOppo.currentIndexChanged.connect(self.cbOppoArche)

        # 등록 버튼
        self.pushRegist.clicked.connect(self.writeRecord)

        # 로드 버튼
        self.pushLoad.clicked.connect(self.loadData)

        # 삭제 버튼
        self.pushErase.clicked.connect(self.eraseData)

        # 초기화 버튼
        self.pushInitailize.clicked.connect(self.initData)

        # 전적 기간 버튼
        self.radioRecordAll.clicked.connect(self.recordperiod)
        self.radioRecordNow.clicked.connect(self.recordperiod)
        self.radioToday.clicked.connect(self.recordperiod)

        # 직업별 모드 버튼
        self.radioJobRota.clicked.connect(self.jobmodbtn)
        self.radioJobUnli.clicked.connect(self.jobmodbtn)

        # 직업별 기간 버튼
        self.radioJobAll.clicked.connect(self.jobperiod)
        self.radioJobPeriod.clicked.connect(self.jobperiod)
        self.radioJobOOT.clicked.connect(self.jobperiod)
        self.radioJobOOTMini.clicked.connect(self.jobperiod)

        # 직업별 날짜 버튼
        self.dateJobStart.dateChanged.connect(self.jobdateUpdate)
        self.dateJobEnd.dateChanged.connect(self.jobdateUpdate)

        # 덱별 승률 모드 버튼
        self.radioDeckRota.clicked.connect(self.deckmodbtn)
        self.radioDeckUnli.clicked.connect(self.deckmodbtn)

        # 덱별 승률 기간 버튼
        self.radioDeckAll.clicked.connect(self.deckperiod)
        self.radioDeckPeriod.clicked.connect(self.deckperiod)
        self.radioDeckOOT.clicked.connect(self.deckperiod)
        self.radioDeckOOTMini.clicked.connect(self.deckperiod)

        # 덱별 승률 날짜 버튼
        self.dateDeckStart.dateChanged.connect(self.deckdateUpdate)
        self.dateDeckEnd.dateChanged.connect(self.deckdateUpdate)

        # 덱별 승률 정렬 버튼
        self.radioDeckVS.clicked.connect(self.sortdeck)
        self.radioDeckRate.clicked.connect(self.sortdeck)

        # 덱별 승률 스핀박스
        self.spinBox.valueChanged.connect(self.sortlimupdate)

        # 덱별 전적 모드 버튼
        self.radioDeckRRota.clicked.connect(self.deckrmodbtn)
        self.radioDeckRUnli.clicked.connect(self.deckrmodbtn)

        # 덱별 전적 기간 버튼
        self.radioDeckRPeriod.clicked.connect(self.deckrperiod)
        self.radioDeckROOT.clicked.connect(self.deckrperiod)
        self.radioDeckROOTMini.clicked.connect(self.deckrperiod)

        # 덱별 전적 날짜 버튼
        self.dateDeckRStart.dateChanged.connect(self.deckrdateUpdate)
        self.dateDeckREnd.dateChanged.connect(self.deckrdateUpdate)

        # 덱별 전적 아키타입 버튼
        self.comboDeckR.currentIndexChanged.connect(self.cbRecArche)

        # 덱별 전적 로드 버튼
        self.pushRLoad.clicked.connect(self.recload)

        # 그래프 공간
        self.figure = plt.figure()
        self.canvas1 = FigureCanvas(self.figure)
        self.RotaLayout.addWidget(self.canvas1)
        self.canvas2 = FigureCanvas(self.figure)
        self.UnliLayout.addWidget(self.canvas2)
        self.canvas3 = FigureCanvas(self.figure)
        self.ElfLayout.addWidget(self.canvas3)
        self.canvas4 = FigureCanvas(self.figure)
        self.RoyalLayout.addWidget(self.canvas4)
        self.canvas5 = FigureCanvas(self.figure)
        self.WitchLayout.addWidget(self.canvas5)
        self.canvas6 = FigureCanvas(self.figure)
        self.BishopLayout.addWidget(self.canvas6)
        self.canvas7 = FigureCanvas(self.figure)
        self.NecroLayout.addWidget(self.canvas7)
        self.canvas8 = FigureCanvas(self.figure)
        self.DragonLayout.addWidget(self.canvas8)
        self.canvas9 = FigureCanvas(self.figure)
        self.VampLayout.addWidget(self.canvas9)
        self.canvas10 = FigureCanvas(self.figure)
        self.NemeLayout.addWidget(self.canvas10)
        self.canvas11 = FigureCanvas(self.figure)
        self.DeckLayout1.addWidget(self.canvas11)
        self.canvas12 = FigureCanvas(self.figure)
        self.DeckLayout2.addWidget(self.canvas12)
        self.canvas13 = FigureCanvas(self.figure)
        self.DeckLayout3.addWidget(self.canvas13)
        self.canvas14 = FigureCanvas(self.figure)
        self.DeckLayout4.addWidget(self.canvas14)
        self.canvas15 = FigureCanvas(self.figure)
        self.DeckLayout5.addWidget(self.canvas15)
        self.canvas16 = FigureCanvas(self.figure)
        self.DeckLayout6.addWidget(self.canvas16)
        self.canvas17 = FigureCanvas(self.figure)
        self.DeckLayout7.addWidget(self.canvas17)
        self.canvas18 = FigureCanvas(self.figure)
        self.DeckLayout8.addWidget(self.canvas18)
        self.canvas19 = FigureCanvas(self.figure)
        self.DeckRLayout1.addWidget(self.canvas19)
        self.font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=self.font_name)
        font_manager.FontProperties().set_size('xx-small')
        style.use('ggplot')

        # 아이콘 설정
        self.setWindowIcon(QtGui.QIcon(resource_path('SVRT.png')))

    first_second, win_lose, logdate, logccp = '', '', datetime.today().strftime("%Y-%m-%d"), 'OOT+'
    myjob, myarche, oppojob, oppoarche, mod = '', '', '', '', '로테이션'
    myjob_num, oppojob_num = 0, 0
    first_load, fscheck, wlcheck = 0, 0, 0
    df = pd.DataFrame()  # 전체 데이터
    df1 = pd.DataFrame()  # 직업별 / 기간, 모드 검색 후
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df4 = pd.DataFrame()
    df5 = pd.DataFrame()
    df6 = pd.DataFrame()
    recordmod = 0
    today = datetime.today().strftime("%Y-%m-%d")
    jobmod, jobdate, jobstartdate = '', 'OOT+', datetime.today().strftime("%Y-%m-%d")
    jobenddate = jobstartdate
    deckmod, deckdate, deckstartdate = '', 'OOT+', datetime.today().strftime("%Y-%m-%d")
    deckenddate = deckstartdate
    sortlim = 5
    periodcheck, jobdatecheck = 0, 0
    jobmodcheck, deckmodcheck, deckrmodcheck = 0, 0, 0
    deckrmod, deckrdate, deckrstartdate = '', 'OOT+', datetime.today().strftime("%Y-%m-%d")
    deckrenddate = deckrstartdate
    deckrarche = ''

    # 덱 타입 (순서는 로얄, 위치, 엘프, 비숍, 드래곤, 네크, 뱀파, 네메)
    dt_oot_rota = [
        ["미드로얄", "로얄(기타)"],
        ["거대키마이라위치", "마나리아위치", "개벽위치", "위치(기타)"],
        ["템포엘프", "변종엘프", "엘프(기타)"],
        ["천호신사비숍", "치천사비숍", "성사자비숍", "비숍(기타)"],
        ["용술사드래곤", "램프드래곤", "린드부름드래곤", "마젤베인드래곤", "드래곤(기타)"],
        ["미드네크", "장송네크", "네크(기타)"],
        ["어먹박뱀파", "어그로뱀파", "요르문간드뱀파", "뱀파(기타)"],
        ["아티팩트네메", "리셰나네메", "꼭두각시네메", "포격네메", "네메(기타)"]
    ]
    dt_oot_unli = [
        ["어그로로얄", "수호로얄", "미드로얄", "로얄(기타)"],
        ["초월위치", "마나리아위치", "도로시위치", "위치(기타)"],
        ["리노엘프", "어그로엘프", "엘프(기타)"],
        ["천호신사비숍", "치천사비숍", "에일라비숍", "신성술사비숍", "비숍(기타)"],
        ["어그로드래곤", "램프드래곤", "마젤베인드래곤", "드래곤(기타)"],
        ["미드네크", "장송네크", "네크(기타)"],
        ["어먹박뱀파", "어그로뱀파", "복수뱀파", "뱀파(기타)"],
        ["아티팩트네메", "리셰나네메", "꼭두각시네메", "포격네메", "네메(기타)"]
    ]
    dt_ootm_rota = [
        ["미드로얄", "로얄(기타)"],
        ["마나리아위치", "거대키마이라위치", "비술위치", "위치(기타)"],
        ["템포엘프", "변종엘프", "어그로엘프", "엘프(기타)"],
        ["성사자비숍", "천호신사비숍", "치천사비숍", "비숍(기타)"],
        ["용술사드래곤", "램프드래곤", "마젤베인드래곤", "린드부름드래곤", "드래곤(기타)"],
        ["미드네크", "장송네크", "네크(기타)"],
        ["어먹박뱀파", "어그로뱀파", "요르문간드뱀파", "뱀파(기타)"],
        ["아티팩트네메", "리셰나네메", "꼭두각시네메", "네메(기타)"]
    ]
    dt_ootm_unli = [
        ["어그로로얄", "철벽로얄", "미드로얄", "로얄(기타)"],
        ["마나리아위치", "도로시위치", "비술위치", "초월위치", "위치(기타)"],
        ["리노엘프", "어그로엘프", "중립엘프", "엘프(기타)"],
        ["천호신사비숍", "치천사비숍", "에일라비숍", "신성술사비숍", "비숍(기타)"],
        ["페이스드래곤", "램프드래곤", "용소녀드래곤", "봉황조이드래곤", "마젤베인드래곤", "드래곤(기타)"],
        ["미드네크", "네프티스네크", "장송네크", "네크(기타)"],
        ["어먹박뱀파", "어그로뱀파", "복수뱀파", "뱀파(기타)"],
        ["아티팩트네메", "리셰나네메", "꼭두각시네메", "포격네메", "네메(기타)"]
    ]

    # 모드 버튼 이벤트
    def radMod(self):
        if self.radioRecRota.isChecked():
            mod = '로테이션'
        elif self.radioRecUnli.isChecked():
            mod = '언리미티드'
        myWindow.mod = mod
        self.radioMyjob()
        self.radioOppojob()

    # 선후공 버튼 이벤트
    def radFS(self):
        if self.radioFirst.isChecked():
            fs = '선공'
        elif self.radioSecond.isChecked():
            fs = '후공'
        myWindow.first_second = fs
        if myWindow.fscheck == 0:
            self.radioWin.setEnabled(True)
            self.radioLose.setEnabled(True)
            myWindow.fscheck = 1

    # 승패 버튼 이벤트
    def radWinLose(self):
        if self.radioWin.isChecked():
            winlose = '승'
        elif self.radioLose.isChecked():
            winlose = '패'
        myWindow.win_lose = winlose
        if myWindow.wlcheck == 0:
            self.pushRegist.setEnabled(True)
            myWindow.wlcheck = 1

    # 날짜 버튼 이벤트
    def dateUpdate(self):
        temp_date = self.dateEdit.date()
        myWindow.logdate = temp_date.toPyDate()

    # 카드팩 버튼 이벤트
    def radRecCCP(self):
        if self.radioRecordOOT.isChecked():
            logccp = 'OOT'
        elif self.radioRecordOOTMini.isChecked():
            logccp = 'OOT+'
        myWindow.logccp = logccp

    # 내 직업
    def radioMyjob(self):
        if self.radioRoyalMy.isChecked():
            myjob = '로얄'
            myjob_num = 0
        elif self.radioWitchMy.isChecked():
            myjob = '위치'
            myjob_num = 1
        elif self.radioElfMy.isChecked():
            myjob = '엘프'
            myjob_num = 2
        elif self.radioBishopMy.isChecked():
            myjob = '비숍'
            myjob_num = 3
        elif self.radioDragonMy.isChecked():
            myjob = '드래곤'
            myjob_num = 4
        elif self.radioNecroMy.isChecked():
            myjob = '네크로맨서'
            myjob_num = 5
        elif self.radioVampMy.isChecked():
            myjob = '뱀파이어'
            myjob_num = 6
        elif self.radioNemeMy.isChecked():
            myjob = '네메시스'
            myjob_num = 7
        else:
            return
        myWindow.myjob = myjob
        if myWindow.mod == '로테이션':
            if myWindow.logccp == 'OOT':
                archelist = myWindow.dt_oot_rota[myjob_num]
            elif myWindow.logccp == 'OOT+':
                archelist = myWindow.dt_ootm_rota[myjob_num]
            else:
                return
        elif myWindow.mod == '언리미티드':
            if myWindow.logccp == 'OOT':
                archelist = myWindow.dt_oot_unli[myjob_num]
            elif myWindow.logccp == 'OOT+':
                archelist = myWindow.dt_ootm_unli[myjob_num]
            else:
                return
        else:
            return
        self.comboArcheMy.clear()
        self.comboArcheMy.addItems(archelist)

    # 내 아키타입
    def cbMyArche(self):
        myWindow.myarche = self.comboArcheMy.currentText()

    # 상대 직업
    def radioOppojob(self):
        if self.radioRoyalOppo.isChecked():
            oppojob = '로얄'
            oppojob_num = 0
        elif self.radioWitchOppo.isChecked():
            oppojob = '위치'
            oppojob_num = 1
        elif self.radioElfOppo.isChecked():
            oppojob = '엘프'
            oppojob_num = 2
        elif self.radioBishopOppo.isChecked():
            oppojob = '비숍'
            oppojob_num = 3
        elif self.radioDragonOppo.isChecked():
            oppojob = '드래곤'
            oppojob_num = 4
        elif self.radioNecroOppo.isChecked():
            oppojob = '네크로맨서'
            oppojob_num = 5
        elif self.radioVampOppo.isChecked():
            oppojob = '뱀파이어'
            oppojob_num = 6
        elif self.radioNemeOppo.isChecked():
            oppojob = '네메시스'
            oppojob_num = 7
        else:
            return
        myWindow.oppojob = oppojob
        if myWindow.mod == '로테이션':
            if myWindow.logccp == 'OOT':
                archelist = myWindow.dt_oot_rota[oppojob_num]
            elif myWindow.logccp == 'OOT+':
                archelist = myWindow.dt_ootm_rota[oppojob_num]
            else:
                return
        elif myWindow.mod == '언리미티드':
            if myWindow.logccp == 'OOT':
                archelist = myWindow.dt_oot_unli[oppojob_num]
            elif myWindow.logccp == 'OOT+':
                archelist = myWindow.dt_ootm_unli[oppojob_num]
            else:
                return
        else:
            return
        self.comboArcheOppo.clear()
        self.comboArcheOppo.addItems(archelist)

    # 상대 아키타입
    def cbOppoArche(self):
        myWindow.oppoarche = self.comboArcheOppo.currentText()

    # 등록 버튼 / 아키타입 한번 더 로드할것!
    def writeRecord(self):
        Date = myWindow.logdate
        CP = myWindow.logccp
        Mod = myWindow.mod
        MyJob = myWindow.myjob
        MyAr = myWindow.myarche
        OpJob = myWindow.oppojob
        OpAr = myWindow.oppoarche
        FirSec = myWindow.first_second
        WinLose = myWindow.win_lose
        RegistTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if MyJob == '':
            QMessageBox.about(self, '주의', '내 덱을 선택해주세요.')
            return
        elif OpJob == '':
            QMessageBox.about(self, '주의', '상대 덱을 선택해주세요.')
            return
        record = [Date, CP, Mod, MyJob, MyAr, OpJob, OpAr, FirSec, WinLose, RegistTime]
        conn = sqlite3.connect('log.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", record)
        conn.commit()
        conn.close()
        self.loadData()
        if Mod == '로테이션':
            self.rotaAllVS()
        elif Mod == '언리미티드':
            self.unliAllVS()
        else:
            return

    # 데이터 로드
    def loadData(self):
        conn = sqlite3.connect('log.db')
        myWindow.df = pd.read_sql("SELECT * FROM log", conn)
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM log ORDER BY RegistTime DESC LIMIT 10")
        rows = result.fetchall()
        rowcntquery = cursor.execute("SELECT * FROM log")
        rowcnt = rowcntquery.fetchall()
        sbmsg = '{0}개 기록 검색됨'.format(len(rowcnt))
        if len(rowcnt) < 10:
            self.tableRecord.setRowCount(len(rowcnt))
        for i, row in enumerate(rows):
            for j, data in enumerate(row):
                item = QTableWidgetItem()
                item.setText(str(data))
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.tableRecord.setItem(i, j, item)
        conn.close()
        self.tableRecord.resizeColumnsToContents()
        self.statusBar().showMessage(sbmsg)
        self.recordperiod()
        if myWindow.first_load == 0:
            self.pushErase.setEnabled(True)
            self.radioRecordAll.setEnabled(True)
            self.radioRecordNow.setEnabled(True)
            self.radioToday.setEnabled(True)
            self.tab_2.setEnabled(True)
            self.tab_3.setEnabled(True)
            self.tab_4.setEnabled(True)
            myWindow.first_load = 1

    # 데이터 삭제 - 최신 1개만
    def eraseData(self):
        conn = sqlite3.connect('log.db')
        cursor = conn.cursor()
        result = cursor.execute("SELECT RegistTime FROM log ORDER BY RegistTime DESC LIMIT 1")
        edata = result.fetchall()
        cursor.execute("DELETE FROM log WHERE RegistTime=?", edata[0])
        conn.commit()
        conn.close()
        self.loadData()

    # 초기화
    def initData(self):
        if os.path.isfile('log.db'):
            msgbox = QMessageBox
            ret = msgbox.question(self, '경고', '정말 기록을 초기화하겠습니까?')
            if ret == QMessageBox.Yes:
                os.remove('log.db')
            elif ret == QMessageBox.No:
                return
        conn = sqlite3.connect('log.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE log(Date text, CardPack text, Mod TEXT, MyJob text, MyArche text, OppoJob text, OppoArche text, FirstSecond text, WinLose text, RegistTime TEXT)")
        conn.commit()
        myWindow.df4 = pd.read_sql("SELECT * FROM log", conn)
        conn.close()
        self.tableRecord.setRowCount(0)
        self.rotaAllVS()
        self.unliAllVS()
        self.pushLoad.setEnabled(True)

    # 전적 기간
    def recordperiod(self):
        df = myWindow.df
        if self.radioRecordAll.isChecked():
            pass
        elif self.radioRecordNow.isChecked():
            df = df[df['CardPack'].isin(['OOT+'])]
        elif self.radioToday.isChecked():
            df = df[df['Date'].isin([myWindow.today])]
        myWindow.df4 = df
        self.rotaAllVS()
        self.unliAllVS()
        self.figure.clear()

    # 로테이션 전적
    def rotaAllVS(self):
        df = myWindow.df4
        df1 = df[df['Mod'].isin(['로테이션'])]
        vscount = len(df1)
        if vscount == 0:
            self.RotaVSCount.setText('전적없음')
            self.RotaWinCount.setText('N/A')
            self.RotaLoseCount.setText('N/A')
            self.RotaFirst.setText('N/A')
            self.RotaSecond.setText('N/A')
            self.figure.clear()
            self.canvas1.draw()
        else:
            self.RotaVSCount.setText(str(vscount))
            result = df1[df1['WinLose'].isin(['승'])]
            wincount = len(result)
            self.RotaWinCount.setText(str(wincount))
            result = df1[df1['WinLose'].isin(['패'])]
            losecount = len(result)
            self.RotaLoseCount.setText(str(losecount))
            self.rotaallplot(wincount, losecount)
            first = df1[df1['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df1[df1['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.RotaFirst.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.RotaFirst.setText(wr1st)
            if len(second) == 0:
                self.RotaSecond.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.RotaSecond.setText(wr2nd)

    # 언리미티드 전적
    def unliAllVS(self):
        df = myWindow.df4
        df1 = df[df['Mod'].isin(['언리미티드'])]
        vscount = len(df1)
        if vscount == 0:
            self.UnliVSCount.setText('전적없음')
            self.UnliWinCount.setText('N/A')
            self.UnliLoseCount.setText('N/A')
            self.UnliFirst.setText('N/A')
            self.UnliSecond.setText('N/A')
            self.figure.clear()
            self.canvas2.draw()
        else:
            self.UnliVSCount.setText(str(vscount))
            result = df1[df1['WinLose'].isin(['승'])]
            wincount = len(result)
            self.UnliWinCount.setText(str(wincount))
            result = df1[df1['WinLose'].isin(['패'])]
            losecount = len(result)
            self.UnliLoseCount.setText(str(losecount))
            self.unliallplot(wincount, losecount)
            first = df1[df1['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df1[df1['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.UnliFirst.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.UnliFirst.setText(wr1st)
            if len(second) == 0:
                self.UnliSecond.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.UnliSecond.setText(wr2nd)

    # 로테이션 그래프 in 전적관리
    def rotaallplot(self, a, b):
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [a, b]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas1.draw()

    # 언리미티드 그래프 in 전적관리
    def unliallplot(self, a, b):
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [a, b]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas2.draw()

    # 모드버튼 in 직업별
    def jobmodbtn(self):
        if self.radioJobRota.isChecked():
            myWindow.jobmod = '로테이션'
            self.groupJobRecord.setTitle('기간 내 로테이션 전적')
        elif self.radioJobUnli.isChecked():
            myWindow.jobmod = '언리미티드'
            self.groupJobRecord.setTitle('기간 내 언리미티드 전적')
        if myWindow.jobmodcheck == 0:
            self.radioJobAll.setEnabled(True)
            self.radioJobOOT.setEnabled(True)
            self.radioJobPeriod.setEnabled(True)
            self.radioJobOOT.setEnabled(True)
            self.radioJobOOTMini.setEnabled(True)
            myWindow.jobmodcheck = 1
        self.jobperiod()
        self.jobrecordupdate()

    # 전적 갱신 in 직업별
    def jobrecordupdate(self):
        df = myWindow.df1
        if len(df) == 0:
            self.JobVS.setText('전적없음')
            self.JobWin.setText('N/A')
            self.JobLose.setText('N/A')
            self.JobWinRate.setText('N/A')
            return
        win = df[df['WinLose'].isin(['승'])]
        lose = df[df['WinLose'].isin(['패'])]
        winrate = str(round(len(win) * 100 / len(df), 1)) + '%'
        self.JobVS.setText(str(len(df)))
        self.JobWin.setText(str(len(win)))
        self.JobLose.setText(str(len(lose)))
        self.JobWinRate.setText(winrate)

    # 기간버튼 in 직업별
    def jobperiod(self):
        df1 = myWindow.df
        if self.radioJobAll.isChecked():
            myWindow.jobdate = '전체'
            df2 = df1
        elif self.radioJobPeriod.isChecked():
            myWindow.jobdate = '기간'
            df2 = df1[(df1['Date'] >= myWindow.jobstartdate) & (df1['Date'] <= myWindow.jobenddate)]
        elif self.radioJobOOT.isChecked():
            myWindow.jobdate = 'OOT'
            df2 = df1[df1['CardPack'].isin(['OOT'])]
        elif self.radioJobOOTMini.isChecked():
            myWindow.jobdate = 'OOT+'
            df2 = df1[df1['CardPack'].isin(['OOT+'])]
        if myWindow.jobmod == '로테이션':
            df3 = df2[df2['Mod'].isin(['로테이션'])]
        elif myWindow.jobmod == '언리미티드':
            df3 = df2[df2['Mod'].isin(['언리미티드'])]
        myWindow.df1 = df3
        self.jobrecordupdate()
        self.elf()
        self.royal()
        self.witch()
        self.bishop()
        self.necro()
        self.dragon()
        self.vamp()
        self.neme()
        self.figure.clear()

    # 날짜변경 in 직업별
    def jobdateUpdate(self):
        temp_date = self.dateJobStart.date()
        myWindow.jobstartdate = str(temp_date.toPyDate())
        temp_date1 = self.dateJobEnd.date()
        myWindow.jobenddate = str(temp_date1.toPython())

    def elf(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['엘프'])]
        if len(df) == 0:
            self.ElfVSCount.setText('전적없음')
            self.ElfWinCount.setText('N/A')
            self.ElfLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas3.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.ElfVSCount.setText(str(len(df)))
        self.ElfWinCount.setText(str(win))
        self.ElfLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas3.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.ElfFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.ElfFirst.setText(wr1st)
        if len(second) == 0:
            self.ElfSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.ElfSecond.setText(wr2nd)

    def royal(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['로얄'])]
        if len(df) == 0:
            self.RoyalVSCount.setText('전적없음')
            self.RoyalWinCount.setText('N/A')
            self.RoyalLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas4.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.RoyalVSCount.setText(str(len(df)))
        self.RoyalWinCount.setText(str(win))
        self.RoyalLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas4.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.RoyalFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.RoyalFirst.setText(wr1st)
        if len(second) == 0:
            self.RoyalSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.RoyalSecond.setText(wr2nd)

    def witch(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['위치'])]
        if len(df) == 0:
            self.WitchVSCount.setText('전적없음')
            self.WitchWinCount.setText('N/A')
            self.WitchLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas5.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.WitchVSCount.setText(str(len(df)))
        self.WitchWinCount.setText(str(win))
        self.WitchLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas5.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.WitchFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.WitchFirst.setText(wr1st)
        if len(second) == 0:
            self.WitchSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.WitchSecond.setText(wr2nd)

    def bishop(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['비숍'])]
        if len(df) == 0:
            self.BishopVSCount.setText('전적없음')
            self.BishopWinCount.setText('N/A')
            self.BishopLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas6.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.BishopVSCount.setText(str(len(df)))
        self.BishopWinCount.setText(str(win))
        self.BishopLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas6.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.BishopFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.BishopFirst.setText(wr1st)
        if len(second) == 0:
            self.BishopSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.BishopSecond.setText(wr2nd)

    def necro(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['네크로맨서'])]
        if len(df) == 0:
            self.NecroVSCount.setText('전적없음')
            self.NecroWinCount.setText('N/A')
            self.NecroLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas7.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.NecroVSCount.setText(str(len(df)))
        self.NecroWinCount.setText(str(win))
        self.NecroLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas7.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.NecroFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.NecroFirst.setText(wr1st)
        if len(second) == 0:
            self.NecroSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.NecroSecond.setText(wr2nd)

    def dragon(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['드래곤'])]
        if len(df) == 0:
            self.DragonVSCount.setText('전적없음')
            self.DragonWinCount.setText('N/A')
            self.DragonLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas8.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.DragonVSCount.setText(str(len(df)))
        self.DragonWinCount.setText(str(win))
        self.DragonLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas8.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.DragonFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.DragonFirst.setText(wr1st)
        if len(second) == 0:
            self.DragonSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.DragonSecond.setText(wr2nd)

    def vamp(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['뱀파이어'])]
        if len(df) == 0:
            self.VampVSCount.setText('전적없음')
            self.VampWinCount.setText('N/A')
            self.VampLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas9.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.VampVSCount.setText(str(len(df)))
        self.VampWinCount.setText(str(win))
        self.VampLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas9.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.VampFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.VampFirst.setText(wr1st)
        if len(second) == 0:
            self.VampSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.VampSecond.setText(wr2nd)

    def neme(self):
        df = myWindow.df1
        df = df[df['MyJob'].isin(['네메시스'])]
        if len(df) == 0:
            self.NemeVSCount.setText('전적없음')
            self.NemeWinCount.setText('N/A')
            self.NemeLoseCount.setText('N/A')
            self.figure.clear()
            self.canvas10.draw()
            return
        win = len(df[df['WinLose'].isin(['승'])])
        lose = len(df[df['WinLose'].isin(['패'])])
        self.NemeVSCount.setText(str(len(df)))
        self.NemeWinCount.setText(str(win))
        self.NemeLoseCount.setText(str(lose))
        colors = ['lightskyblue', 'red']
        labels = ['승', '패']
        ratio = [win, lose]
        self.figure.clear()
        plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.canvas10.draw()
        first = df[df['FirstSecond'].isin(['선공'])]
        firstwin = first[first['WinLose'].isin(['승'])]
        second = df[df['FirstSecond'].isin(['후공'])]
        secondwin = second[second['WinLose'].isin(['승'])]
        if len(first) == 0:
            self.NemeFirst.setText('N/A')
        else:
            wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
            self.NemeFirst.setText(wr1st)
        if len(second) == 0:
            self.NemeSecond.setText('N/A')
        else:
            wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
            self.NemeSecond.setText(wr2nd)

    # 모드버튼 in 직업별
    def deckmodbtn(self):
        if self.radioDeckRota.isChecked():
            myWindow.deckmod = '로테이션'
            self.groupDeckRecord.setTitle('기간 내 로테이션 전적')
        elif self.radioDeckUnli.isChecked():
            myWindow.deckmod = '언리미티드'
            self.groupDeckRecord.setTitle('기간 내 언리미티드 전적')
        if myWindow.deckmodcheck == 0:
            self.radioDeckAll.setEnabled(True)
            self.radioDeckPeriod.setEnabled(True)
            self.radioDeckOOT.setEnabled(True)
            self.radioDeckOOTMini.setEnabled(True)
            self.radioDeckRate.setEnabled(True)
            self.radioDeckVS.setEnabled(True)
            myWindow.deckmodcheck = 1
        self.deckperiod()
        self.deckrecordupdate()

    def deckrecordupdate(self):
        df = myWindow.df2
        if len(df) == 0:
            self.DeckVS.setText('전적없음')
            self.DeckWin.setText('N/A')
            self.DeckLose.setText('N/A')
            self.DeckWinRate.setText('N/A')
            return
        win = df[df['WinLose'].isin(['승'])]
        lose = df[df['WinLose'].isin(['패'])]
        winrate = str(round(len(win) * 100 / len(df), 1)) + '%'
        self.DeckVS.setText(str(len(df)))
        self.DeckWin.setText(str(len(win)))
        self.DeckLose.setText(str(len(lose)))
        self.DeckWinRate.setText(winrate)

    # 기간버튼 in 직업별
    def deckperiod(self):
        df1 = myWindow.df
        if self.radioDeckAll.isChecked():
            myWindow.deckdate = '전체'
            df2 = df1
        elif self.radioDeckPeriod.isChecked():
            myWindow.deckdate = '기간'
            df2 = df1[(df1['Date'] >= myWindow.deckstartdate) & (df1['Date'] <= myWindow.deckenddate)]
        elif self.radioDeckOOT.isChecked():
            myWindow.deckdate = 'OOT'
            df2 = df1[df1['CardPack'].isin(['OOT'])]
        elif self.radioDeckOOTMini.isChecked():
            myWindow.deckdate = 'OOT+'
            df2 = df1[df1['CardPack'].isin(['OOT+'])]
        if myWindow.deckmod == '로테이션':
            df3 = df2[df2['Mod'].isin(['로테이션'])]
        elif myWindow.deckmod == '언리미티드':
            df3 = df2[df2['Mod'].isin(['언리미티드'])]
        myWindow.df2 = df3
        self.deckrecordupdate()
        df4 = df3.drop_duplicates(['MyArche'])
        lists = list(set(df4['MyArche']))
        dict = {}

        for deck in lists:
            record = []
            vs = df3[df3['MyArche'].isin([deck])]
            win = vs[vs['WinLose'].isin(['승'])]
            lose = vs[vs['WinLose'].isin(['패'])]
            record.append(len(vs))
            record.append(len(win))
            record.append(len(lose))
            record.append(round(len(win) * 100 / len(vs), 1))
            dict[deck] = record
        myWindow.df3 = pd.DataFrame.from_dict(dict, orient='index', columns=['VS', 'Win', 'Lose', 'WinRate'])
        self.sortdeck()

    def sortdeck(self):
        if self.radioDeckRate.isChecked():
            df = myWindow.df3.sort_values(['WinRate'], ascending=[False])
            df = df.loc[df['VS'] >= myWindow.sortlim, :]
        elif self.radioDeckVS.isChecked():
            df = myWindow.df3.sort_values(['VS'], ascending=[False])
        self.deck1(df)
        self.deck2(df)
        self.deck3(df)
        self.deck4(df)
        self.deck5(df)
        self.deck6(df)
        self.deck7(df)
        self.deck8(df)
        self.figure.clear()

    def sortlimupdate(self):
        myWindow.sortlim = self.spinBox.value()

    def deck1(self, df):
        if len(df) >= 1:
            name = df.index[0]
            self.groupDeck1.setTitle(name)
            self.Deck1VSCount.setText(str(df.iloc[0, 0]))
            self.Deck1WinCount.setText(str(df.iloc[0, 1]))
            self.Deck1LoseCount.setText(str(df.iloc[0, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[0, 1], df.iloc[0, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas11.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck1First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck1First.setText(wr1st)
            if len(second) == 0:
                self.Deck1Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck1Second.setText(wr2nd)
        else:
            self.groupDeck1.setTitle('N/A')
            self.Deck1VSCount.setText('전적없음')
            self.Deck1WinCount.setText('N/A')
            self.Deck1LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas11.draw()
            return

    def deck2(self, df):
        if len(df) >= 2:
            name = df.index[1]
            self.groupDeck2.setTitle(name)
            self.Deck2VSCount.setText(str(df.iloc[1, 0]))
            self.Deck2WinCount.setText(str(df.iloc[1, 1]))
            self.Deck2LoseCount.setText(str(df.iloc[1, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[1, 1], df.iloc[1, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas12.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck2First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck2First.setText(wr1st)
            if len(second) == 0:
                self.Deck2Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck2Second.setText(wr2nd)
        else:
            self.groupDeck2.setTitle('N/A')
            self.Deck2VSCount.setText('전적없음')
            self.Deck2WinCount.setText('N/A')
            self.Deck2LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas12.draw()
            return

    def deck3(self, df):
        if len(df) >= 3:
            name = df.index[2]
            self.groupDeck3.setTitle(name)
            self.Deck3VSCount.setText(str(df.iloc[2, 0]))
            self.Deck3WinCount.setText(str(df.iloc[2, 1]))
            self.Deck3LoseCount.setText(str(df.iloc[2, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[2, 1], df.iloc[2, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas13.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck3First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck3First.setText(wr1st)
            if len(second) == 0:
                self.Deck3Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck3Second.setText(wr2nd)
        else:
            self.groupDeck3.setTitle('N/A')
            self.Deck3VSCount.setText('전적없음')
            self.Deck3WinCount.setText('N/A')
            self.Deck3LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas13.draw()
            return

    def deck4(self, df):
        if len(df) >= 4:
            name = df.index[3]
            self.groupDeck4.setTitle(name)
            self.Deck4VSCount.setText(str(df.iloc[3, 0]))
            self.Deck4WinCount.setText(str(df.iloc[3, 1]))
            self.Deck4LoseCount.setText(str(df.iloc[3, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[3, 1], df.iloc[3, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas14.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck4First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck4First.setText(wr1st)
            if len(second) == 0:
                self.Deck4Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck4Second.setText(wr2nd)
        else:
            self.groupDeck4.setTitle('N/A')
            self.Deck4VSCount.setText('전적없음')
            self.Deck4WinCount.setText('N/A')
            self.Deck4LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas14.draw()
            return

    def deck5(self, df):
        if len(df) >= 5:
            name = df.index[4]
            self.groupDeck5.setTitle(name)
            self.Deck5VSCount.setText(str(df.iloc[4, 0]))
            self.Deck5WinCount.setText(str(df.iloc[4, 1]))
            self.Deck5LoseCount.setText(str(df.iloc[4, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[4, 1], df.iloc[4, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas15.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck5First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck5First.setText(wr1st)
            if len(second) == 0:
                self.Deck5Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck5Second.setText(wr2nd)
        else:
            self.groupDeck5.setTitle('N/A')
            self.Deck5VSCount.setText('전적없음')
            self.Deck5WinCount.setText('N/A')
            self.Deck5LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas15.draw()
            return

    def deck6(self, df):
        if len(df) >= 6:
            name = df.index[5]
            self.groupDeck6.setTitle(name)
            self.Deck6VSCount.setText(str(df.iloc[5, 0]))
            self.Deck6WinCount.setText(str(df.iloc[5, 1]))
            self.Deck6LoseCount.setText(str(df.iloc[5, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[5, 1], df.iloc[5, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas16.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck6First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck6First.setText(wr1st)
            if len(second) == 0:
                self.Deck6Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck6Second.setText(wr2nd)
        else:
            self.groupDeck6.setTitle('N/A')
            self.Deck6VSCount.setText('전적없음')
            self.Deck6WinCount.setText('N/A')
            self.Deck6LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas16.draw()
            return

    def deck7(self, df):
        if len(df) >= 7:
            name = df.index[6]
            self.groupDeck7.setTitle(name)
            self.Deck7VSCount.setText(str(df.iloc[6, 0]))
            self.Deck7WinCount.setText(str(df.iloc[6, 1]))
            self.Deck7LoseCount.setText(str(df.iloc[6, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[6, 1], df.iloc[6, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas17.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck7First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck7First.setText(wr1st)
            if len(second) == 0:
                self.Deck7Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck7Second.setText(wr2nd)
        else:
            self.groupDeck7.setTitle('N/A')
            self.Deck7VSCount.setText('전적없음')
            self.Deck7WinCount.setText('N/A')
            self.Deck7LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas17.draw()
            return

    def deck8(self, df):
        if len(df) >= 8:
            name = df.index[7]
            self.groupDeck8.setTitle(name)
            self.Deck8VSCount.setText(str(df.iloc[7, 0]))
            self.Deck8WinCount.setText(str(df.iloc[7, 1]))
            self.Deck8LoseCount.setText(str(df.iloc[7, 2]))
            colors = ['lightskyblue', 'red']
            labels = ['승', '패']
            ratio = [df.iloc[7, 1], df.iloc[7, 2]]
            self.figure.clear()
            plt.pie(ratio, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            self.canvas18.draw()
            df = myWindow.df2
            df = df[df['MyArche'].isin([name])]
            first = df[df['FirstSecond'].isin(['선공'])]
            firstwin = first[first['WinLose'].isin(['승'])]
            second = df[df['FirstSecond'].isin(['후공'])]
            secondwin = second[second['WinLose'].isin(['승'])]
            if len(first) == 0:
                self.Deck8First.setText('N/A')
            else:
                wr1st = str(round(len(firstwin) * 100 / len(first), 1)) + '%'
                self.Deck8First.setText(wr1st)
            if len(second) == 0:
                self.Deck8Second.setText('N/A')
            else:
                wr2nd = str(round(len(secondwin) * 100 / len(second), 1)) + '%'
                self.Deck8Second.setText(wr2nd)
        else:
            self.groupDeck8.setTitle('N/A')
            self.Deck8VSCount.setText('전적없음')
            self.Deck8WinCount.setText('N/A')
            self.Deck8LoseCount.setText('N/A')
            self.figure.clear()
            self.canvas18.draw()
            return

    # 날짜변경 in 덱별 승률
    def deckdateUpdate(self):
        temp_date = self.dateDeckStart.date()
        myWindow.deckstartdate = str(temp_date.toPython())
        temp_date1 = self.dateDeckEnd.date()
        myWindow.deckenddate = str(temp_date1.toPython())

    # 모드 버튼 in 덱별 전적
    def deckrmodbtn(self):
        if self.radioDeckRRota.isChecked():
            myWindow.deckrmod = '로테이션'
        elif self.radioDeckUnli.isChecked():
            myWindow.deckrmod = '언리미티드'
        if myWindow.deckrmodcheck == 0:
            self.radioDeckRPeriod.setEnabled(True)
            self.radioDeckROOT.setEnabled(True)
            self.radioDeckROOTMini.setEnabled(True)
            myWindow.deckrmodcheck = 1
        self.deckrperiod()
        self.deckrrecordupdate()

    # 기간버튼 in 직업별
    def deckrperiod(self):
        df1 = myWindow.df
        if self.radioDeckRPeriod.isChecked():
            myWindow.deckrdate = '기간'
            df2 = df1[(df1['Date'] >= myWindow.deckrstartdate) & (df1['Date'] <= myWindow.deckrenddate)]
        elif self.radioDeckROOT.isChecked():
            myWindow.deckrdate = 'OOT'
            df2 = df1[df1['CardPack'].isin(['OOT'])]
        elif self.radioDeckROOTMini.isChecked():
            myWindow.deckrdate = 'OOT+'
            df2 = df1[df1['CardPack'].isin(['OOT+'])]
        if myWindow.deckrmod == '로테이션':
            df3 = df2[df2['Mod'].isin(['로테이션'])]
        elif myWindow.deckrmod == '언리미티드':
            df3 = df2[df2['Mod'].isin(['언리미티드'])]
        myWindow.df5 = df3
        df4 = df3.drop_duplicates(['MyArche'])
        lists = list(set(df4['MyArche']))
        self.comboDeckR.clear()
        self.comboDeckR.addItems(lists)
        self.deckrrecordupdate()

    # 날짜변경 in 덱별 전적
    def deckrdateUpdate(self):
        temp_date = self.dateDeckRStart.date()
        myWindow.deckrstartdate = str(temp_date.toPython())
        temp_date1 = self.dateDeckREnd.date()
        myWindow.deckrenddate = str(temp_date1.toPython())

    # 덱별 전적 아키타입
    def cbRecArche(self):
        myWindow.deckrarche = self.comboDeckR.currentText()
        self.deckrrecordupdate()

    def deckrrecordupdate(self):
        df = myWindow.df5
        df = df[df['MyArche'].isin([myWindow.deckrarche])]
        myWindow.df6 = df
        if len(df) == 0:
            self.DeckVS.setText('전적없음')
            self.DeckWin.setText('N/A')
            self.DeckLose.setText('N/A')
            self.DeckWinRate.setText('N/A')
            return
        win = df[df['WinLose'].isin(['승'])]
        lose = df[df['WinLose'].isin(['패'])]
        winrate = str(round(len(win) * 100 / len(df), 1)) + '%'
        self.DeckRVS.setText(str(len(df)))
        self.DeckRWin.setText(str(len(win)))
        self.DeckRLose.setText(str(len(lose)))
        self.DeckRWinRate.setText(winrate)

    def recload(self):
        self.tableDeckR1.setRowCount(0)
        self.tableDeckR2.setRowCount(0)
        self.fsgraph()
        self.relf()
        self.rroyal()
        self.rwitch()
        self.rbishop()
        self.tableDeckR1.resizeColumnsToContents()
        self.rnecro()
        self.rdragon()
        self.rvamp()
        self.rneme()
        self.tableDeckR2.resizeColumnsToContents()

    # 선후공 승률 막대 그래프 in 덱별 전적
    def fsgraph(self):
        df = myWindow.df6
        df1 = df[df['FirstSecond'].isin(['선공'])]
        df1_1 = df1[df1['WinLose'].isin(['승'])]
        df2 = df[df['FirstSecond'].isin(['후공'])]
        df2_1 = df2[df2['WinLose'].isin(['승'])]
        if len(df1) == 0:
            fwin = 0
        else:
            fwin = round(len(df1_1) * 100 / len(df1), 1)
        if len(df2) == 0:
            swin = 0
        else:
            swin = round(len(df2_1) * 100 / len(df2), 1)
        self.figure.clear()
        ax = plt.subplot(2, 1, 1)
        rects1 = plt.barh(2, fwin, align='center', color='lightskyblue', height=0.5, label='선공')
        rects2 = plt.barh(1, swin, align='center', color='xkcd:pistachio', height=0.5, label='후공')
        plt.xlim([0, 100])
        plt.yticks([])
        if fwin >= 30:
            for i, rect in enumerate(rects1):
                ax.text(0.95 * rect.get_width(), rect.get_y() + rect.get_height() / 2.0, str(fwin) + '%',
                        ha='right', va='center')
        else:
            for i, rect in enumerate(rects1):
                ax.text(rect.get_width() + 2, rect.get_y() + rect.get_height() / 2.0, str(fwin) + '%',
                        ha='left', va='center')
        if swin >= 30:
            for i, rect in enumerate(rects2):
                ax.text(0.95 * rect.get_width(), rect.get_y() + rect.get_height() / 2.0, str(swin) + '%',
                        ha='right', va='center')
        else:
            for i, rect in enumerate(rects2):
                ax.text(rect.get_width() + 2, rect.get_y() + rect.get_height() / 2.0, str(swin) + '%',
                        ha='left', va='center')

        self.canvas19.draw()
        self.figure.clear()

    def relf(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['엘프'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS엘프', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS엘프', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR1.rowCount()
        self.tableDeckR1.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(207, 247, 99))
            self.tableDeckR1.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR1.rowCount()
                self.tableDeckR1.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(176, 239, 12))
                    self.tableDeckR1.setItem(rowcount, i, item)

    def rroyal(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['로얄'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS로얄', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS로얄', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR1.rowCount()
        self.tableDeckR1.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(253, 251, 140))
            self.tableDeckR1.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR1.rowCount()
                self.tableDeckR1.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(197, 191, 3))
                    self.tableDeckR1.setItem(rowcount, i, item)

    def rwitch(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['위치'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS위치', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS위치', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR1.rowCount()
        self.tableDeckR1.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(158, 168, 240))
            self.tableDeckR1.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR1.rowCount()
                self.tableDeckR1.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(92, 109, 231))
                    self.tableDeckR1.setItem(rowcount, i, item)

    def rbishop(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['비숍'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS비숍', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS비숍', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR1.rowCount()
        self.tableDeckR1.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(255, 255, 255))
            self.tableDeckR1.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR1.rowCount()
                self.tableDeckR1.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(190, 190, 190))
                    self.tableDeckR1.setItem(rowcount, i, item)

    def rnecro(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['네크로맨서'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS네크로맨서', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS네크로맨서', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR2.rowCount()
        self.tableDeckR2.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(242, 178, 255))
            self.tableDeckR2.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR2.rowCount()
                self.tableDeckR2.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(226, 89, 255))
                    self.tableDeckR2.setItem(rowcount, i, item)

    def rdragon(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['드래곤'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS드래곤', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS드래곤', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR2.rowCount()
        self.tableDeckR2.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(255, 232, 99))
            self.tableDeckR2.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR2.rowCount()
                self.tableDeckR2.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(249, 211, 0))
                    self.tableDeckR2.setItem(rowcount, i, item)

    def rvamp(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['뱀파이어'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS뱀파이어', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS뱀파이어어', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR2.rowCount()
        self.tableDeckR2.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(255, 125, 177))
            self.tableDeckR2.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR2.rowCount()
                self.tableDeckR2.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(255, 40, 126))
                    self.tableDeckR2.setItem(rowcount, i, item)

    def rneme(self):
        df = myWindow.df6
        df1 = df[df['OppoJob'].isin(['네메시스'])]
        vsc = len(df1)
        if vsc == 0:
            rec = ['VS네메시스', '0', '0', '0', 'N/A', 'N/A', 'N/A']
        else:
            win = len(df1[df1['WinLose'].isin(['승'])])
            lose = len(df1[df1['WinLose'].isin(['패'])])
            winrate = str(round(win * 100 / vsc, 1)) + '%'
            df2 = df1[df1['FirstSecond'].isin(['선공'])]
            df2_1 = df2[df2['WinLose'].isin(['승'])]
            df3 = df1[df1['FirstSecond'].isin(['후공'])]
            df3_1 = df3[df3['WinLose'].isin(['승'])]
            if len(df2) == 0:
                fwin = 'N/A'
            else:
                fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
            if len(df3) == 0:
                swin = 'N/A'
            else:
                swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
            rec = ['VS네메시스', str(vsc), str(win), str(lose), winrate, fwin, swin]
        rowcount = self.tableDeckR2.rowCount()
        self.tableDeckR2.insertRow(rowcount)
        for i, text in enumerate(rec):
            item = QTableWidgetItem()
            item.setText(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            item.setBackground(QtGui.QColor(215, 255, 255))
            self.tableDeckR2.setItem(rowcount, i, item)
        if vsc == 0:
            return
        else:
            df4 = df1.drop_duplicates(['OppoArche'])
            lists = list(set(df4['OppoArche']))
            for arche in lists:
                df1 = df[df['OppoArche'].isin([arche])]
                deck = 'VS' + arche
                vsc = len(df1)
                win = len(df1[df1['WinLose'].isin(['승'])])
                lose = len(df1[df1['WinLose'].isin(['패'])])
                winrate = str(round(win * 100 / vsc, 1)) + '%'
                df2 = df1[df1['FirstSecond'].isin(['선공'])]
                df2_1 = df2[df2['WinLose'].isin(['승'])]
                df3 = df1[df1['FirstSecond'].isin(['후공'])]
                df3_1 = df3[df3['WinLose'].isin(['승'])]
                if len(df2) == 0:
                    fwin = 'N/A'
                else:
                    fwin = str(round(len(df2_1) * 100 / len(df2), 1)) + '%'
                if len(df3) == 0:
                    swin = 'N/A'
                else:
                    swin = str(round(len(df3_1) * 100 / len(df3), 1)) + '%'
                rec = [deck, str(vsc), str(win), str(lose), winrate, fwin, swin]
                rowcount = self.tableDeckR2.rowCount()
                self.tableDeckR2.insertRow(rowcount)
                for i, text in enumerate(rec):
                    item = QTableWidgetItem()
                    item.setText(text)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    item.setBackground(QtGui.QColor(155, 255, 255))
                    self.tableDeckR2.setItem(rowcount, i, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
