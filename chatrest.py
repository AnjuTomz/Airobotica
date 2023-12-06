import os, sys, web, time

import logging
import traceback

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='RealEstateBot_App.log',level=logging.INFO,format=FORMAT)
# logging.basicConfig(stream=sys.stdout,level=logging.INFO,format=FORMAT)
logger = logging.getLogger(__name__)

if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chat_engine
'''
http://localhost:8081/amd?companyName=RealEstate&userID=123&requestType=plain_text&query=hi
'''

urls = (
    '/amd','Bot',
)

query = ''


class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class Bot:
    def GET(self):
         #try:
            logger.info("########################################")
            web.header('Content-Type', 'application/json')
            user_data = web.input(companyName="no info from input",query="no query",requestType="no info from input",userID="no user id provided",flow="no flow_type given")
            query = user_data.query
            #query = unicode(query).encode("utf-8")
            companyname = user_data.companyName
            user_id = user_data.userID
            request_type = user_data.requestType
            flow_type = user_data.flow
            logger.info("QUERY => %s", query)
            logger.info("Company name => %s", companyname)
            logger.info("User Id => %s", user_id)
            logger.info("Request Type => %s", request_type)
            start_time = time.time()
            resp = chat_engine.wrapper(companyname, query, request_type, user_id,flow_type)
            logger.info(resp)
            final_time = time.time()
            time_taken = final_time - start_time
            logger.info("Time taken from python for query ## %s ## is :: %s", query, time_taken)
            return resp
         #except Exception as e:
            #logger.error("Error: %s", traceback.format_exc())
            #return chat_engine.answer_not_found()

if __name__ == "__main__":
    app = MyApplication(urls, globals())
    app.run(port=8081)
   


