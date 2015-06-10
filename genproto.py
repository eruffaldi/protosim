#
# GenPROTO by Emanuele Ruffaldi 2009
# v1 2009/12/05
#
# TODO:
# - nicer Simulink layout
# - hash as annotation or as output
# - encoder id > 256 in particular using extended encoding (lsb+msb)
# - Alternative: XVR encoding of an array
# - Support for new types
import hashlib

def fixref(x):
    if type(x) is str:
        return (x,1)
    else:
        return x
        
class Generator:    
    def __init__(self):
        self.lines = []
        self.subsys = ""
    def addText(self,text):
        self.lines = self.lines + text.split("\n")
    def save(self,io):
        for x in self.lines:
            io.write("%s\n" % x)
class GeneratorXVR(Generator):    
    def __init__(self):
        Generator.__init__(self)
            
class GeneratorSim(Generator):    
    def __init__(self):
        Generator.__init__(self)
    def closeSubsystem(self):
        self.subsys = ""
    def setSubsystem(self,name):
        self.subsys = name
    def addSubsystem(self,name):
        self.lines.append("h = add_block('built-in/SubSystem',[prefix,'/', \'%s\']);" % (name))
        self.setSubsystem(name)
    def delSubsystem(self,name):
        self.lines.append("try")
        self.lines.append("h = delete_block([prefix,'/', \'%s\']);" % (name))
        self.lines.append("end")
    def addInport(self,name,size=-1):
        self.lines.append("d = add_blockg(d,'built-in/Inport',[prefix,'/',\'%s\','/',\'%s\'],'PortDimensions','%d');" % (self.subsys,name,size))
        return name
    def addConst(self,name,value):
        self.lines.append("d = add_blockg(d,'built-in/Constant',[prefix,'/',\'%s\','/',\'%s\'],'Value','%s');" % (self.subsys,name,value))
        return name
    def setPos(self,x,y,w,h):
        #self.addText("set(h,'Position',[%d,%d,%d,%d]);" % (x,y,w,h))
        pass
    def addPack(self,name):
        self.lines.append("d = add_blockg(d,'netlib/Pack',[prefix,'/',\'%s\','/',\'%s\']);" % (self.subsys,name))
        #self.lines.append("h = add_block('xpclib/UDP/Pack',[prefix,'/',\'%s\','/',\'%s\']);" % (self.subsys,name))
        return name
    def addConvert(self,name,type="uint8"):
        self.lines.append("d = add_blockg(d,'built-in/DataTypeConversion',[prefix,'/',\'%s\','/',\'%s\'],'OutDataTypeStr','%s');" % (self.subsys,name,type))
        return name
    def addOutport(self,name):
        self.lines.append("d = add_blockg(d,'built-in/Outport',[prefix,'/',\'%s\','/',\'%s\']);" % (self.subsys,name))    
        return name
    def addMux(self,ports,name="demuxy",mode="bar"):
        self.lines.append("d = add_blockg(d,'built-in/Mux',[prefix,'/',\'%s\','/%s'],'Inputs','%d','DisplayOption',\'%s\');" % (self.subsys,name,ports,mode))    
        return name
    def addDemux(self,ports,name="demuxy",mode="bar"):
        self.lines.append("d = add_blockg(d,'built-in/Demux',[prefix,'/',\'%s\','/%s'],'Outputs','%d','DisplayOption',\'%s\');" % (self.subsys,name,ports,mode))    
        return name
    def addLine(self,inb,outb):
        inb = fixref(inb)
        outb = fixref(outb)
        self.lines.append("h = add_line([prefix,'/',\'%s\'],'%s/%d','%s/%d');" % (self.subsys,inb[0],inb[1],outb[0],outb[1]))
typesizes = dict(double=8,single=4,int32=4,int16=2,uint8=1,char=1)

