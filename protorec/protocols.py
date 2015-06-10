import struct
import array
class proto_env:
	id = 0
	name = "env"
	size = 4
	bytesize = 33
	hash = "a7c9bdbae9b7c692af5d65a935fa8c78"
	meta = (("time",1,"double"),("camera",3,"double"),)
	def __init__(self):
		self.time = 0.0;
		self.camera = array.array('d',[0 for i in range(0,3)]);
	def decode(self,data):
		if len(data) < 32:
			return False
		self.time = struct.unpack('d',data[0:8])[0]
		self.camera = struct.unpack('3d',data[8:32])
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.time))
		io.write(struct.pack('3d',*self.camera))
		return True
class proto_boat:
	id = 1
	name = "boat"
	size = 5
	bytesize = 41
	hash = "87aef19be1d945eb6ea21e42b88bdac2"
	meta = (("boatid",1,"double"),("position",3,"double"),("psi",1,"double"),)
	def __init__(self):
		self.boatid = 0.0;
		self.position = array.array('d',[0 for i in range(0,3)]);
		self.psi = 0.0;
	def decode(self,data):
		if len(data) < 40:
			return False
		self.boatid = struct.unpack('d',data[0:8])[0]
		self.position = struct.unpack('3d',data[8:32])
		self.psi = struct.unpack('d',data[32:40])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.boatid))
		io.write(struct.pack('3d',*self.position))
		io.write(struct.pack('d',self.psi))
		return True
class proto_avatar:
	id = 2
	name = "avatar"
	size = 6
	bytesize = 49
	hash = "2fcb99f1cb7c3d7f24fd4fe5f4e4089b"
	meta = (("avatarid",1,"double"),("alphas",2,"double"),("phis",2,"double"),("seat",1,"double"),)
	def __init__(self):
		self.avatarid = 0.0;
		self.alphas = array.array('d',[0 for i in range(0,2)]);
		self.phis = array.array('d',[0 for i in range(0,2)]);
		self.seat = 0.0;
	def decode(self,data):
		if len(data) < 48:
			return False
		self.avatarid = struct.unpack('d',data[0:8])[0]
		self.alphas = struct.unpack('2d',data[8:24])
		self.phis = struct.unpack('2d',data[24:40])
		self.seat = struct.unpack('d',data[40:48])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.avatarid))
		io.write(struct.pack('2d',*self.alphas))
		io.write(struct.pack('2d',*self.phis))
		io.write(struct.pack('d',self.seat))
		return True
class proto_visibility:
	id = 3
	name = "visibility"
	size = 2
	bytesize = 17
	hash = "347aab2d90fdbcae3513fc823e5dbe28"
	meta = (("entityid",1,"double"),("show",1,"double"),)
	def __init__(self):
		self.entityid = 0.0;
		self.show = 0.0;
	def decode(self,data):
		if len(data) < 16:
			return False
		self.entityid = struct.unpack('d',data[0:8])[0]
		self.show = struct.unpack('d',data[8:16])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.entityid))
		io.write(struct.pack('d',self.show))
		return True
