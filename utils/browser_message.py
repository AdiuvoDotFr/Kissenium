# coding: utf-8
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class InjectMessage:
    is_actived = False
    logger = None
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

    def __init__(self, is_activated, logger):
        self.is_actived = is_activated
        self.logger = logger

    def show_message(self, browser, message, message_timing=4, pause=2):
        self.logger.info("[InjectMessage] show_message: Messaging status : %s | Message to send : %s " % (self.is_actived, message))
        if self.is_actived == "True":
            self.inject_dependencies(browser)
            browser.execute_script("spop({ template: '%s', autoclose: %s });" % (message, str(message_timing * 1000)))
            time.sleep(pause)

    def inject_dependencies(self, browser):
        if self.is_actived == "True":
            try:
                browser.find_element(By.__dict__.get('ID'), "kissenium")
            except NoSuchElementException:
                self.logger.info("[InjectMessage] inject_dependencies: no dependencies injected, injecting them...")
                browser.execute_script(self.js_injector +
                                       """
                                        include_css('https://cdn.rawgit.com/silvio-r/spop/gh-pages/dist/spop.min.css', function(){});
                                        include_js('//cdn.rawgit.com/silvio-r/spop/gh-pages/dist/spop.min.js', function(){});
                                        create_target();
                                       """)
                time.sleep(3)
                self.logger.info("[InjectMessage] inject_dependencies: Dependencies injected!")


