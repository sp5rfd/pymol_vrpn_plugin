import pymol

MOBILE="mobile"
REGION="region"
TARGET="target"

cmd.load("helix.pdb",MOBILE)
cmd.load("1fg0.pdb",TARGET)
cmd.hide("lines")
cmd.show("cartoon")
cmd.color("red",MOBILE)
cmd.color("green",TARGET)

mobile_com=cmd.centerofmass(MOBILE)
target_com=cmd.centerofmass(TARGET)
print "mobile_com=", mobile_com, "target_com=", target_com

cmd.translate(object=MOBILE, vector=[-mobile_com[0],-mobile_com[1],-mobile_com[2]], camera=0)
cmd.translate(object=TARGET, vector=[-target_com[0],-target_com[1],-target_com[2]], camera=0)
cmd.center()

print cmd.select(REGION,"target and resi 2654-2658")

align_result=cmd.align(MOBILE,REGION)

mobile_com=cmd.centerofmass(MOBILE)
region_com=cmd.centerofmass(REGION)

print "mobile_com=", mobile_com, "region_com=", region_com

cmd.translate(object=MOBILE, vector=[-(mobile_com[0]-region_com[0]),-(mobile_com[1]-region_com[1]),-(mobile_com[2]-region_com[2])],camera=0)

print "ALIGNMENT: ",align_result
