# =============================================================================
# PROJECT CHRONO - http:#projectchrono.org
#
# Copyright (c) 2014 projectchrono.org
# All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be found
# in the LICENSE file at the top level of the distribution and at
# http:#projectchrono.org/license-chrono.txt.
#
# =============================================================================
# Authors: Simone Benatti
# =============================================================================
#
# RoboSimian on rigid terrain
#
# =============================================================================
import os
import math
import pychrono as chrono
import pychrono.robosimian as robosimian
try:
   from pychrono import irrlicht as chronoirr
except:
   print('Could not import ChronoIrrlicht')

chrono.SetChronoDataPath('C:/codes/ChronoRobosimian/data/')
time_step = 1e-3

# Drop the robot on rigid terrain
drop = True

# Robot locomotion mode
mode = robosimian.LocomotionMode_WALK

# Contact method (system type)
contact_method = chrono.ChMaterialSurfaceSMC()

# Phase durations
duration_pose = 1.0          # Interval to assume initial pose
duration_settle_robot = 0.5  # Interval to allow robot settling on terrain
duration_sim = 10            # Duration of actual locomotion simulation

# Output frequencies
output_fps = 100
render_fps = 60

# Output directories
out_dir = "./ROBOSIMIAN_RIGID"
pov_dir = out_dir + "/POVRAY"
img_dir = out_dir + "/IMG"

# POV-Ray and/or IMG output
data_output = True
povray_output = False
image_output = False

# =============================================================================

class RayCaster:

    def __init__(self, sys, origin, dims, spacing):
        self.m_sys = sys
        self.m_origin = origin
        self.m_dims = dims
        self.m_spacing = spacing
        self.m_points = []
        
        self.m_body = sys.NewBody()
        self.m_body.SetBodyFixed(True)
        self.m_body.SetCollide(False)
        self.m_sys.AddBody(self.m_body)
        

        self.m_glyphs = chrono.ChGlyphs()
        self.m_glyphs.SetGlyphsSize(0.004)
        self.m_glyphs.SetZbufferHide(True)
        self.m_glyphs.SetDrawMode(chrono.ChGlyphs.GLYPH_POINT)
        self.m_body.AddAsset(self.m_glyphs)


    def Update(self):
        m_points = []
        direc = self.m_origin.GetA().Get_A_Zaxis()
        nx = round(self.m_dims[0]/self.m_spacing)
        ny = round(self.m_dims[1]/self.m_spacing)
        for ix in range(nx):
            for iy in range(ny):
                x_local = -0.5 * self.m_dims[0] + ix * self.m_spacing
                y_local = -0.5 * self.m_dims[1] + iy * self.m_spacing
                from_vec = self.m_origin.TransformPointLocalToParent(chrono.ChVectorD(x_local, y_local, 0.0))
                to = from_vec + direc * 100
                result = chrono.ChRayhitResult()
                self.m_sys.GetCollisionSystem().RayHit(from_vec, to, result)
                if (result.hit):
                    m_points.append(result.abs_hitPoint)
            
        
        
        self.m_glyphs.Reserve(0)
        for point_id in range(m_points.size()) :
            self.m_glyphs.SetGlyphPoint(point_id, m_points[point_id], chrono.ChColor(1, 1, 0))
        


# =============================================================================

def CreateTerrain(robot, length, width, height, offset) :
    ground = robot.GetSystem().NewBody()
    ground.SetBodyFixed(True)
    ground.SetCollide(True)

    ground.GetCollisionModel().ClearModel()
    ground.GetCollisionModel().AddBox(length / 2, width / 2, 0.1, chrono.ChVectorD(offset, 0, height - 0.1))
    ground.GetCollisionModel().BuildModel()

    box = chrono.ChBoxShape()
    box.GetBoxGeometry().Size = chrono.ChVectorD(length / 2, width / 2, 0.1)
    box.GetBoxGeometry().Pos = chrono.ChVectorD(offset, 0, height - 0.1)
    ground.AddAsset(box)

    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile("pinkwhite.png"))
    texture.SetTextureScale(10 * length, 10 * width)
    ground.AddAsset(texture)

    ground.AddAsset(chrono.ChColorAsset(0.8, 0.8, 0.8))

    robot.GetSystem().AddBody(ground)

    return ground


