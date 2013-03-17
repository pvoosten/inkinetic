var stage = new Kinetic.Stage({
        container:'container',
        width:574.28571,
        height:462.85727
        });

// Create a new layer
var layer2 = new Kinetic.Layer({"y": -663.78941, "x": 68.57143, "id": "layer2"});
var g3839 = new Kinetic.Group({"y": 462.85714, "x": -208.57143, "id": "g3839"});
var rect3833 = new Kinetic.Rect({"height": 162.85715, "width": 574.28571, "y": 200.93227, "x": 140.0, "id": "rect3833", "fill": "#008080"});
g3839.add(rect3833); // add to the g3839 group
var rect3835 = new Kinetic.Rect({"height": 94.285721, "width": 574.28571, "y": 360.93228, "x": 140.0, "id": "rect3835", "fill": "#00ffff"});
g3839.add(rect3835); // add to the g3839 group
var rect3837 = new Kinetic.Rect({"height": 211.42873, "width": 574.28571, "y": 452.36081, "x": 140.0, "id": "rect3837", "fill": "#ff6600"});
g3839.add(rect3837); // add to the g3839 group
layer2.add(g3839); // add g3839 to layer
var wolk = new Kinetic.Path({"opacity": "0.5", "data": "m 377.16454,721.40513 c -85.88206,-29.86711 -75.14244,85.13194 -15.20757,44.64116 4.29621,-1.1926 10.19099,-6.36757 8.8329,1.02253 -4.67292,40.05549 85.2157,30.45556 81.30633,3.5911 1.77981,-4.01316 -1.57502,-17.61279 5.96507,-9.12455 42.77611,51.35003 55.78209,-36.3136 31.88878,-44.28938 -3.42693,-3.18196 -17.0662,2.40741 -7.96557,-0.6854 33.81772,-21.54802 12.56377,-53.36907 -27.38486,-37.90898 -8.37205,2.90679 -14.66639,11.04047 -10.47969,18.11051 -23.30246,-25.76861 -81.69983,8.65359 -66.90532,23.15525 z", "id": "wolk", "fill": "#ffffff"});
layer2.add(wolk); // add wolk to layer
stage.add(layer2); // add the layer to the stage

// Create a new layer
var layer3 = new Kinetic.Layer({"y": -663.78941, "x": 68.57143, "id": "layer3"});
stage.add(layer3); // add the layer to the stage

// Create a new layer
var layer1 = new Kinetic.Layer({"y": -663.78941, "x": 68.57143, "id": "layer1"});
stage.add(layer1); // add the layer to the stage
