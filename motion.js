moveWolk = function(){
	wolk.setX(-550);
	wolk.setOpacity(0.5);
	wolk.transitionTo({duration:40, callback:moveWolk, x:200, opacity:1,});
};
moveWolk();

// Make things move in this file.

var r = new Kinetic.Rect({x:200 + 100/2, y:900 + 5/2, width: 100, height: 5, fill: '#FF0000',
offset: {x:100/2, y:5/2},
// rotationDeg: -30,
});
var rr = new Kinetic.Rect({x:200, y:900, width: 100, height: 5, fill: '#FF0000'});
layer2.add(r);
layer2.add(rr);
layer2.draw();

turn = function(){
	r.setRotation(0);
	r.transitionTo({rotation: Math.PI, duration: 5, callback: turn});
}

turn();