class proto_user_perf:
	id = 4
	name = "user_perf"
	size = 12
	bytesize = 97
	hash = "5f99d875dcad77874748a4feab4a0b94"
	meta = (("avatarid",1,"double"),("tpass",1,"double"),("mpass",1,"double"),("trip",1,"double"),("mrip",1,"double"),("strokes",1,"double"),("tin",1,"double"),("tout",1,"double"),("vmean",1,"double"),("work",1,"double"),("efficiency",1,"double"),("powerout",1,"double"),)
	def __init__(self):
		self.avatarid = 0.0;
		self.tpass = 0.0;
		self.mpass = 0.0;
		self.trip = 0.0;
		self.mrip = 0.0;
		self.strokes = 0.0;
		self.tin = 0.0;
		self.tout = 0.0;
		self.vmean = 0.0;
		self.work = 0.0;
		self.efficiency = 0.0;
		self.powerout = 0.0;
	def decode(self,data):
		if len(data) < 96:
			return False
		self.avatarid = struct.unpack('d',data[0:8])[0]
		self.tpass = struct.unpack('d',data[8:16])[0]
		self.mpass = struct.unpack('d',data[16:24])[0]
		self.trip = struct.unpack('d',data[24:32])[0]
		self.mrip = struct.unpack('d',data[32:40])[0]
		self.strokes = struct.unpack('d',data[40:48])[0]
		self.tin = struct.unpack('d',data[48:56])[0]
		self.tout = struct.unpack('d',data[56:64])[0]
		self.vmean = struct.unpack('d',data[64:72])[0]
		self.work = struct.unpack('d',data[72:80])[0]
		self.efficiency = struct.unpack('d',data[80:88])[0]
		self.powerout = struct.unpack('d',data[88:96])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.avatarid))
		io.write(struct.pack('d',self.tpass))
		io.write(struct.pack('d',self.mpass))
		io.write(struct.pack('d',self.trip))
		io.write(struct.pack('d',self.mrip))
		io.write(struct.pack('d',self.strokes))
		io.write(struct.pack('d',self.tin))
		io.write(struct.pack('d',self.tout))
		io.write(struct.pack('d',self.vmean))
		io.write(struct.pack('d',self.work))
		io.write(struct.pack('d',self.efficiency))
		io.write(struct.pack('d',self.powerout))
		return True
class proto_task:
	id = 5
	name = "task"
	size = 1
	bytesize = 9
	hash = "3993512e4594c79305ef1397b145b569"
	meta = (("distance",1,"double"),)
	def __init__(self):
		self.distance = 0.0;
	def decode(self,data):
		if len(data) < 8:
			return False
		self.distance = struct.unpack('d',data[0:8])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.distance))
		return True
class proto_multi2:
	id = 6
	name = "multi2"
	size = 6
	bytesize = 49
	hash = "fd979ae08bdb493287eeb0e19f503d44"
	meta = (("plotstat",1,"double"),("plotdyn",1,"double"),("resstatus",1,"double"),("xplotstat",1,"double"),("xplotdyn",1,"double"),("visualfeed",1,"double"),)
	def __init__(self):
		self.plotstat = 0.0;
		self.plotdyn = 0.0;
		self.resstatus = 0.0;
		self.xplotstat = 0.0;
		self.xplotdyn = 0.0;
		self.visualfeed = 0.0;
	def decode(self,data):
		if len(data) < 48:
			return False
		self.plotstat = struct.unpack('d',data[0:8])[0]
		self.plotdyn = struct.unpack('d',data[8:16])[0]
		self.resstatus = struct.unpack('d',data[16:24])[0]
		self.xplotstat = struct.unpack('d',data[24:32])[0]
		self.xplotdyn = struct.unpack('d',data[32:40])[0]
		self.visualfeed = struct.unpack('d',data[40:48])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.plotstat))
		io.write(struct.pack('d',self.plotdyn))
		io.write(struct.pack('d',self.resstatus))
		io.write(struct.pack('d',self.xplotstat))
		io.write(struct.pack('d',self.xplotdyn))
		io.write(struct.pack('d',self.visualfeed))
		return True
class proto_widget:
	id = 7
	name = "widget"
	size = 2
	bytesize = 17
	hash = "e4d4979b13b3cb0ebe20ff62663c2228"
	meta = (("widgetid",1,"double"),("visible",1,"double"),)
	def __init__(self):
		self.widgetid = 0.0;
		self.visible = 0.0;
	def decode(self,data):
		if len(data) < 16:
			return False
		self.widgetid = struct.unpack('d',data[0:8])[0]
		self.visible = struct.unpack('d',data[8:16])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.widgetid))
		io.write(struct.pack('d',self.visible))
		return True