def SetContactProperties(robot):
    friction = 0.8
    Y = 1e7
    cr = 0.0

    CM = robot.GetSystem().GetContactMethod()
    
    #if  isinstance(CM, chrono.ChMaterialCompositeNSC):
    if  CM == 0:
        robot.GetSledBody().GetMaterialSurfaceNSC().SetFriction(friction)
        robot.GetWheelBody(robosimian.FR).GetMaterialSurfaceNSC().SetFriction(friction)
        robot.GetWheelBody(robosimian.FL).GetMaterialSurfaceNSC().SetFriction(friction)
        robot.GetWheelBody(robosimian.RR).GetMaterialSurfaceNSC().SetFriction(friction)
        robot.GetWheelBody(robosimian.RL).GetMaterialSurfaceNSC().SetFriction(friction)

        
    elif  CM == 1:
    #elif  isinstance(CM, chrono.ChMaterialCompositeSMC):
        robot.GetSledBody().GetMaterialSurfaceSMC().SetFriction(friction)
        robot.GetWheelBody(robosimian.FR).GetMaterialSurfaceSMC().SetFriction(friction)
        robot.GetWheelBody(robosimian.FL).GetMaterialSurfaceSMC().SetFriction(friction)
        robot.GetWheelBody(robosimian.RR).GetMaterialSurfaceSMC().SetFriction(friction)
        robot.GetWheelBody(robosimian.RL).GetMaterialSurfaceSMC().SetFriction(friction)

        robot.GetSledBody().GetMaterialSurfaceSMC().SetYoungModulus(Y)
        robot.GetWheelBody(robosimian.FR).GetMaterialSurfaceSMC().SetYoungModulus(Y)
        robot.GetWheelBody(robosimian.FL).GetMaterialSurfaceSMC().SetYoungModulus(Y)
        robot.GetWheelBody(robosimian.RR).GetMaterialSurfaceSMC().SetYoungModulus(Y)
        robot.GetWheelBody(robosimian.RL).GetMaterialSurfaceSMC().SetYoungModulus(Y)

        robot.GetSledBody().GetMaterialSurfaceSMC().SetRestitution(cr)
        robot.GetWheelBody(robosimian.FR).GetMaterialSurfaceSMC().SetRestitution(cr)
        robot.GetWheelBody(robosimian.FL).GetMaterialSurfaceSMC().SetRestitution(cr)
        robot.GetWheelBody(robosimian.RR).GetMaterialSurfaceSMC().SetRestitution(cr)
        robot.GetWheelBody(robosimian.RL).GetMaterialSurfaceSMC().SetRestitution(cr)

    else :    
        raise Exception('Unvalid contact method')
    

def SetGroundContactProperties(ground, sys) :
    friction = 0.8
    Y = 1e7
    cr = 0.0
    CM = sys.GetContactMethod()
 
    if  CM == 0:
    #if  isinstance(CM, chrono.ChMaterialCompositeNSC):
        ground.GetMaterialSurfaceNSC().SetFriction(friction)
        
    elif  CM == 1:
    #elif  isinstance(CM, chrono.ChMaterialCompositeNSC):
        ground.GetMaterialSurfaceSMC().SetFriction(friction)
        ground.GetMaterialSurfaceSMC().SetYoungModulus(Y)
        ground.GetMaterialSurfaceSMC().SetRestitution(cr)
        
    else:
        
        raise Exception('Unvalid contact method')
    

# =============================================================================

# ------------
# Timed events
# ------------

time_create_terrain = duration_pose                       # create terrain after robot assumes initial pose
time_start = time_create_terrain + duration_settle_robot  # start actual simulation after robot settling
time_end = time_start + duration_sim                      # end simulation after specified duration

# -------------
# Create system
# -------------

if  isinstance(contact_method, chrono.ChMaterialSurfaceNSC):
		my_sys = chrono.ChSystemNSC()

if  isinstance(contact_method, chrono.ChMaterialSurfaceSMC):
		my_sys = chrono.ChSystemSMC()



