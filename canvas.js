comment = function(cmt){
document.getElementById('comments').innerHTML=cmt;
}

var stage = new Kinetic.Stage({
        container:'container',
        width:354.33069,
        height:354.33069
        });
// Create a new layer
var layer2 = new Kinetic.Layer();
var g3076 = new Kinetic.Group();
var path3082 = new Kinetic.Path({
        x: 0,
        y: 0,
        data: "m 237.10597,976.34162 41.59878,41.87848 0,-125.97536 -41.59878,-78.96696 z",
        });
path3082.setFill('#8686bf');
comment("made it to here");
g3076.add(path3082); // add to the g3076 group
var path3078 = new Kinetic.Path({
        x: 0,
        y: 0,
        data: "m 237.10597,976.34162 0,-163.06384 -157.221067,-59.14271 0,193.33234 z",
        });
path3078.setFill('#353564');
g3076.add(path3078); // add to the g3076 group
var path3080 = new Kinetic.Path({
        x: 0,
        y: 0,
        data: "m 237.10597,976.34162 41.59878,41.87848 -110.81743,-15.6409 -88.002417,-55.11179 z",
        });
path3080.setFill('#4d4d9f');
g3076.add(path3080); // add to the g3076 group
var path3088 = new Kinetic.Path({
        x: 0,
        y: 0,
        data: "m 79.884903,947.46741 88.002417,55.11179 0,-143.30895 -88.002417,-105.13518 z",
        });
path3088.setFill('#e9e9ff');
g3076.add(path3088); // add to the g3076 group
var path3086 = new Kinetic.Path({
        x: 0,
        y: 0,
        data: "M 237.10597,813.27778 278.70475,892.24474 167.88732,859.27025 79.884903,754.13507 z",
        });
path3086.setFill('#afafde');
g3076.add(path3086); // add to the g3076 group
var path3084 = new Kinetic.Path({
        x: 0,
        y: 0,
        data: "m 278.70475,1018.2201 0,-125.97536 -110.81743,-32.97449 0,143.30895 z",
        });
path3084.setFill('#d7d7ff');
g3076.add(path3084); // add to the g3076 group
g3076.setFill('#00ff00');
layer2.add(g3076); // add g3076 to layer
stage.add(layer2); // add the layer to the stage

// Create a new layer
var layer3 = new Kinetic.Layer();
stage.add(layer3); // add the layer to the stage

// Create a new layer
var layer1 = new Kinetic.Layer();
stage.add(layer1); // add the layer to the stage
