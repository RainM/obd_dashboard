var fixtures = {};

fixtures.PLATES = [
    {
	w: 1,
	h: 1,
	x: 0,
	y: 0,
	title: 'AT Temp, C',
	canvas_text: 'data-type="radial-gauge"',
	ws_selector: 'at_temp',
	plate_ctor: function(elem) {
	    return new RadialGauge(
		{
		    renderTo: elem
		}
	    ).draw();
	},
	on_update: function(new_value, plate) {
	    
	}
    },
    {
	w: 1,
	h: 1,
	x: 1,
	y: 0,
	title: 'RPM',
	canvas_text: 'data-type="radial-gauge"',
	ws_selector: 'engine_rpm',
	plate_ctor: function(elem) {
	    return new RadialGauge(
		{
		    renderTo: elem,
		    maxValue: 6000,
		    animationRule: 'bounce',
		    animationDuration: 200
		}
	    ).draw();
	},
	on_update: function(new_value, plate) {
	    plate.value = new_value;
	    //plate.update();
	}
    },
    {
	w:1,
	h: 2,
	x: 0,
	y: 1,
	title: 'speed, kph',
	canvas_text: '',
	ws_selector: 'speed',
	plate_ctor: function(elem) {
	    return new Chart(elem.getContext('2d'), {
		type: 'line',
		data: {
			labels: ["A", "B", "C", "O", "G", "W", "S"],
			datasets: [{
				label: 'Company A',
				data: [12, 19, 3, 17, 6, 3, 7],
				backgroundColor: "rgba(182, 213, 139, 0.5)"
			}, {
				label: 'Company B',
				data: [2, 29, 5, 5, 2, 3, 10],
				backgroundColor: "rgba(182, 133, 139, 1)"
			}]
		}
	    });
	},
	on_update: function(new_value, plate) {

	}
    }
];
