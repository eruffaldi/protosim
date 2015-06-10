# Proto Recorder
#
# Emanuele Ruffaldi 2010
import socket,sys,time,Queue,threading,uuid,os
import cStringIO,gzip,struct,inspect,protocols,traceback
from protostore import StoreWrite

   
def buildpath(base,ps,uuid,t):
    return ("/".join([base,uuid,"u"+str(int(ps.userid)),"s"+str(int(ps.sessionid)),"b"+str(int(ps.blockid))]),time.strftime("%Y-%m-%d.%H%M.%S",time.gmtime(t)))
      
def newstore(base,ps,uuid,t,tags,protos):
    # ps is a start proto
    # uuid 
    # t is time
    path,name = buildpath (base,ps,uuid,t)
    if not os.path.exists(path):
        os.makedirs(path)
    return StoreWrite(path,name,t,tags,protos)
    

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)
    
class PacketStat:
    def __init__(self,name):
        self.name = name
        self.basetime = None
        self.count = 0
        self.size = 0
        self.tcount = 0
        self.tsize = 0
        self.lasttime = None
    def add(self,t,n):
        if self.basetime is None:
            self.basetime = t
        self.lasttime = t
        self.size += n
        self.count += 1
        self.tsize += n
        self.tcount += 1
    def resettime(self):
        self.basetime = None
        self.lasttime = None
        self.count = 0
        self.size = 0
    def __str__(self):
        t = self.basetime is not None and (self.lasttime-self.basetime) or 0
        return "%25s %8d paks %8.3f paks/sec %8d KB %8.3f KB/sec" % (self.name,self.tcount,t != 0 and self.count/t or 0,self.tsize/1024.0,t != 0 and self.size/t/1024 or 0)
class UDP:
    def __init__(self,sock,index,targetqueue):
        self.sock = sock
        self.index = index
        self.t = threading.Thread(target=self.worker)
        self.t.daemon = True
        self.targetqueue = targetqueue
        self.t.start()
    def protoerror(self,msg,id):
        print id,msg
    def worker(self):
        sock = self.sock
        bufsize = 32768
        try:
            while True:            
                d = sock.recv(bufsize)
                n = len(d)
                if n == 0:
                    break
                t = time.time()    
                while n > 0:
                    id = struct.unpack("b",d[0])[0]
                    proto = protos.get(id,None)
                    if proto is not None:
                        bytesize = proto.bytesize
                        if n < bytesize:
                            self.protoerror("Proto Size Mismatch id:%d size:%d received:%d" % (id,bytesize,n),id)
                            #content = d[1:n] + "\x00"*(bytesize-n)
                            #n = bytesize
                            break
                        content = d[1:bytesize+1]
                        try:
                            self.targetqueue.put((self.index,t,id,content,proto))
                        except:
                            traceback.print_exc()
                        n = n - bytesize
                        d = d[bytesize:]
                        # 25 25 41
                    else:
                        self.protoerror("Unknown Proto %d" % id,id)                   
        except:
            traceback.print_exc()
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-a", "--address", dest="address",default="",
                  help="listening IP address")
parser.add_option("-o", "--outputfolder", dest="output",default="rec",
                  help="target folder")
parser.add_option("-t", "--timeout", dest="timeout",default=2000,
                  help="timeout of storage")
parser.add_option("-u", "--allow-not-started", dest="allownotstarted",default=False,action='store_true',
                  help="Allow Not Started")
parser.add_option("-n", "--no-store", dest="nostore",default=False,action='store_true',
                  help="target folder")
parser.add_option("", "--row", dest="rowmode",default=False,action='store_true',
                  help="store as rowing mode 40000:default 40001:raw 40002:vibro 40003:audio")
(options, args) = parser.parse_args()
if options.rowmode:
    args.append("40000:default")
    args.append("40001:raw")
    args.append("40002:vibro")
    args.append("40003:audio")
if len(args) == 0:
    parser.error("incorrect number of arguments. Expecting port:tag association")
    sys.exit(0)    

protos = dict([(x.id,x) for x in [getattr(protocols,x) for x in dir(protocols)] if inspect.isclass(x)])
proto_startid = protocols.proto_start.id
ps = protocols.proto_start()
protostat = dict([(x.id,PacketStat("%s(%2d)" % (x.__name__,x.id))) for x in protos.values()])
globalstat = PacketStat("global")

targetstat = {}  # stats for  packets of idx
tags = {} # tags
targets = []
waitqueue = Queue.Queue()

for i in args:
    port, tag = (i+":default").split(":")[0:2]
    if not tag in tags:
        idx = len(tags)+1
        tags[tag] = idx
        targetstat[idx] = PacketStat("tag_%s(%2d)" % (tag,idx))
    else:
        idx = tags[tag]
    address = (options.address,int(port))
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
    ss.bind(address)
    targets.append(UDP(ss,idx,waitqueue))                
    
try:
    laststat = time.time()
    statstep = 5    
    # dummy ps    
    curstore = None
    startednotified = False
    lastpackettime = None
    while True:
        try:
            r = waitqueue.get(True,statstep)        
        except:
            r = None
        if r is not None:
            (idx,t,id,content,proto) = r
            waitqueue.task_done()
            lastpackettime = t
            protostat[id].add(t,len(content))
            targetstat[idx].add(t,len(content))
            globalstat.add(t,len(content))        
            if id == proto_startid:
                # start protocol!
                if ps.decode(content):
                    print  ps.taskuuid
                    uuid = struct.pack("36b",*[int(x) for x in ps.taskuuid])
                    curstore = newstore(options.output,ps,uuid,t,tags,protos.values())
                    print "new storage",uuid,"at",time.time()," to ",curstore.fullpath
                    curstore.append(idx,t,id,content)
                else:
                    print "decode of start failed"
            else:
                # store content
                #print "store",(idx,t,id,len(content))
                # options.nostore            
                if curstore is None:
                    if options.allownotstarted:
                        uuid = str(uuid.uuid1())
                        curstore = newstore(options.output,ps,uuid,t,tags,protos.values())
                        print "start not received. Storing to ",curstore.fullpath
                        curstore.append(idx,t,id,content)
                    elif not startednotified:
                        print "not started yet"                    
                        startednotified = True
                else:
                    curstore.append(idx,t,id,content)
        else:
            t = time.time()
        if lastpackettime is not None and (t-lastpackettime) > options.timeout:
            if custore is not None:
                print "Timeout ",curstore.path," closing"            
                curstore = None
        if t-laststat > statstep:
            print "Stats of ",curstore is not None and curstore.fullpath or "<none>"
            laststat = t
            for x in protostat.values():
                print x
                x.resettime()
            for x in targetstat.values():
                print x
                x.resettime()
            print globalstat
            globalstat.resettime()
except (KeyboardInterrupt,SystemExit):
    print "Closing"
    # TODO storage close