class proto_cameramode:
	id = 8
	name = "cameramode"
	size = 2
	bytesize = 17
	hash = "6436d9c7db23a2264cba398af7b0017c"
	meta = (("mode",1,"double"),("entityid",1,"double"),)
	def __init__(self):
		self.mode = 0.0;
		self.entityid = 0.0;
	def decode(self,data):
		if len(data) < 16:
			return False
		self.mode = struct.unpack('d',data[0:8])[0]
		self.entityid = struct.unpack('d',data[8:16])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.mode))
		io.write(struct.pack('d',self.entityid))
		return True
class proto_cameraset:
	id = 9
	name = "cameraset"
	size = 7
	bytesize = 57
	hash = "62a457a83c57256c4329084b1bb6bd64"
	meta = (("mode",1,"double"),("position",3,"double"),("direction",3,"double"),)
	def __init__(self):
		self.mode = 0.0;
		self.position = array.array('d',[0 for i in range(0,3)]);
		self.direction = array.array('d',[0 for i in range(0,3)]);
	def decode(self,data):
		if len(data) < 56:
			return False
		self.mode = struct.unpack('d',data[0:8])[0]
		self.position = struct.unpack('3d',data[8:32])
		self.direction = struct.unpack('3d',data[32:56])
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.mode))
		io.write(struct.pack('3d',*self.position))
		io.write(struct.pack('3d',*self.direction))
		return True
class proto_subskills:
	id = 10
	name = "subskills"
	size = 11
	bytesize = 89
	hash = "3cb1f1630664490e0afa47ced8429666"
	meta = (("procedural",6,"double"),("PDC",5,"double"),)
	def __init__(self):
		self.procedural = array.array('d',[0 for i in range(0,6)]);
		self.PDC = array.array('d',[0 for i in range(0,5)]);
	def decode(self,data):
		if len(data) < 88:
			return False
		self.procedural = struct.unpack('6d',data[0:48])
		self.PDC = struct.unpack('5d',data[48:88])
		return True
	def encode(self,io):
		io.write(struct.pack('6d',*self.procedural))
		io.write(struct.pack('5d',*self.PDC))
		return True
class proto_energy_measures:
	id = 11
	name = "energy_measures"
	size = 4
	bytesize = 33
	hash = "3dee8f7f266a54c1d12bf15574fe7325"
	meta = (("energy_measures",4,"double"),)
	def __init__(self):
		self.energy_measures = array.array('d',[0 for i in range(0,4)]);
	def decode(self,data):
		if len(data) < 32:
			return False
		self.energy_measures = struct.unpack('4d',data[0:32])
		return True
	def encode(self,io):
		io.write(struct.pack('4d',*self.energy_measures))
		return True
class proto_phases_times:
	id = 12
	name = "phases_times"
	size = 9
	bytesize = 73
	hash = "6ee2b520cfdd6da26be89bb96b618c87"
	meta = (("phases_times",8,"double"),("drive_rec_ratio",1,"double"),)
	def __init__(self):
		self.phases_times = array.array('d',[0 for i in range(0,8)]);
		self.drive_rec_ratio = 0.0;
	def decode(self,data):
		if len(data) < 72:
			return False
		self.phases_times = struct.unpack('8d',data[0:64])
		self.drive_rec_ratio = struct.unpack('d',data[64:72])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('8d',*self.phases_times))
		io.write(struct.pack('d',self.drive_rec_ratio))
		return True
