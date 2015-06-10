import struct,os

PROTOCOL= 0
TAG = 1
DATAPACKET = 2
sig1 = "#PROTO1.0\r\n"

class Packet:
    def __init__(self,store,tagidx,time,id,data):
        self.store = store
        self.tagidx = tagidx
        self.time = time
        self.id = id
        self.data = data
class Protocol:
    def __init__(self,name,idx,fields):
        self.name = name
        self.idx = idx
        self.fields = fields
    def __repr__(self):
        return "%s as %d with %s" % (self.name,self.idx,self.fields)
def decodestr(x):
    k = struct.unpack("<i",x[0:4])[0]
    return x[4:4+k],x[4+k:]
def encodestr(x):
    return struct.pack("<i",len(x))+x
def encodepak(x):
    return struct.pack("<i",len(x))+x
class StoreRead:
    def __init__(self,path):
        self.f = open(path,"rb")
        self.protos = {}
        self.tags = {}
        first = self.f.readline()
        if first != sig1:
            raise "Unknown format"
    def iter(self):
        while True:
            t = self.f.read(4)
            if t == "":
                break
            n = struct.unpack("<i",t)[0]
            p = self.f.read(n)
            if len(p) < n:
                break
            id = struct.unpack("b",p[0])[0]
            if id == PROTOCOL:
                name,p = decodestr(p[1:])
                idx,count = struct.unpack("<hh",p[0:4])
                p = p[4:]
                pp = Protocol(name,idx,[])
                for i in range(0,count):
                    name,p = decodestr(p)
                    size = struct.unpack("<i",p[0:4])
                    type,p = decodestr(p[4:])
                    pp.fields.append((name,size,type))
                self.protos[idx] = pp
            elif id == TAG:
                idx = struct.unpack("<h",p[1:3])[0]
                name,p = decodestr(p[3:])
                self.tags[idx] = name
            elif id == DATAPACKET:
                idx,time,id,size = struct.unpack("<hdhh",p[1:15])
                data = p[15:15+size] 
                yield Packet(self,idx,time,id,data)            
    
class StoreWrite:
    def __init__(self,path,name,basetime,tags,protos):
        self.path = path
        self.name = name
        self.fullpath = "/".join([path,name+".dat"]).replace("/","\\")
        self.f = open(self.fullpath,"wb")
        self.savehead(tags,protos)
        self.savemeta(tags,protos)
        self.basetime = basetime
    def savemeta(self,tags,protos):
        m = open("/".join([self.path,self.name+".meta"]),"wb")
        m.write("""PROTO1.0 format:
        Starts with line
        #PROTO1.0\r\n
        Sequence of Records as Little Endian
        <record length int32 LE><data[length]>

        Strings are stored using
        size(int32)
        value[size]

        First byte is type of Record
        PROTOCOL=0
        type (byte) = 0    
        name (str)
        id (int16)
        count(int16)
            name (str)
            size (int32)
            type
        TAGS=1
        type (byte) = 1
        index (int16)
        name (str)    
        DATAPACKET=2 bhdhh + data
        type (byte) = 2
        tagindex (int16) = group of tag
        time (double) since EPOCH in seconds
        id (int16) = protocol type
        size (int16) 
        content[size] binary data based on protocoltype
        """)
        m.write("PROTOS")
        for p in protos:
            m.write("\tProto %s %d " % (p.name,p.id) + str(p.meta))
        m.write("TAGS")
        for k,v in tags.iteritems():
            m.write("\tTag %s %d" % (k,v))
    def savehead(self,tags,protos):
        self.f.write(sig1)
        for p in protos:
            w = "".join([encodestr(x[0])+struct.pack("<i",x[1])+encodestr(x[2]) for x in p.meta])
            pak = struct.pack("<b",PROTOCOL)+encodestr(p.name)+struct.pack("<hh",p.id,len(p.meta))+w
            self.f.write(encodepak(pak))
        for k,v in tags.iteritems():
            pak = struct.pack("<bh",TAG,v)+encodestr(k)
            self.f.write(encodepak(pak))
    def append(self,idx,t,id,content):
        pak = struct.pack("<bhdhh",DATAPACKET,idx,t,id,len(content))+content
        self.f.write(encodepak(pak))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sr = StoreRead(sys.argv[1])        
        first = True
        for x in sr.iter():
            if first:
                print sr.protos
                print sr.tags
                first = False
            print x.time,x.tagidx,x.id,len(x.data)