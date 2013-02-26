var stage = new Kinetic.Stage({
        container:'container',
        width:574.28571,
        height:462.85727
        });

// Create a new layer
var layer2 = new Kinetic.Layer();
var g3839 = new Kinetic.Group();
var rect3833 = new Kinetic.Rect({
        x: 140.0,
        y: 200.93227,
        width: 574.28571,
        height: 162.85715,
        });
rect3833.setFill('#008080');
g3839.add(rect3833); // add to the g3839 group
var rect3835 = new Kinetic.Rect({
        x: 140.0,
        y: 360.93228,
        width: 574.28571,
        height: 94.285721,
        });
rect3835.setFill('#00ffff');
g3839.add(rect3835); // add to the g3839 group
var rect3837 = new Kinetic.Rect({
        x: 140.0,
        y: 452.36081,
        width: 574.28571,
        height: 211.42873,
        });
rect3837.setFill('#ff6600');
g3839.add(rect3837); // add to the g3839 group
g3839.setAbsolutePosition(-208.57143, 462.85714);
layer2.add(g3839); // add g3839 to layer
var wolk = new Kinetic.Path({
        x: 0,
        y: 0,
        data: "m 377.16454,721.40513 c -85.88206,-29.86711 -75.14244,85.13194 -15.20757,44.64116 4.29621,-1.1926 10.19099,-6.36757 8.8329,1.02253 -4.67292,40.05549 85.2157,30.45556 81.30633,3.5911 1.77981,-4.01316 -1.57502,-17.61279 5.96507,-9.12455 42.77611,51.35003 55.78209,-36.3136 31.88878,-44.28938 -3.42693,-3.18196 -17.0662,2.40741 -7.96557,-0.6854 33.81772,-21.54802 12.56377,-53.36907 -27.38486,-37.90898 -8.37205,2.90679 -14.66639,11.04047 -10.47969,18.11051 -23.30246,-25.76861 -81.69983,8.65359 -66.90532,23.15525 z",
        });
wolk.setFill('#ffffff');
wolk.setOpacity(0.5);
layer2.add(wolk); // add wolk to layer
layer2.setAbsolutePosition(68.57143, -663.78941);
stage.add(layer2); // add the layer to the stage

// Create a new layer
var layer3 = new Kinetic.Layer();
layer3.setAbsolutePosition(68.57143, -663.78941);
stage.add(layer3); // add the layer to the stage

// Create a new layer
var layer1 = new Kinetic.Layer();
layer1.setAbsolutePosition(68.57143, -663.78941);
stage.add(layer1); // add the layer to the stage


