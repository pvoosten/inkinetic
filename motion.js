moveWolk = function(){
	wolk.setX(-550);
	wolk.setOpacity(0.5);
	wolk.transitionTo({duration:40, callback:moveWolk, x:200, opacity:1,});
};
moveWolk();