my_sys.SetMaxItersSolverSpeed(200)
my_sys.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN)
my_sys.Set_G_acc(chrono.ChVectorD(0, 0, -9.8))
##my_sys.Set_G_acc(ChVector<double>(0, 0, 0))

# -----------------------
# Create RoboSimian robot
# -----------------------

robot = robosimian.RoboSimian(my_sys, True, True)

# Set output directory

robot.SetOutputDirectory(out_dir)

# Set actuation mode for wheel motors

##robot.SetMotorActuationMode(robosimian::ActuationMode::ANGLE)

# Control collisions (default: True for sled and wheels only)

##robot.SetCollide(robosimian::CollisionFlags::NONE)
##robot.SetCollide(robosimian::CollisionFlags::ALL)
##robot.SetCollide(robosimian::CollisionFlags::LIMBS)
##robot.SetCollide(robosimian::CollisionFlags::CHASSIS | robosimian::CollisionFlags::WHEELS)

# Set visualization modes (default: all COLLISION)

##robot.SetVisualizationTypeChassis(robosimian::VisualizationType::MESH)
##robot.SetVisualizationTypeLimb(robosimian::FL, robosimian::VisualizationType::COLLISION)
##robot.SetVisualizationTypeLimb(robosimian::FR, robosimian::VisualizationType::COLLISION)
##robot.SetVisualizationTypeLimb(robosimian::RL, robosimian::VisualizationType::COLLISION)
##robot.SetVisualizationTypeLimb(robosimian::RR, robosimian::VisualizationType::COLLISION)
##robot.SetVisualizationTypeLimbs(robosimian::VisualizationType::NONE)
##robot.SetVisualizationTypeChassis(robosimian::VisualizationType::MESH)
##robot.SetVisualizationTypeSled(robosimian::VisualizationType::MESH)
##robot.SetVisualizationTypeLimbs(robosimian::VisualizationType::MESH)

# Initialize Robosimian robot

##robot.Initialize(ChCoordsys<>(chrono.ChVectorD(0, 0, 0), QUNIT))
robot.Initialize(chrono.ChCoordsysD(chrono.ChVectorD(0, 0, 0), chrono.Q_from_AngX(chrono.CH_C_PI)))

# -----------------------------------
# Create a driver and attach to robot
# -----------------------------------

if mode == robosimian.LocomotionMode_WALK:
		driver = robosimian.Driver(
			"",                                                           # start input file
			chrono.GetChronoDataFile("robosimian/actuation/walking_cycle.txt"),  # cycle input file
			"",                                                           # stop input file
			True)
elif mode == robosimian.LocomotionMode_SCULL:
		driver = robosimian.Driver(
			chrono.GetChronoDataFile("robosimian/actuation/sculling_start.txt"),   # start input file
			chrono.GetChronoDataFile("robosimian/actuation/sculling_cycle2.txt"),  # cycle input file
			chrono.GetChronoDataFile("robosimian/actuation/sculling_stop.txt"),    # stop input file
			True)

elif mode == robosimian.LocomotionMode_INCHWORM:
		driver = robosimian.Driver(
			chrono.GetChronoDataFile("robosimian/actuation/inchworming_start.txt"),  # start input file
			chrono.GetChronoDataFile("robosimian/actuation/inchworming_cycle.txt"),  # cycle input file
			chrono.GetChronoDataFile("robosimian/actuation/inchworming_stop.txt"),   # stop input file
			True)

elif mode == robosimian.LocomotionMode_DRIVE:
		driver = robosimian.Driver(
			chrono.GetChronoDataFile("robosimian/actuation/driving_start.txt"),  # start input file
			chrono.GetChronoDataFile("robosimian/actuation/driving_cycle.txt"),  # cycle input file
			chrono.GetChronoDataFile("robosimian/actuation/driving_stop.txt"),   # stop input file
			True)
else:
    raise('Unvalid contact method')

cbk = robosimian.RobotDriverCallback(robot)
driver.RegisterPhaseChangeCallback(cbk)

driver.SetTimeOffsets(duration_pose, duration_settle_robot)
robot.SetDriver(driver)