class Protocol:
    protocols = []
    def __init__(self,name,id,namesizes):
        """ Create as (name,size1),(name,size2) ... """
        self.namesizes = []
        for x in namesizes:
            if type(x) is str:
                self.namesizes.append((x,1,"double",8))
            elif len(x) == 2:
                self.namesizes.append((x[0],x[1],"double",8))
            else:
                self.namesizes.append((x[0],x[1],x[2],typesizes[x[2]]))
        self.nbytesize = sum([x[3]*x[1] for x in self.namesizes])+1
        self.id = id
        self.name = name
        Protocol.protocols.append(self)
    def bytesize(self):
        return self.nbytesize
    def size(self):
        return sum([x[1] for x in self.namesizes])
    def hash(self):
        m = hashlib.md5()
        m.update(",".join(["%s/%d/%s" % x[0:3] for x in self.namesizes]))
        return m.hexdigest()
    def gensim(self):
        outname = "proto_"+self.name
        id = self.id
        inputs = self.namesizes
        g = GeneratorSim()
        g.addText("function %s(prefix)" % outname)    
        g.addText("""if nargin == 0
 try
    open_system('protocols');
    prefix = 'protocols';
 catch me
    new_system('protocols')
    prefix = 'protocols';
 end
 end""")
        #g.addText("load_system('xpclib')")
        g.addText("d = setup_default_draw_parameters();")
        g.delSubsystem(self.name)
        g.addSubsystem(self.name)
        for i in range(0,len(inputs)):
            g.addInport(inputs[i][0],inputs[i][1])
        # modify the type of ports
        g.addMux(len(inputs),"muxpre","bar")
        g.addMux(2,"muxout","bar")
        g.addOutport("output")
        for i in range(0,len(inputs)):
            g.addLine(inputs[i][0],("muxpre",i+1))
        g.addPack("pack")
        b_cvt = g.addConvert("cvt","uint8")
        g.addConst("idc",id)
        g.addLine("idc",b_cvt)
        g.addLine(b_cvt,"muxout")
        g.addLine("muxpre","pack")
        g.addLine("pack",("muxout",2))
        g.addLine("muxout","output")
        g.addText("""
		function draw_params = add_blockg(draw_params,t,block,varargin)
	h = add_block(t,block,varargin{:});
	set_param(block,'position',[draw_params.h_pos,draw_params.v_pos,draw_params.h_pos+draw_params.block_width,draw_params.v_pos+draw_params.block_height]);
	draw_params.h_pos = draw_params.h_pos + draw_params.block_width + draw_params.h_space;
	draw_params.v_pos = draw_params.v_pos + draw_params.block_height + draw_params.v_space;
function draw_params = setup_default_draw_parameters()
draw_params.block_width  = 40;
draw_params.block_height = 40;

draw_params.h_space = 20;
draw_params.v_space = 40;

draw_params.max_height = 32700;
draw_params.last_height = 0;

draw_params.h_pos = 20;
draw_params.v_pos = 20;
draw_params.v_reset_pos = draw_params.v_pos;""")
        g.save(open("%s.m" % outname,"wb"))
    def genxvr(self):
        outname = "proto_"+self.name
        id = self.id
        inputs = [(x[0].replace(".","_"),x[1]) for x in self.namesizes]
        g = GeneratorXVR()
        g.addText("#include \"cvec.h.s3d\"")
        g.addText("class %s\n{" % outname)
        for x in inputs:
            g.addText("\tvar %s;" % x[0]);
        g.addText("\tdecode(data);");
        g.addText("\tencode(out,outoff);");
        g.addText("};")
        g.addText("function %s::%s()\n{\n" % (outname,outname));
        for x in inputs:
            g.addText("\t%s = %s;" % (x[0],x[1] == 1 and "0.0" or "vector(%d)" % x[1]))
        g.addText("}")
        g.addText("function %s::decode(data)\n{\n" % outname);
        g.addText("\tif(len(data) < %d) return false;" % self.size());
        i = 0
        for x in inputs:
            if x[1] == 1:
                g.addText("\t%s = data[%d];" % (x[0],i));
            elif x[1] == 2:
                g.addText("\t%s[0] = data[%d];" % (x[0],i));
                g.addText("\t%s[1] = data[%d];" % (x[0],i+1));
            elif x[1] == 3:
                g.addText("\t%s[0] = data[%d];" % (x[0],i));
                g.addText("\t%s[1] = data[%d];" % (x[0],i+1));
                g.addText("\t%s[2] = data[%d];" % (x[0],i+2));
            elif x[1] == 4:
                g.addText("\t%s[0] = data[%d];" % (x[0],i));
                g.addText("\t%s[1] = data[%d];" % (x[0],i+1));
                g.addText("\t%s[2] = data[%d];" % (x[0],i+2));
                g.addText("\t%s[3] = data[%d];" % (x[0],i+3));
            else:
                g.addText("\tcopyvec(&%s,&data,%d,%d);" % (x[0],i,x[1]));
            i = i + x[1]
        g.addText("\treturn true;")
        g.addText("}")
        g.addText("function %s::encode(out,ooff)\n{\n" % outname);
        i = 0
        for x in inputs:
            if x[1] == 1:
                g.addText("\tout[%d+ooff] = %s;" % (i,x[0]));
            elif x[1] == 2:
                g.addText("\tout[%d+ooff] = %s[0];" % (i,x[0]));
                g.addText("\tout[%d+ooff] = %s[1];" % (i+1,x[0]));
            elif x[1] == 3:
                g.addText("\tout[%d+ooff] = %s[0];" % (i,x[0]));
                g.addText("\tout[%d+ooff] = %s[1];" % (i+1,x[0]));
                g.addText("\tout[%d+ooff] = %s[2];" % (i+2,x[0]));
            elif x[1] == 4:
                g.addText("\tout[%d+ooff] = %s[0];" % (i,x[0]));
                g.addText("\tout[%d+ooff] = %s[1];" % (i+1,x[0]));
                g.addText("\tout[%d+ooff] = %s[2];" % (i+2,x[0]));
                g.addText("\tout[%d+ooff] = %s[3];" % (i+3,x[0]));
            else:
                g.addText("\tcopyvec(&out,&%s,%d,%d,%d+ooff);" % (x[0],0,x[1],i));
            i = i + x[1]
        g.addText("\treturn true;")
        g.addText("}")
        g.addText("#define %s_id %d" % (outname,self.id));
        g.addText("var %s_size = %d;" % (outname,self.size()));
        g.addText("var %s_obj = %s();" % (outname,outname));
        g.addText("var %s_hash = \"%s\";" % (outname,self.hash()));
        g.save(open("%s.s3d" % outname,"wb"))
    @classmethod
    def genpypre(self,out):
        g = GeneratorXVR()
        g.addText("import struct")
        g.addText("import array")
        g.save(out)
    def meta(self):
        return "(%s,)" % ",".join(["(%s)" % ",".join(["\""+str(x[0])+"\"",str(x[1]),"\""+str(x[2])+"\""]) for x in self.namesizes])
    def genpy(self,out,doheader=True):
        id = self.id
        inputs = [(x[0].replace(".","_"),x[1],x[2],x[3]) for x in self.namesizes]
        g = GeneratorXVR()
        if doheader:
            g.addText("import struct")
            g.addText("import array")
        g.addText("class proto_%s:" % self.name)
        g.addText("\tid = %d" % self.id)
        g.addText("\tname = \"%s\"" % self.name)
        g.addText("\tsize = %d" % self.size())
        g.addText("\tbytesize = %d" % self.bytesize())
        g.addText("\thash = \"%s\"" % self.hash())
        g.addText("\tmeta = %s" % self.meta())
        g.addText("\tdef __init__(self):");
        for x in inputs:
            g.addText("\t\tself.%s = %s;" % (x[0],x[1] == 1 and "0.0" or "array.array('d',[0 for i in range(0,%d)])" % x[1]))
        g.addText("\tdef decode(self,data):");
        g.addText("\t\tif len(data) < %d:\n\t\t\treturn False" % (self.bytesize()-1));
        i = 0
        for x in inputs:
            L = x[3]
            n = x[1]
            if n == 1:
                g.addText("\t\tself.%s = struct.unpack('d',data[%d:%d])[0]" % (x[0],i,i+L));
            else:
                g.addText("\t\tself.%s = struct.unpack('%dd',data[%d:%d])" % (x[0],n,i,i+n*L));
            i = i + n*L
        g.addText("\t\treturn True")
        g.addText("\tdef encode(self,io):");
        i = 0
        for x in inputs:
            if x[1] == 1:
                g.addText("\t\tio.write(struct.pack('d',self.%s))" % x[0])
            else:
                g.addText("\t\tio.write(struct.pack('%dd',*self.%s))" % (x[1],x[0]));
            i = i + x[1]
        g.addText("\t\treturn True")
        g.save(out)
        
