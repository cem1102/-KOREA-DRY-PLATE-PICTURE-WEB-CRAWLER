#-*- coding: utf-8 -*-
import time, glob, os
from selenium import webdriver

from selenium.common.exceptions import TimeoutException

class chromeDriverProvider:
    def __init__(self):
        self.options = None
        self.driver = None
        self.save_path = u"[저장 디렉토리]"


    def _create_options(self):
        print "  ! create option set"
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--lang=ko-kr')
        prefs = { "download.default_directory": self.save_path }
        options.add_experimental_option('prefs', prefs)
        return options

    def check_wait(self, target, time_v):
        if not target:
            time.sleep(time_v)
        else:
            while True:
                if self.driver.page_source.find(target) > 0: break
                time.sleep(time_v)

    def _create_driver(self):
        if not self.options:
            self.options = self._create_options()
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=self.options)
        self.driver.implicitly_wait(5)


    def run(self):
        self._create_driver()
        base_url = """http://www.emuseum.go.kr/detail?cateClass=&cateListFlag=&keyword=&pageNum=%d&rows=&sort=title&highQualityYn=&isImgExistOp=&mckoglsvOp=&isIntrstMuseumOp=&filedOp=&detailFlag=&dq=&ps01Lv1=&ps01Lv2=&ps01Lv3=&mcSeqNo=&author=&ps06Lv1=&ps06Lv2=&ps08Lv1=&ps08Lv2=&ps09Lv1=&ps09Lv2=&ps09Lv3=&ps09Lv4=&gl05Lv1=&gl05Lv2=&ps12Lv1=&ps15Lv1=&culturalHerNo=&publicType=&detailedDes=&thema=&storySeq=1101&categoryLv=&categoryCode=&mobileFacetIng=&location=&facet1Lv1=&facet1Lv2=&facet2Lv1=&facet3Lv1=&facet3Lv2=&facet4Lv1=&facet4Lv2=&facet5Lv1=&facet5Lv2=&facet5Lv3=&facet5Lv4=&facet6Lv1=&facet6Lv2=&facet7Lv1Selected=&facet7Lv1=&facet8Lv1=&keywordHistory=&showSearchOption=&intrstMuseumCode=&returnUrl=%%2FstorySearch"""
        for i in range(38170):
            success = False
            while True:
                try:
                    self.driver.get(base_url % (i + 1))
                    self.check_wait("ote_con", 1)
                    nuri_type= "누리_" + self.driver.find_element_by_xpath("//dl[@class='ote_con']/dt").get_attribute("innerHTML").split(":")[0].strip().replace(" ","")
                    title = self.driver.find_element_by_xpath("//strong[@class='dinfo_title']").get_attribute("innerHTML").strip()
        
                    time.sleep(3)
        
                    self.driver.find_element_by_xpath("//a[@class='btn_download modal_btn']/span").click()
        
                    self.check_wait("usage_purpose_type", 1)
        
                    self.driver.find_element_by_xpath("//select[@id='usage_purpose_type']/option[@value='기타']").click()
        
                    time.sleep(3)
        
                    self.driver.find_element_by_xpath("//textarea[@id='usage_purpose_desc']").send_keys(u"usage purpose description")
        
                    time.sleep(3)
        
                    for item in self.driver.find_elements_by_xpath("//a[@class='btn download']/span"):
                        if item.get_attribute("innerHTML") == "이미지 다운로드":
                            item.click()
                            break
        
                    time.sleep(10)
                    download_complete = False
                    while True:
                        if len(glob.glob(self.save_path + u"\\*.crdownload")) == 0:
                            download_complete = True
                        if download_complete: break
                    for _file in glob.glob(self.save_path + u"\\[!COMPLETE]*"):
                    	if _file.split("\\")[-1].startswith("COMPLETE"): continue
                    	os.rename(_file, self.save_path + "\\COMPLETE_" + str(i+1).zfill(5) + "_" + nuri_type + "_"  + title + ".jpg")
                    success = True
                except TimeoutException as ex:
                    print "- download failed with timeout, restart chrome and session"
                    success = False
                    self.close()
                    self._create_driver()
                if success: break
                  
        self.close()
   

       

    def close(self):
        try: self.driver.close()
        except: pass
        try: self.driver.quit()
        except: pass

if __name__ == '__main__':
	cdp = chromeDriverProvider()
	cdp.run()