# -------------------------------
# Cast rays into collision models
# -------------------------------

##RayCaster caster(my_sys, ChFrame<>(chrono.ChVectorD(2, 0, -1), Q_from_AngY(-CH_C_PI_2)), ChVector2<>(2.5, 2.5),
#/ 0.02)
caster = RayCaster(my_sys, chrono.ChFrameD(chrono.ChVectorD(0, -2, -1), chrono.Q_from_AngX(-chrono.CH_C_PI_2)), [2.5, 2.5], 0.02)

# -------------------------------
# Create the visualization window
# -------------------------------

application = chronoirr.ChIrrApp(my_sys, "RoboSimian - Rigid terrain",
									chronoirr.dimension2du(800, 600))
application.AddTypicalLogo(chrono.GetChronoDataPath() + 'logo_pychrono_alpha.png')
application.AddTypicalSky()
application.AddTypicalCamera(chronoirr.vector3df(1, -2.75, 0.2), chronoirr.vector3df(1, 0, 0))
application.AddTypicalLights(chronoirr.vector3df(100, 100, 100), chronoirr.vector3df(100, -100, 80))
application.AddLightWithShadow(chronoirr.vector3df(10, -6, 3), chronoirr.vector3df(0, 0, 0), 3, -10, 10,
							   40, 512)

application.AssetBindAll()
application.AssetUpdateAll()

# -----------------------------
# Initialize output directories
# -----------------------------

os.mkdir(out_dir)

if (povray_output) :
    os.mkdir(pov_dir)
    
if (image_output) :
    os.mkdir(img_dir)

# ---------------------------------
# Run simulation for specified time
# ---------------------------------

output_steps = math.ceil((1.0 / output_fps) / time_step)
render_steps = math.ceil((1.0 / render_fps) / time_step)
sim_frame = 0
output_frame = 0
render_frame = 0

terrain_created = False

while (application.GetDevice().run()) :
	##caster.Update()
    if (drop and not terrain_created and my_sys.GetChTime() > time_create_terrain) :
		# Set terrain height
        z = robot.GetWheelPos(robosimian.LIMB_FR).z - 0.15

		# Rigid terrain parameters
        length = 8
        width = 2

        # Create terrain
        hdim = chrono.ChVectorD(length / 2, width / 2, 0.1)
        loc = chrono.ChVectorD(length / 4, 0, z - 0.1)
        ground = CreateTerrain(robot, length, width, z, length / 4)
        SetContactProperties(robot)
        SetGroundContactProperties(ground, my_sys)
        application.AssetBind(ground)
        application.AssetUpdate(ground)
        robot.GetChassisBody().SetBodyFixed(False)
        terrain_created = True
	

    application.BeginScene(True, True, chronoirr.SColor(255, 140, 161, 192))
    application.DrawAll()

    if (data_output and sim_frame % output_steps == 0) :
        robot.Output()

# Output POV-Ray date and/or snapshot images
    if(sim_frame % render_steps == 0) :
        if (povray_output) :
            filename = pov_dir + '/data_' + str(render_frame + 1) +'04d.dat' 
            chrono.WriteShapesPovray(my_sys, filename)
		
        if (image_output) :
            filename = img_dir + '/img_' + str(render_frame + 1) +'04d.jpg' 
            image = application.GetVideoDriver().createScreenShot()
            if (image) :
                application.GetVideoDriver().writeImageToFile(image, filename)
                image.drop()
			
		

        render_frame += 1
	

	##time = my_sys.GetChTime()
	##A = CH_C_PI / 6
	##freq = 2
	##val = 0.5 * A * (1 - std::cos(CH_C_2PI * freq * time))
	##robot.Activate(robosimian::FR, "joint2", time, val)
	##robot.Activate(robosimian::RL, "joint5", time, val)

    robot.DoStepDynamics(time_step)

	##if (my_sys.GetNcontacts() > 0) {
	##    robot.ReportContacts()
	##}

    sim_frame += 1

    application.EndScene()


print("avg. speed: "  + str(cbk.GetAvgSpeed()) + '/n')

del my_sys

