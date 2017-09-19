# coding: utf-8
import time


class InjectMessage:
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
         """

    def show_message(self, browser, message, message_timing=4, pause=2):
        browser.execute_script("spop({ template: ' " + message + " ', autoclose: " + str(message_timing * 1000) + " });")
        time.sleep(pause)

    def inject_dependencies(self, browser):
        browser.execute_script(self.js_injector +
                       """
                        include_css('https://cdn.rawgit.com/silvio-r/spop/gh-pages/dist/spop.min.css', function(){});
                        include_js('//cdn.rawgit.com/silvio-r/spop/gh-pages/dist/spop.min.js', function() {});
                       """)
        time.sleep(3)

