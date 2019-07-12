import bpy
import math
import sys

############# lib ########################

def degToRad(deg):
    return 2 * math.pi / 360 * deg

def getObjHeight(obj):
    obj.select_set(True)
    x, y, z = bpy.context.active_object.dimensions
    return z

def getObjThickness(obj):
    obj.select_set(True)
    x, y, z = bpy.context.active_object.dimensions
    return y

def getEdgeVerts(obj):
    if obj.type != "MESH":
        print('Error: getEdgeVerts failed', file=sys.stderr)
        sys.exit(1)
    else:
        return obj.data.vertices
    
def getMinMaxLocation():
    obj = bpy.data.objects["Collision"] #Hard coding
    verts = getEdgeVerts(obj)
    xMax = 0
    xMin = 0
    yMax = 0
    yMin = 0
    zMax = 0
    zMin = 0
    for vert in verts:
        location = vert.co
        if location.x > xMax:
            xMax = location.x
        if location.x < xMin:
            xMin = location.x
        if location.y > yMax:
            yMax = location.y
        if location.y < yMin:
            yMin = location.y
        if location.z > zMax:
            zMax = location.z
        if location.z < zMin:
            zMin = location.z
    return [[xMin, yMin, zMin],[xMax, yMax, zMax]]
    
def move(obj, minMaxLocation):
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    obj.select_set(False)
    obj.scale *= 0.001
    if 'P0005' in obj.name: #Hard coding BACK
        obj.rotation_euler.y = degToRad(-90) #Hard coding
        obj.rotation_euler.z = degToRad(-90) #Hard coding
        obj.location = (0, minMaxLocation[1][1], minMaxLocation[1][2])
    elif 'P0018' in obj.name: #Hard coding FRONT
        obj.rotation_euler.y = degToRad(-90) #Hard coding
        obj.rotation_euler.z = degToRad(-90) #Hard coding
        obj.location = (0, minMaxLocation[0][1], minMaxLocation[1][2])
    elif 'P0031' in obj.name: #Hard coding SLEEVE
        obj.rotation_euler.y = degToRad(-120) #Hard coding
        obj.location = (minMaxLocation[1][0]/2, 0, minMaxLocation[1][2])
        obj.select_set(True)
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(-minMaxLocation[1][0], 0, 0)})
        obj.select_set(False)
        bpy.ops.transform.rotate(value=degToRad(-60), orient_axis='Y')
        #bpy.ops.object.rotation_euler.y = degToRad(60)
        
    elif 'P0044' in obj.name: #Hard coding COLLAR
        obj.rotation_euler.x = degToRad(-90) #Hard coding
        obj.location = (0, minMaxLocation[1][1], minMaxLocation[1][2])

def propSet(obj):
    obj.data.dimensions = '2D'
    obj.data.splines[0].use_cyclic_u = True
    obj.data.twist_mode = 'MINIMUM'
    obj.data.fill_mode = 'BOTH'
    #obj.editmode_toggle()

def remove(obj):
    bpy.data.objects.remove(obj)
    
def execPreProcess(objects):
    for obj in objects:
        if obj.type == "CURVE":
            minMaxLocation = getMinMaxLocation()
            move(obj, minMaxLocation)
            propSet(obj)
            
        elif obj.type == "MESH":
            if obj.name != 'Collision': #Hard coding
                bpy.data.objects.remove(obj)
            continue
        else:
            remove(obj)
            
################ main ######################

objects = bpy.context.visible_objects
execPreProcess(objects)