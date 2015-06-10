# Rowing Protocols
# - COORD3
# - ENERGY2
# - TECHOPT
# 
# Note: protocols can be extended as wish by adding new entities
# Protocol can be extended as wish but not reduced.
# Protocol(name of protocol, identifier, list of variables)
# list of variables: list of pairs name and size. If size is not specified it is 1
# You can use also 
#
# Types for protos: default is double: allowed uint8 int32 single char

# \name Environment Protocol
# \description Provides the fundamental information about the Virtual Environment
#
# \param time Time in the Simulation
# \param camera The position of the Camera 
Protocol("env",0,["time",("camera",3)])

# boat features
Protocol("boat",1,["boatid",("position",3),"psi"])

# avatar performance: avatar is identified as: boatid*10+avatarid
# seat of avatar is relative to reference position of avatar
Protocol("avatar",2,["avatarid",("alphas",2),("phis",2),"seat"])

# controls the visibility of an entity: boatid*10+avatarid
Protocol("visibility",3,["entityid","show"])

# user performance (can be sent at lower rate)
Protocol("user_perf",4,["avatarid","tpass", "mpass", "trip" , "mrip" , "strokes"  , "tin" , "tout" , "vmean" , "work" , "efficiency","powerout",])

# task performance
Protocol("task",5,["distance"])

# MULTI2 specific
# xplotstat == plotstat marks plotting of statistics  => remove
# xplotdyn == plotDyn plots dynamic => remove
# resstatus not used
# visualfeed ignored
#
# xplot = stat or dynamic
#
# On change of xplot makes start or stop plotting
# TODO: manca hide all controlled externally and not by app?
Protocol("multi2",6,["plotstat","plotdyn","resstatus","xplotstat","xplotdyn","visualfeed"])

# show widget: speedometer=0,time=1,digitalclock=2,bimanual=3,drr=4,distance=5,trafficlight=6,power=7,taskdistance=8
Protocol("widget",7,["widgetid","visible"])

# cameramode: CAMMODE_AVATAR_BACK=0,CAMMODE_BOAT_BACK=1,CAMMODE_AVATAR_FRONT=2,CAMMODE_BOAT_FRONT=3,CAMMODE_BOAT_TOP=4,CAMMODE_BOAT_SIDE=5,CAMMODE_BOAT_TOP_FAR=6,CAMMODE_FREE=7
Protocol("cameramode",8,["mode","entityid"])

# modifies a given camera
Protocol("cameraset",9,["mode",("position",3),("direction",3)])

# subskills
Protocol("subskills",10,[("procedural",6),("PDC",5)])

# energy_measures
Protocol("energy_measures",11,[("energy_measures",4)])

# phases times
Protocol("phases_times",12,[("phases_times",8),"drive_rec_ratio"])

#energy2
Protocol("energy2",13,["PO_err","PO_tol","opp_dist","target_dist","hull_pos_in","WU_flag","VO2_flag","arrow_flag","race_flag","opp_flag","opt_flow_gain","countdown"])

# Techexp
Protocol("techexp",14,["scenery_flag","cube_flag","VisFb_flag",("point_ev",8),("global_ev",1)])

#Coord3
Protocol("coord3",15,["error","Fb_flag"])

#Avatar Coloring
Protocol("avatarcolor",16,["avatarid",("color",4)])

#Avatar Head
Protocol("avatarext",17,["avatarid","backangle","headangle"])

#Avatar Shirt: 0=blue 1=green,2=organge,3=black
Protocol("avatarshirt",18,["avatarid","shirt"])

# Configuress
Protocol("rowconfig",19,["boats","crew"])

# Real SPRINT data
Protocol("sprintdata",20,["time",("left_alpha_phi_fan",3),("right_alpha_phi_fan",3),"seat"])

# Audio
Protocol("audio",21,["time","strokes_min","phase","volume"])
#Vibro
Protocol("vibrorun",22,["device","activemotors"])

Protocol("vibrosetup",23,["device","motor","frequency_Hz","offset_0_100","dutycycle_0_100"])

#Protocol("start",24,[("task",16,char),("userid",int32),("sessionid",int32),("blockid",int32),"systime","wintime"])
Protocol("start",24,[("taskuuid",36),"tasktype","userid","sessionid","blockid","simtime","wintime"])

#Freerunning protocol
Protocol("freerunning",25,["time","boat_pos","boat_speed","strokes","strokes_min","power","average_speed","average_pow"])

#Transfer Faults protocol
Protocol("techfaults",26,["fb_flag","skying","deepentry","earlyfinish","seatsliding","forcefinish","shoulderraising","backleaning"])

Protocol("avataroar",27,["avatarid","oarrots","oarrotd"])

#Avatar Shirt: 0=blue 1=green,2=organge,3=black
#Protocol("avatarbody",28,["avatarid",(])