if __name__ == "__main__":
    import sys
    ctx = dict(__builtin__={},Protocol=Protocol,single="single",double="double",uint8="uint8",int32="int32",char="char")
    for x in sys.argv[1:]:
        execfile(x,ctx,dict())
    print "% MATLAB"
    out = open("protocols.py","wb")
    Protocol.genpypre(out)
    for p in Protocol.protocols:
        print "%",p.name,p.id,p.size(),p.bytesize()
        p.gensim()
        p.genxvr()
        p.genpy(out,False)
    print """try
open_system('protocols');
catch me
new_system('protocols');
end"""
    for p in Protocol.protocols:
        print "proto_%s('protocols');" % p.name
    print "// XVR Include"
    out = open("protocols.h.s3d","wb")
    out.write("""#ifndef PROTOCOLS_H_S3D
#define PROTOCOLS_H_S3D
""")
    for p in Protocol.protocols:
        out.write("#include \"proto_%s.s3d\"\n" % p.name)
    out.write("#endif")
    out.close()
    print "// XVR Switch"
    out = open("protoswitch.h.s3d","wb")    
    for p in Protocol.protocols:
        out.write("case proto_%s_id: size = proto_%s_size; tgt = proto_%s_obj; break;\n" % (p.name,p.name,p.name))
# get_param(gcb,'OutDataTypeStr')
# get_param(gcb,'Position')