class proto_energy2:
	id = 13
	name = "energy2"
	size = 10
	bytesize = 81
	hash = "038f889d0cd84b1ace00a2914eb42ef5"
	meta = (("PO_err",1,"double"),("PO_tol",1,"double"),("opp_dist",1,"double"),("target_dist",1,"double"),("hull_pos_in",1,"double"),("WU_flag",1,"double"),("VO2_flag",1,"double"),("arrow_flag",1,"double"),("race_flag",1,"double"),("opp_flag",1,"double"),)
	def __init__(self):
		self.PO_err = 0.0;
		self.PO_tol = 0.0;
		self.opp_dist = 0.0;
		self.target_dist = 0.0;
		self.hull_pos_in = 0.0;
		self.WU_flag = 0.0;
		self.VO2_flag = 0.0;
		self.arrow_flag = 0.0;
		self.race_flag = 0.0;
		self.opp_flag = 0.0;
	def decode(self,data):
		if len(data) < 80:
			return False
		self.PO_err = struct.unpack('d',data[0:8])[0]
		self.PO_tol = struct.unpack('d',data[8:16])[0]
		self.opp_dist = struct.unpack('d',data[16:24])[0]
		self.target_dist = struct.unpack('d',data[24:32])[0]
		self.hull_pos_in = struct.unpack('d',data[32:40])[0]
		self.WU_flag = struct.unpack('d',data[40:48])[0]
		self.VO2_flag = struct.unpack('d',data[48:56])[0]
		self.arrow_flag = struct.unpack('d',data[56:64])[0]
		self.race_flag = struct.unpack('d',data[64:72])[0]
		self.opp_flag = struct.unpack('d',data[72:80])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.PO_err))
		io.write(struct.pack('d',self.PO_tol))
		io.write(struct.pack('d',self.opp_dist))
		io.write(struct.pack('d',self.target_dist))
		io.write(struct.pack('d',self.hull_pos_in))
		io.write(struct.pack('d',self.WU_flag))
		io.write(struct.pack('d',self.VO2_flag))
		io.write(struct.pack('d',self.arrow_flag))
		io.write(struct.pack('d',self.race_flag))
		io.write(struct.pack('d',self.opp_flag))
		return True
class proto_techexp:
	id = 14
	name = "techexp"
	size = 12
	bytesize = 97
	hash = "16bb28136d6dd73da800c44ef81996fa"
	meta = (("scenery_flag",1,"double"),("cube_flag",1,"double"),("VisFb_flag",1,"double"),("point_ev",8,"double"),("global_ev",1,"double"),)
	def __init__(self):
		self.scenery_flag = 0.0;
		self.cube_flag = 0.0;
		self.VisFb_flag = 0.0;
		self.point_ev = array.array('d',[0 for i in range(0,8)]);
		self.global_ev = 0.0;
	def decode(self,data):
		if len(data) < 96:
			return False
		self.scenery_flag = struct.unpack('d',data[0:8])[0]
		self.cube_flag = struct.unpack('d',data[8:16])[0]
		self.VisFb_flag = struct.unpack('d',data[16:24])[0]
		self.point_ev = struct.unpack('8d',data[24:88])
		self.global_ev = struct.unpack('d',data[88:96])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.scenery_flag))
		io.write(struct.pack('d',self.cube_flag))
		io.write(struct.pack('d',self.VisFb_flag))
		io.write(struct.pack('8d',*self.point_ev))
		io.write(struct.pack('d',self.global_ev))
		return True
class proto_coord3:
	id = 15
	name = "coord3"
	size = 2
	bytesize = 17
	hash = "55d8a8ec295e0ac413d8c2e7ca8d1f91"
	meta = (("error",1,"double"),("Fb_flag",1,"double"),)
	def __init__(self):
		self.error = 0.0;
		self.Fb_flag = 0.0;
	def decode(self,data):
		if len(data) < 16:
			return False
		self.error = struct.unpack('d',data[0:8])[0]
		self.Fb_flag = struct.unpack('d',data[8:16])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.error))
		io.write(struct.pack('d',self.Fb_flag))
		return True
class proto_avatarcolor:
	id = 16
	name = "avatarcolor"
	size = 5
	bytesize = 41
	hash = "e06e3fce2783c38b4f20b5369a680d54"
	meta = (("avatarid",1,"double"),("color",4,"double"),)
	def __init__(self):
		self.avatarid = 0.0;
		self.color = array.array('d',[0 for i in range(0,4)]);
	def decode(self,data):
		if len(data) < 40:
			return False
		self.avatarid = struct.unpack('d',data[0:8])[0]
		self.color = struct.unpack('4d',data[8:40])
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.avatarid))
		io.write(struct.pack('4d',*self.color))
		return True
