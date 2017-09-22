# coding: utf-8
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class JsTools:
    message_status = False
    dim_status = False
    logger = None
    page_wait = None
    js_injector = """
            var include_js = function(url, callback){
                var script = document.createElement('script');
                script.type = 'text/javascript';
                script.src = url;
                if (callback) {
                    script.onreadystatechange = callback;
                    script.onload = script.onreadystatechange;
                }
                document.getElementsByTagName('head')[0].appendChild(script);
                console.log("Scrip loaded");
            }

            var include_css = function(url, callback){
                var css = document.createElement('link');
                css.type = 'text/css';
                css.rel = 'stylesheet';
                css.href = url;
                document.getElementsByTagName('head')[0].appendChild(css);
                console.log("CSS loaded");
            }

            var create_target = function(){
                document.body.innerHTML += '<span id="kissenium"></span>';
            }
         """

    def __init__(self, message_status, dim_status, logger, page_wait):
        self.message_status = message_status
        self.dim_status = dim_status
        self.logger = logger
        self.page_wait = page_wait

    def message(self, browser, message, message_timing=4, pause=2):
        self.logger.info(
            "[InjectMessage] message: Messaging status : %s | Message to send : %s " % (self.message_status, message))
        if self.message_status == "True":
            self.inject_dependencies(browser)
            browser.execute_script("spop({ template: '%s', autoclose: %s });" % (message, str(message_timing * 1000)))
            time.sleep(pause)

    def dim_by_id(self, browser, element_id, timing=2):
        self.logger.info(
            "[InjectMessage] dim: Messaging status : %s" % self.dim_status)
        if self.dim_status == "True":
            self.inject_dependencies(browser)
            browser.execute_script("$('#%s').dimBackground();" % element_id)
            time.sleep(timing)
            browser.execute_script("$('#%s').undim();" % element_id)

    def inject_dependencies(self, browser):
        if self.message_status == "True" or self.dim_status == "True":
            try:
                browser.find_element(By.__dict__.get('ID'), "kissenium")
            except NoSuchElementException:
                self.logger.info("[InjectMessage] inject_dependencies: no dependencies injected, injecting them...")
                browser.execute_script(self.js_injector +
                                       """
                                        include_css('https://www.adiuvo.fr/kissenium.min.css', function(){});
                                        include_js('https://www.adiuvo.fr/kissenium.min.js', 
                                                    function(){ create_target(); });
                                       """)
                WebDriverWait(browser, int(self.page_wait)).until(
                    ec.presence_of_element_located((By.ID, "kissenium"))
                )
                self.logger.info("[InjectMessage] inject_dependencies: Dependencies injected!")


