from UrlManager import UrlManager
from DataOutput import DataOutput
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
import time

class NodeManager(object):
    
    def start_Manager(self, url_q, result_q):
        """
        functions:
        1. create a distribute manager
        2. register url_q, result_q into web for interface with spide node 
        3. bind port, set authkey
        4. return a manager object
        """
        # register these two Queue into web
        # callable connect Queue object
        BaseManager.register('get_task_queue', callable=lambda:url_q)
        BaseManager.register('get_result_queue', callable=lambda:result_q)
        # bind port 8001
        # set authentic key "baike"
        manager = BaseManager(address=('',8001), authkey='baike')
        return manager
    
    def url_manager_proc(self, url_q, conn_q, root_url):
        """
        functions: 
            1. get new url into conn_q and give to UrlManager 
            2. UrlManager process dereplication
            3. pull url out and send to url_queue to spider node
        """
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while(url_manager.has_new_urls()):
                # get a uncrawled url in UrlManager
                new_url = url_manager.get_new_url()
                # send url to work node
                url_q.put(new_url)
                print 'old_url = ', url_manager.old_url_size()
                # set conditions
                if(url_manager.old_url_size() > 2000):
                    url_q.put('end')
                    print('[!] scheduler send information [END]')
                    # close node and store set()
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)
                    return
                # get url into result_solve_proc
                # and send it into UrlManager
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException, e:
                time.sleep(0.1)
    
    def result_sovle_proc(self, result_q, conn_q, store_q):
        """
        functions:
            1. read data back from result_queue
            2. filter url into conn_q then back to UrlManager 
            3. filter data into store_q then send to store process
        """
        while(True):
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content["new_urls"] == "end":
                        # result_sovle_proc recv information then end process
                        print "result_sovle_proc receive info"
                        print "--------process end---------"
                        store_q.put("end")
                        return
                    conn_q.put(content["new_urls"]) # set()
                    store_q.put(content["data"]) # parser out as dict()
                else:
                    time.sleep(0.1)
            except BaseException, e:
                time.sleep(0.1)
    
    def store_proc(self, store_q):
        """
        functions:
            1. read data from store_q
            2. call Dataoutput to store data
        """
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print 'store process receive info'
                    print '-----process end----------'
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)

if __name__ == '__main__':
    # initialize four queue
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    # create a object
    node = NodeManager()
    manager = node.start_Manager(url_q, result_q)

    # create url manager process
    url_manager_proc = Process(target=node.url_manager_proc, args=(url_q, conn_q, 
         'https://baike.baidu.com/item/%E8%97%8F%E7%8B%90',))
    # data output process 
    result_solve_proc = Process(target=node.result_sovle_proc, args=(result_q,
         conn_q, store_q,))
    # data store process
    store_proc = Process(target=node.store_proc, args=(store_q,))
    # start up processes and contribution manager
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()