class proto_avatarext:
	id = 17
	name = "avatarext"
	size = 3
	bytesize = 25
	hash = "853d468c57ee9e4a62caadc9acbad829"
	meta = (("avatarid",1,"double"),("backangle",1,"double"),("headangle",1,"double"),)
	def __init__(self):
		self.avatarid = 0.0;
		self.backangle = 0.0;
		self.headangle = 0.0;
	def decode(self,data):
		if len(data) < 24:
			return False
		self.avatarid = struct.unpack('d',data[0:8])[0]
		self.backangle = struct.unpack('d',data[8:16])[0]
		self.headangle = struct.unpack('d',data[16:24])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.avatarid))
		io.write(struct.pack('d',self.backangle))
		io.write(struct.pack('d',self.headangle))
		return True
class proto_avatarshirt:
	id = 18
	name = "avatarshirt"
	size = 2
	bytesize = 17
	hash = "ea2e3cc921adfaa0551d98c4728b3e7e"
	meta = (("avatarid",1,"double"),("shirt",1,"double"),)
	def __init__(self):
		self.avatarid = 0.0;
		self.shirt = 0.0;
	def decode(self,data):
		if len(data) < 16:
			return False
		self.avatarid = struct.unpack('d',data[0:8])[0]
		self.shirt = struct.unpack('d',data[8:16])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.avatarid))
		io.write(struct.pack('d',self.shirt))
		return True
class proto_rowconfig:
	id = 19
	name = "rowconfig"
	size = 2
	bytesize = 17
	hash = "bf751387aef6d5fb50374ddab3dacee7"
	meta = (("boats",1,"double"),("crew",1,"double"),)
	def __init__(self):
		self.boats = 0.0;
		self.crew = 0.0;
	def decode(self,data):
		if len(data) < 16:
			return False
		self.boats = struct.unpack('d',data[0:8])[0]
		self.crew = struct.unpack('d',data[8:16])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.boats))
		io.write(struct.pack('d',self.crew))
		return True
class proto_sprintdata:
	id = 20
	name = "sprintdata"
	size = 8
	bytesize = 65
	hash = "3cc5cb554740e50e6c97af3ab00fa63a"
	meta = (("time",1,"double"),("left_alpha_phi_fan",3,"double"),("right_alpha_phi_fan",3,"double"),("seat",1,"double"),)
	def __init__(self):
		self.time = 0.0;
		self.left_alpha_phi_fan = array.array('d',[0 for i in range(0,3)]);
		self.right_alpha_phi_fan = array.array('d',[0 for i in range(0,3)]);
		self.seat = 0.0;
	def decode(self,data):
		if len(data) < 64:
			return False
		self.time = struct.unpack('d',data[0:8])[0]
		self.left_alpha_phi_fan = struct.unpack('3d',data[8:32])
		self.right_alpha_phi_fan = struct.unpack('3d',data[32:56])
		self.seat = struct.unpack('d',data[56:64])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.time))
		io.write(struct.pack('3d',*self.left_alpha_phi_fan))
		io.write(struct.pack('3d',*self.right_alpha_phi_fan))
		io.write(struct.pack('d',self.seat))
		return True
class proto_audio:
	id = 21
	name = "audio"
	size = 4
	bytesize = 33
	hash = "70877dc8e6924b74d77a0c046e3e15a2"
	meta = (("time",1,"double"),("strokes_min",1,"double"),("phase",1,"double"),("volume",1,"double"),)
	def __init__(self):
		self.time = 0.0;
		self.strokes_min = 0.0;
		self.phase = 0.0;
		self.volume = 0.0;
	def decode(self,data):
		if len(data) < 32:
			return False
		self.time = struct.unpack('d',data[0:8])[0]
		self.strokes_min = struct.unpack('d',data[8:16])[0]
		self.phase = struct.unpack('d',data[16:24])[0]
		self.volume = struct.unpack('d',data[24:32])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.time))
		io.write(struct.pack('d',self.strokes_min))
		io.write(struct.pack('d',self.phase))
		io.write(struct.pack('d',self.volume))
		return True
class proto_vibrorun:
	id = 22
	name = "vibrorun"
	size = 2
	bytesize = 17
	hash = "6f55ff4e1d316430e613565fa626fa1a"
	meta = (("device",1,"double"),("activemotors",1,"double"),)
	def __init__(self):
		self.device = 0.0;
		self.activemotors = 0.0;
	def decode(self,data):
		if len(data) < 16:
			return False
		self.device = struct.unpack('d',data[0:8])[0]
		self.activemotors = struct.unpack('d',data[8:16])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.device))
		io.write(struct.pack('d',self.activemotors))
		return True
class proto_vibrosetup:
	id = 23
	name = "vibrosetup"
	size = 5
	bytesize = 41
	hash = "599408ef77c229cc460666aa28b4d57e"
	meta = (("device",1,"double"),("motor",1,"double"),("frequency_Hz",1,"double"),("offset_0_100",1,"double"),("dutycycle_0_100",1,"double"),)
	def __init__(self):
		self.device = 0.0;
		self.motor = 0.0;
		self.frequency_Hz = 0.0;
		self.offset_0_100 = 0.0;
		self.dutycycle_0_100 = 0.0;
	def decode(self,data):
		if len(data) < 40:
			return False
		self.device = struct.unpack('d',data[0:8])[0]
		self.motor = struct.unpack('d',data[8:16])[0]
		self.frequency_Hz = struct.unpack('d',data[16:24])[0]
		self.offset_0_100 = struct.unpack('d',data[24:32])[0]
		self.dutycycle_0_100 = struct.unpack('d',data[32:40])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('d',self.device))
		io.write(struct.pack('d',self.motor))
		io.write(struct.pack('d',self.frequency_Hz))
		io.write(struct.pack('d',self.offset_0_100))
		io.write(struct.pack('d',self.dutycycle_0_100))
		return True
class proto_start:
	id = 24
	name = "start"
	size = 42
	bytesize = 337
	hash = "450c95b10a3baa75bf7769e872ddff49"
	meta = (("taskuuid",36,"double"),("tasktype",1,"double"),("userid",1,"double"),("sessionid",1,"double"),("blockid",1,"double"),("simtime",1,"double"),("wintime",1,"double"),)
	def __init__(self):
		self.taskuuid = array.array('d',[0 for i in range(0,36)]);
		self.tasktype = 0.0;
		self.userid = 0.0;
		self.sessionid = 0.0;
		self.blockid = 0.0;
		self.simtime = 0.0;
		self.wintime = 0.0;
	def decode(self,data):
		if len(data) < 336:
			return False
		self.taskuuid = struct.unpack('36d',data[0:288])
		self.tasktype = struct.unpack('d',data[288:296])[0]
		self.userid = struct.unpack('d',data[296:304])[0]
		self.sessionid = struct.unpack('d',data[304:312])[0]
		self.blockid = struct.unpack('d',data[312:320])[0]
		self.simtime = struct.unpack('d',data[320:328])[0]
		self.wintime = struct.unpack('d',data[328:336])[0]
		return True
	def encode(self,io):
		io.write(struct.pack('36d',*self.taskuuid))
		io.write(struct.pack('d',self.tasktype))
		io.write(struct.pack('d',self.userid))
		io.write(struct.pack('d',self.sessionid))
		io.write(struct.pack('d',self.blockid))
		io.write(struct.pack('d',self.simtime))
		io.write(struct.pack('d',self.wintime))
		return True
